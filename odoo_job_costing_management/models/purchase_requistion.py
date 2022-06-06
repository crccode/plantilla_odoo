# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError


class PurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    #@api.multi
    @api.onchange('task_id')
    def onchange_project_task(self):
        for rec in self:
            rec.project_id = rec.task_id.project_id.id
            rec.analytic_account_id = rec.task_id.project_id.analytic_account_id.id

    #@api.multi
    @api.depends('requisition_line_ids',
                 'requisition_line_ids.product_id',
                 'requisition_line_ids.product_id.boq_type')
    def compute_equipment_machine(self):
        eqp_machine_total = 0.0
        work_resource_total = 0.0
        work_cost_package_total = 0.0
        subcontract_total = 0.0
        for rec in self:
            for line in rec.requisition_line_ids:
                if line.product_id.boq_type == 'eqp_machine':
                    eqp_machine_total += line.product_id.standard_price * line.qty
                if line.product_id.boq_type == 'worker_resource':
                    work_resource_total += line.product_id.standard_price * line.qty
                if line.product_id.boq_type == 'work_cost_package':
                    work_cost_package_total += line.product_id.standard_price * line.qty
                if line.product_id.boq_type == 'subcontract':
                    subcontract_total += line.product_id.standard_price * line.qty
            print ("::::::::::::::::::::::::eqp_machine_total",eqp_machine_total)
            rec.equipment_machine_total = eqp_machine_total
            rec.worker_resource_total = work_resource_total
            rec.work_cost_package_total = work_cost_package_total
            rec.subcontract_total = subcontract_total

#     #@api.multi
#     @api.depends('purchase_order_ids')
#     def _purchase_order_count(self):
#         for rec in self:
#             rec.purchase_order_count = len(rec.purchase_order_ids)

    task_id = fields.Many2one(
        'project.task',
        string='Task / Job Order',
    )
    task_user_id = fields.Many2one(
        'res.users',
        related='task_id.user_id',
        string='Task / Job Order User'
    )
    project_id = fields.Many2one(
        'project.project',
        string='Construction Project',
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
    )
#     analytic_account_id = fields.Many2one(
#         'account.analytic.account',
#         string='Analytic Account',
#     )
    purchase_order_ids = fields.Many2many(
        'purchase.order', 
        string='Purchase Orders',
    )
#     purchase_order_count = fields.Integer(
#         compute='_purchase_order_count', 
#         string="Purchase Orders",
#         store=True,
#     )
    equipment_machine_total = fields.Float(
        compute='compute_equipment_machine',
        string='Equipment / Machinery Cost',
        store=True,
    )
    worker_resource_total = fields.Float(
        compute='compute_equipment_machine',
        string='Worker / Resource Cost',
        store=True,
    )
    work_cost_package_total = fields.Float(
        compute='compute_equipment_machine',
        string='Work Cost Package',
        store=True,
    )
    subcontract_total = fields.Float(
        compute='compute_equipment_machine',
        string='Subcontract Cost',
        store=True,
    )
    
    
class MaterialPurchaseRequisitionLine(models.Model):   
    _inherit = 'material.purchase.requisition.line'
    
    job_cost_id = fields.Many2one(
        'job.costing',readonly=False,    
        string='Job Cost Center',
    )
    job_cost_line_id = fields.Many2one(
        'job.cost.line',
        string='Job Cost Line',
    )
    project_id = fields.Many2one(related='requisition_id.project_id', depends=['requisition_id.project_id'], readonly=False, string="Proyecto", store=True)
    qty_left = fields.Float(compute='_compute_restante', string='Cant Restante', store=True)
    
    @api.depends('job_cost_line_id','job_cost_line_id.product_qty','job_cost_line_id.actual_quantity')
    def _compute_restante(self):
        for line in self:
            line.qty_left = sum([p.product_qty for p in line.job_cost_line_id])-sum([p.actual_quantity for p in line.job_cost_line_id]) 