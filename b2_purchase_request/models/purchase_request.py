from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    
    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, default=lambda self: 'New')
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
    ], string='Status', default='draft', group_expand='_expand_states')
    total_quantity = fields.Float(string='Total Quantity', compute='_compute_total_quantity')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    canceled_reason = fields.Text(string='Reason for Cancellation')

    def _expand_states(self, states, domain):
        return [key for key, val in self._fields['state'].selection]

    @api.depends('request_line_ids.quantity')
    def _compute_total_quantity(self):
        for request in self:
            request.total_quantity = sum(request.request_line_ids.mapped('quantity'))

    @api.depends('request_line_ids.total')
    def _compute_total_amount(self):
        for request in self:
            request.total_amount = sum(request.request_line_ids.mapped('total'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'New'

        return super(PurchaseRequest, self).create(vals_list)
    
    def unlink(self):
        for request in self:
            if request.state != 'draft':
                raise UserError(_('Only draft purchase requests can be deleted.'))
        return super().unlink()
    
    def export_data(self, fields=None, format=False, raw_data=False):
        if fields and 'state' in fields:
            for request in self:
                if request.state != 'approved':
                    raise UserError(_('Only approved purchase requests can be exported.'))
        return super().export_data(fields=fields, format=format, raw_data=raw_data)

    def action_request_approve(self):
        for request in self:
            if not request.request_line_ids:
                raise UserError(_('You cannot submit a purchase request without any lines.'))
            request.state = 'waiting'

    def action_back_to_draft(self):
        for request in self:
            request.state = 'draft'

    def action_approve(self):
        for request in self:
            if not request.approver_id:
                request.approver_id = self.env.user
            request.date_approved = fields.Date.context_today(self)
            request.state = 'approved'    
    
    def action_reject_request(self):
        return {
            'name': _('Reject Purchase Request Reason'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.request.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
            },
        }

    def action_export(self):
        return {
            'name': _('Export Purchase Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.request.export.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_ids': self.ids,
            },
        }
    