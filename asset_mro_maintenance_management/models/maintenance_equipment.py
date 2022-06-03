# -*- coding: utf-8 -*-

from odoo import models, fields


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    equipment_checklist_ids = fields.Many2many(
        'equipment.checklist',
        string='Equipment Checklist',
    )
    material_ids = fields.One2many(
        'maintenance.planned.material',
        'equipment_id',
        string='Maintenance Planned Material',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
