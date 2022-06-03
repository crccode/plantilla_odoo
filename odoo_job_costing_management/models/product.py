# -*- coding: utf-8 -*-

from odoo import models, fields


class Product(models.Model):
    _inherit = 'product.product'

    boq_type = fields.Selection([
        ('eqp_machine', 'Machinery / Equipment'),
        ('worker_resource', 'Worker / Resource'),
        ('work_cost_package', 'Work Cost Package'),
        ('subcontract', 'Subcontract')], 
        string='BOQ Type', 
    )
