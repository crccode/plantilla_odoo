from odoo import models, fields, api


class JobOrderCategory(models.Model):
    _name = "custom.job.order.category"

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
    )
