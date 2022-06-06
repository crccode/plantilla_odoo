# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectUserSubtask(models.TransientModel):
    _name = 'project.user.subtask'
    _description = 'Project User Subtask'

    subtask_user_ids = fields.One2many(
        'user.subtask', 
        'subtask_id',
        string="Project Subtask User",
        required=True,
    )
    
    #@api.multi
    def create_subtask(self):
        task_id = self._context.get('active_id', False)
        task = self.env['project.task'].browse(task_id)
        subtask_ids = []
        for subtask in self.subtask_user_ids:
            #copy_task_vals = task.copy() #13may2020
            vals = {
                'planned_hours' : subtask.planned_hours,
                'description'   : subtask.description,
                'user_id'       : subtask.user_id.id,
                'name'          : subtask.name,
                'parent_task_id' : task.id,
                'parent_id'      : task.id,
                'project_id'     : task.project_id.id,
                'company_id'     : task.company_id.id,
            }
            copy_task_vals = self.env['project.task'].create(vals)
            # copy_task_vals.planned_hours = subtask.planned_hours
            # copy_task_vals.description = subtask.description
            # copy_task_vals.user_id = subtask.user_id
            # copy_task_vals.name = subtask.name
            # copy_task_vals.parent_task_id = task.id
            # copy_task_vals.parent_id = task.id
            #copy_task_vals.company_id = task.company_id #13may2020
            subtask_ids.append(copy_task_vals.id)
        if subtask_ids:
#            result = self.env.ref('odoo_job_costing_management.action_view_task_subtask')
            result = self.env.ref('project.project_task_action_sub_task')#ODOO 13
            result = result.read()[0]
            result['domain'] = "[('id','in',[" + ','.join(map(str, subtask_ids)) + "])]"
            return result
        return True
    
class UserSubtask(models.TransientModel):
    _name = 'user.subtask'
    _description = 'User Subtask'
    
    user_id = fields.Many2one(
        'res.users',
        string="User",
        required=True,
    )
    name = fields.Char(
        string='Task Name',
        required=True,
    )
    description = fields.Text(
        string='Task Description',
        required=True,
    )
    planned_hours = fields.Float(
        'Planned Hours',
        required=True,
    )
    subtask_id = fields.Many2one(
        'project.user.subtask',
        string='Project User Subtask'
    )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
