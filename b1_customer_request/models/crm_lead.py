from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many('customer.request', 'opportunity_id', string='Customer Requests')
    sale_amount = fields.Float(string='Sale Amount', compute='_compute_sale_amount')
    revenue = fields.Float(string='Revenue', compute='_compute_revenue')
    is_stage_past_new = fields.Boolean(compute='_compute_is_stage_past_new')

    @api.depends('stage_id.sequence')
    def _compute_is_stage_past_new(self):
        for lead in self:
            lead.is_stage_past_new = bool(lead.stage_id and lead.stage_id.sequence > 1)

    @api.depends('request_ids.quantity')
    def _compute_sale_amount(self):
        for lead in self:
            lead.sale_amount = sum(lead.request_ids.mapped('quantity'))
    
    @api.depends('request_ids.quantity', 'request_ids.product_id.list_price')
    def _compute_revenue(self):
        for lead in self:
            total = 0.0
            for request in lead.request_ids:
                price = request.product_id.list_price or 0.0
                total += request.quantity * price
            lead.revenue = total

    def _prepare_opportunity_quotation_context(self):
        context = super()._prepare_opportunity_quotation_context()
        self.ensure_one()

        order_lines = []
        for request in self.request_ids:
            variant = request.product_id.product_variant_id
            if not variant:
                continue
            order_lines.append((0, 0, {
                'product_id': variant.id,
                'name': request.description or request.product_id.name,
                'product_uom_qty': request.quantity,
                'price_unit': variant.lst_price,
                'product_uom_id': variant.uom_id.id,
            }))

        if order_lines:
            context['default_order_line'] = order_lines
        return context

    def write(self, vals):
        for lead in self:
            if lead.stage_id.sequence > 1 and 'stage_id' not in vals:
                raise UserError("You cannot modify this record once it has left the New stage.")
        return super().write(vals)
    
    def unlink(self):
        for lead in self:
            if lead.stage_id.sequence > 1:
                raise UserError("You cannot delete this record once it has left the New stage.")
        return super().unlink()
