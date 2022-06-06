# -*- coding: utf-8 -*-

from odoo import models, fields


class JobType(models.Model):
    _name = 'job.type'
    _description = 'Job Type'

    name = fields.Char(
        string='Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    job_type = fields.Selection(
        selection=[
            ('material','Material'),
            ('labour','Labour'),
            ('overhead','Overhead')],
        string='Type',
        required=True,
    )
