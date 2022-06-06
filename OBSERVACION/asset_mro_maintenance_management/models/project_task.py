# -*- coding: utf-8 -*-

from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = "project.task"

    maintenance_request_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
        readonly=True,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
