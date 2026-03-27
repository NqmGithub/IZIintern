from odoo import http
from odoo.exceptions import UserError
from odoo.http import request
from odoo import fields


class PurchaseRequestController(http.Controller):
    def _parse_json_body(self):
        try:
            return request.get_json_data() or {}
        except ValueError:
            return None
    
    @http.route(
        '/api/v1/http/purchase-requests',
        type='http',
        auth='bearer',
        methods=['GET'],
        csrf=False,
    )
    def http_list(self, **kwargs):
        limit = int(kwargs.get('limit', 20))
        offset = int(kwargs.get('offset', 0))
        fields = ['id', 'name', 'create_date', 'write_date']
        records = request.env['purchase.request'].search_read([], fields, limit=limit, offset=offset)
        return request.make_json_response({'data': records, 'meta': {'limit': limit, 'offset': offset}}, status=200)

    @http.route(
        '/api/v1/http/purchase-requests/<int:record_id>',
        type='http',
        auth='bearer',
        methods=['GET'],
        csrf=False,
    )
    def http_read_one(self, record_id, **kwargs):
        fields = ['id', 'name', 'create_date', 'write_date']

        record = request.env['purchase.request'].browse(record_id)
        if not record.exists():
            return request.make_json_response({'error': {'code': 'NOT_FOUND', 'message': 'purchase.request not found'}}, status=404)
        return request.make_json_response({'data': record.read(fields)[0]}, status=200)

    @http.route(
        '/api/v1/http/purchase-requests',
        type='http',
        auth='bearer',
        methods=['POST'],
        csrf=False,
    )
    def http_create(self, **_kwargs):
        payload = self._parse_json_body()
        if payload is None:
            return request.make_json_response({'error': {'code': 'BAD_REQUEST', 'message': 'Invalid JSON body'}}, status=400)

        name = 'New'
        department_id = payload.get('department_id')
        if not department_id:
            return request.make_json_response({'error': {'code': 'BAD_REQUEST', 'message': 'Missing required field: department_id'}}, status=400)
        requester_id = payload.get('requester_id')
        if not requester_id:
            requester_id = request.env.user.id
        date = payload.get('date')
        if not date:
            date = fields.Date.context_today(request)
        description = payload.get('description')
        if not description:
            description = ''
        state = 'draft'
        vals = {
            'name': name,
            'department_id': department_id,
            'requester_id': requester_id,
            'date': date,
            'description': description,
            'state': state,
        }

        record_id = request.env['purchase.request'].create(vals).id
        return request.make_json_response({'id': record_id}, status=201)

    @http.route(
        '/api/v1/http/purchase-requests/<int:record_id>',
        type='http',
        auth='bearer',
        methods=['PUT'],
        csrf=False,
    )
    def http_update(self, record_id, **_kwargs):
        payload = self._parse_json_body()
        if payload is None:
            return request.make_json_response({'error': {'code': 'BAD_REQUEST', 'message': 'Invalid JSON body'}}, status=400)

        record = request.env['purchase.request'].browse(record_id)
        if not record.exists():
            return request.make_json_response({'error': {'code': 'NOT_FOUND', 'message': 'purchase.request not found'}}, status=404)

        vals = {}
        if 'state' in payload:
            vals['state'] = payload['state']
            if vals['state'] == 'approved' and not record.approver_id:
                vals['approver_id'] = request.env.user.id
                vals['date_approved'] = fields.Date.context_today(request)
            elif vals['state'] == 'rejected' and 'canceled_reason' in payload:
                vals['canceled_reason'] = payload['canceled_reason']
            elif vals['state'] == 'rejected' and 'canceled_reason' not in payload:
                return request.make_json_response({'error': {'code': 'BAD_REQUEST', 'message': 'Missing required field: canceled_reason for rejected state'}}, status=400)
            elif vals['state'] not in ['draft', 'waiting', 'approved', 'rejected']:
                return request.make_json_response({'error': {'code': 'BAD_REQUEST', 'message': 'Invalid state value'}}, status=400)
        else:
            return request.make_json_response({'error': {'code': 'BAD_REQUEST', 'message': 'Missing required field: state'}}, status=400)

        record.write(vals)
        return request.make_json_response({'updated': True, 'id': record_id}, status=200)

    @http.route(
        '/api/v1/http/purchase-requests/<int:record_id>',
        type='http',
        auth='bearer',
        methods=['DELETE'],
        csrf=False,
    )
    def http_delete(self, record_id, **_kwargs):
        record = request.env['purchase.request'].browse(record_id)
        if not record.exists():
            return request.make_json_response({'error': {'code': 'NOT_FOUND', 'message': 'purchase.request not found'}}, status=404)
        record.unlink()
        return request.make_json_response({'deleted': True, 'id': record_id}, status=200)


    