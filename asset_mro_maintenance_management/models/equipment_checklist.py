# -*- coding: utf-8 -*-

from odoo import models, fields


class EquipmentChecklist(models.Model):
    _name = 'equipment.checklist'
    _description = 'Equipment Checklist'

    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Maintenance Equipment',
    )
    name = fields.Char(
        string='Checklist Name',
        required=True,
    )
    note = fields.Char(
        string='Description',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
