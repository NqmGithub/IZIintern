# from odoo import http


# class B1CustomerRequest(http.Controller):
#     @http.route('/b1_customer_request/b1_customer_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/b1_customer_request/b1_customer_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('b1_customer_request.listing', {
#             'root': '/b1_customer_request/b1_customer_request',
#             'objects': http.request.env['b1_customer_request.b1_customer_request'].search([]),
#         })

#     @http.route('/b1_customer_request/b1_customer_request/objects/<model("b1_customer_request.b1_customer_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('b1_customer_request.object', {
#             'object': obj
#         })

