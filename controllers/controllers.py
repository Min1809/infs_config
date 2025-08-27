# -*- coding: utf-8 -*-
# from odoo import http


# class InfsConfig(http.Controller):
#     @http.route('/infs_config/infs_config', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/infs_config/infs_config/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('infs_config.listing', {
#             'root': '/infs_config/infs_config',
#             'objects': http.request.env['infs_config.infs_config'].search([]),
#         })

#     @http.route('/infs_config/infs_config/objects/<model("infs_config.infs_config"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('infs_config.object', {
#             'object': obj
#         })

