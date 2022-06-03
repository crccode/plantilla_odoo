# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'
    
    custom_maintenance_request_id = fields.Many2one(
        'maintenance.request',
        'Maintenance Request'
    )
    
    #@api.multi
    def _compute_maintenance_request_count(self):
        maintenance_request = self.env['maintenance.request']
        maintenance_request_ids = self.mapped('maintenance_request_ids')
        for project in self:
            project.maintenance_request_count = maintenance_request.search_count([('id', 'in', maintenance_request_ids.ids)])
    
    
    maintenance_request_count = fields.Integer(
        compute='_compute_maintenance_request_count'
    )
    
    maintenance_request_ids = fields.One2many(
        'maintenance.request',
        'custom_project_id',
    )
    
    #@api.multi
    def action_projectmaintenance_request_count(self):
        maintenance_request = self.mapped('maintenance_request_ids')
        action = self.env.ref('maintenance.hr_equipment_request_action').read()[0]
        action['domain'] = [('id', 'in', maintenance_request.ids)]
        return action

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    custom_maintenance_request_id = fields.Many2one(
        'maintenance.request',
        'Maintenance Request'
    )
    
    #@api.multi
    def _compute_maintenance_request_count(self):
        maintenance_request = self.env['maintenance.request']
        maintenance_request_ids = self.mapped('maintenance_request_ids')
        for task in self:
            task.maintenance_request_count = maintenance_request.search_count([('id', 'in', maintenance_request_ids.ids)])
    
    
    maintenance_request_count = fields.Integer(
        compute='_compute_maintenance_request_count'
    )
    
    maintenance_request_ids = fields.One2many(
        'maintenance.request',
        'custom_job_order_id',
    )
    
    #@api.multi
    def action_taskmaintenance_request_count(self):
        maintenance_request = self.mapped('maintenance_request_ids')
        action = self.env.ref('maintenance.hr_equipment_request_action').read()[0]
        action['domain'] = [('id', 'in', maintenance_request.ids)]
        return action

