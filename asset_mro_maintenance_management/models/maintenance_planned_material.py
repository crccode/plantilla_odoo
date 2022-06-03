# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenancePlannedMaterial(models.Model):
    _name = 'maintenance.planned.material'
    _description = 'Maintenance Planned Material'

    equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Maintenance Equipment',
    )
    product_id = fields.Many2one(
        'product.product',
        required=True,
    )
    quantity = fields.Float(
        string='Quantity',
        required=True,
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='UOM',
        required=True,
    )

    @api.onchange('product_id')
    def set_uom(self):
        for rec in self:
            rec.uom_id = rec.product_id.uom_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
