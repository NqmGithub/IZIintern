from odoo import _, api, fields, models
from odoo.exceptions import UserError

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', ondelete='cascade')
    product_id = fields.Many2one('product.template', string='Product', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    quantity_approved = fields.Float(string='Quantity Approved')
    total = fields.Float(string='Total', compute='_compute_total')
    price_unit = fields.Float(string='Unit Price')
    state = fields.Selection(related='request_id.state', string='Request State', store=True)
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.product_id:
            self.uom_id = False
            self.price_unit = 0.0
            return
        self.uom_id = self.product_id.uom_id
        
        lastest_price = self.env['purchase.order.line'].search([
            ('product_id', '=', self.product_id.id)],
              order='id desc', limit=1)
        if lastest_price:
            self.price_unit = lastest_price.price_unit
        else:
            self.price_unit = self.product_id.list_price

    @api.depends('quantity', 'product_id.list_price')
    def _compute_total(self):
        for line in self:
            price = line.product_id.list_price or 0.0
            line.total = line.quantity * price

    def unlink(self):
        for line in self:
            if line.state != 'draft':
                raise UserError(_('Only lines of draft purchase requests can be deleted.'))
        return super().unlink()
    
    def write(self, vals):
        for line in self:
            if line.state != 'draft':
                raise UserError(_('Only lines of draft purchase requests can be modified.'))
        return super().write(vals)