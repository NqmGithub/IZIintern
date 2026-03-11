from odoo import models, fields, api

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', ondelete='cascade')
    product_id = fields.Many2one('product.template', string='Product', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    quantity_approved = fields.Float(string='Quantity Approved')
    total = fields.Float(string='Total', compute='_compute_total')

    @api.depends('quantity', 'product_id.list_price')
    def _compute_total(self):
        for line in self:
            price = line.product_id.list_price or 0.0
            line.total = line.quantity * price