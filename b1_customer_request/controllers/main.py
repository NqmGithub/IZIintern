import json
from odoo import http
from odoo.http import request

class CrmApi(http.Controller):
    @http.route('/api/v1/create_lead', auth='none', type='json', methods=['POST'], csrf=False)
    def create_lead(self, **kwargs):
        data = kwargs

        admin_user = request.env['res.users'].sudo().search([('id', '=', 2)], limit=1)
        request.update_env(user=admin_user)

        lead = request.env['crm.lead'].sudo().create({
            'name': data.get('name'),
            'partner_id': data.get('partner_id'),
            'email_from': data.get('email_from'),
            'phone': data.get('phone'),
            'date_deadline': data.get('date_deadline'), 
            'description': data.get('description'),
        })

        customer_requests = data.get('customer_requests', [])
        for req in customer_requests:
            product_id = req.get('product_id')
            description = req.get('description')
            date = req.get('date')
            quantity = req.get('quantity')

            request.env['customer.request'].sudo().create({
                'product_id': product_id,
                'opportunity_id': lead.id,
                'description': description,
                'date': date,
                'quantity': quantity,
            })
        return {'status': 'success', 'lead_id': lead.id}
        
