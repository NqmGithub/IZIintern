# from odoo import http


# class B2PurchaseRequest(http.Controller):
#     @http.route('/b2_purchase_request/b2_purchase_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/b2_purchase_request/b2_purchase_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('b2_purchase_request.listing', {
#             'root': '/b2_purchase_request/b2_purchase_request',
#             'objects': http.request.env['b2_purchase_request.b2_purchase_request'].search([]),
#         })

#     @http.route('/b2_purchase_request/b2_purchase_request/objects/<model("b2_purchase_request.b2_purchase_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('b2_purchase_request.object', {
#             'object': obj
#         })

