from email.policy import default
import re

from odoo import models, fields, api
from odoo.orm.domains import operator_optimization


class CustomerRequest(models.Model):
    _name = 'customer.request'
    _description = 'Customer Request'

    product_id = fields.Many2one('product.template', string='Product', required=True)
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0, required=True)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many('customer.request', 'opportunity_id', string='Customer Requests')
    sale_amount = fields.Float(string='Sale Amount', compute='_compute_sale_amount')
    revenue = fields.Float(string='Revenue', compute='_compute_revenue')

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
            
    



