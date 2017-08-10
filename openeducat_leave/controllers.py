# -*- coding: utf-8 -*-
from openerp import http

# class OpeneducatLeave(http.Controller):
#     @http.route('/openeducat_leave/openeducat_leave/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_leave/openeducat_leave/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_leave.listing', {
#             'root': '/openeducat_leave/openeducat_leave',
#             'objects': http.request.env['openeducat_leave.openeducat_leave'].search([]),
#         })

#     @http.route('/openeducat_leave/openeducat_leave/objects/<model("openeducat_leave.openeducat_leave"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_leave.object', {
#             'object': obj
#         })