# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    start_time = fields.Float(
        string='Start Time',
    )
    end_time = fields.Float(
        string='End Time',
    )
    job_cost_id = fields.Many2one(
        'job.costing',
        string='Job Cost Center',
    )
    job_cost_line_id = fields.Many2one(
        'job.cost.line',
        string='Job Cost Line',
    )
    
