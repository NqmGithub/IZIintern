from odoo import fields, models, api


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    requester_id = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, required=True)
    approver_id = fields.Many2one('res.users', string='Approved By')
    date = fields.Date(string='Request Date', default=fields.Date.context_today, required=True)
    date_approved = fields.Date(string='Approval Date')
    request_line_ids = fields.One2many('purchase.request.line', 'request_id', string='Request Lines')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),   
    ], string='Status', default='draft', tracking=True)
    total_quantity = fields.Float(string='Total Quantity', compute='_compute_total_quantity')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')

    @api.depends('request_line_ids.quantity')
    def _compute_total_quantity(self):
        for request in self:
            request.total_quantity = sum(request.request_line_ids.mapped('quantity'))

    @api.depends('request_line_ids.total')
    def _compute_total_amount(self):
        for request in self:
            request.total_amount = sum(request.request_line_ids.mapped('total'))
