# -*- coding: utf-8 -*-

from odoo import fields, models, api

class MaterialPurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'
    
    custom_wo_joborder_id = fields.Many2one(
        'project.task',
        string='Job Order',
    )
    custom_wo_project_id = fields.Many2one(
        'project.project',
        string='Project',
    )
    
    
    @api.onchange('custom_wo_joborder_id')
    def custom_wo_set_project(self):
        for rec in self:
            rec.custom_wo_project_id = rec.custom_wo_joborder_id.project_id.id
            
    @api.onchange('custom_wo_project_id')
    def custom_wo_set_analytic_account(self):
        for rec in self:
            rec.analytic_account_id = rec.custom_wo_project_id.analytic_account_id.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
