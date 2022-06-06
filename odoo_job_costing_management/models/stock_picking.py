# # -*- coding: utf-8 -*-
# 
# from odoo import models, fields, api
# 
# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#     
#     @api.multi
#     @api.onchange('task_id',
#                   'project_id',
#                   'analytic_account_id')
#     def onchange_project_task(self):
#         for rec in self:
#             rec.project_id = rec.task_id.project_id.id
#             rec.analytic_account_id = rec.task_id.project_id.analytic_account_id.id
#     
#     @api.multi
#     @api.depends('move_lines',
#                  'move_lines.product_id',
#                  'product_id.boq_type')
#     def compute_equipment_machine(self):
#         eqp_machine_total = 0.0
#         work_resource_total = 0.0
#         work_cost_package_total = 0.0
#         subcontract_total = 0.0
#         for rec in self:
#             for line in rec.move_lines:
#                 if line.product_id.boq_type == 'eqp_machine':
#                     eqp_machine_total += line.product_id.standard_price * line.product_uom_qty
#                 if line.product_id.boq_type == 'worker_resource':
#                     work_resource_total += line.product_id.standard_price * line.product_uom_qty
#                 if line.product_id.boq_type == 'work_cost_package':
#                     work_cost_package_total += line.product_id.standard_price * line.product_uom_qty
#                 if line.product_id.boq_type == 'subcontract':
#                     subcontract_total += line.product_id.standard_price * line.product_uom_qty
#             rec.equipment_machine_total = eqp_machine_total
#             rec.worker_resource_total = work_resource_total
#             rec.work_cost_package_total = work_cost_package_total
#             rec.subcontract_total = subcontract_total
#     
#     @api.multi
#     @api.depends('purchase_order_ids')
#     def _purchase_order_count(self):
#         for rec in self:
#             rec.purchase_order_count = len(rec.purchase_order_ids)
#     
#     task_id = fields.Many2one(
#         'project.task',
#         string='Task / Job Order',
#     )
#     task_user_id = fields.Many2one(
#         'res.users',
#         related='task_id.user_id',
#         string='Task / Job Order User'
#     )
#     project_id = fields.Many2one(
#         'project.project',
#         string='Construction Project',
#     )
#     purchase_order_id = fields.Many2one(
#         'purchase.order',
#         string='Purchase Order',
#     )
#     analytic_account_id = fields.Many2one(
#         'account.analytic.account',
#         string='Analytic Account',
#     )
#     purchase_order_ids = fields.Many2many(
#         'purchase.order', 
#         string='Purchase Orders',
#     )
#     purchase_order_count = fields.Integer(
#         compute='_purchase_order_count', 
#         string="Purchase Orders",
#         store=True,
#     )
#     equipment_machine_total = fields.Float(
#         compute='compute_equipment_machine',
#         string='Equipment / Machinery Cost',
#         store=True,
#     )
#     worker_resource_total = fields.Float(
#         compute='compute_equipment_machine',
#         string='Worker / Resource Cost',
#         store=True,
#     )
#     work_cost_package_total = fields.Float(
#         compute='compute_equipment_machine',
#         string='Work Cost Package',
#         store=True,
#     )
#     subcontract_total = fields.Float(
#         compute='compute_equipment_machine',
#         string='Subcontract Cost',
#         store=True,
#     )
#     
#         
#     @api.multi
#     def view_purchase_order(self):
#         for rec in self:
#             res = self.env.ref('odoo_job_costing_management.purchase_rfq_construction')
#             res = res.read()[0]
#             res['domain'] = str([('id','in',rec.purchase_order_ids.ids)])
#         return res