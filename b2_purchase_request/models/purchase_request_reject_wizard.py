
from odoo import fields, models


class PurchaseRquestRejectWizard(models.TransientModel):
    _name = 'purchase.request.reject.wizard'
    _description = 'Purchase Request Reject Wizard'

    reason = fields.Text(string='Reason for Rejection', required=True)

    def action_reject(self):
        active_id = self.env.context.get('active_id')
        request = self.env['purchase.request'].browse(active_id)
        request.canceled_reason = self.reason
        request.state = 'canceled'
        
        return { 'type': 'ir.actions.act_window_close' }