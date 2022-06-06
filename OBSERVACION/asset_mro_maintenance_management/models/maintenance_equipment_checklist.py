# -*- coding: utf-8 -*-

from odoo import models, fields


class MaintenanceEquipmentChecklist(models.Model):
    _name = 'maintenance.equipment.checklist'
    _description = 'Maintenance Equipment Checklist'

    name = fields.Char(
        string='Checklist Name',
        required=True,
    )
    product_id = fields.Many2one(
        'product.product',
        required=False,
    )
    is_ok = fields.Boolean(
        string='Is Validated ?',
    )
    note = fields.Char(
        string='Description',
    )
    maintenance_request_checklist_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
