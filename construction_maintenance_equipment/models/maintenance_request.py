# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    custom_project_id = fields.Many2one(
        'project.project',
        'Project',
        copy=False,
    )
    custom_job_order_id = fields.Many2one(
        'project.task',
        'Job Order',
        copy=False,
    )