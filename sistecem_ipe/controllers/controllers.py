# -*- coding: utf-8 -*-
# from odoo import http


# class SistecemIpe(http.Controller):
#     @http.route('/sistecem_ipe/sistecem_ipe/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sistecem_ipe/sistecem_ipe/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sistecem_ipe.listing', {
#             'root': '/sistecem_ipe/sistecem_ipe',
#             'objects': http.request.env['sistecem_ipe.sistecem_ipe'].search([]),
#         })

#     @http.route('/sistecem_ipe/sistecem_ipe/objects/<model("sistecem_ipe.sistecem_ipe"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sistecem_ipe.object', {
#             'object': obj
#         })
