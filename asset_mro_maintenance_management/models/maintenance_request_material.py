# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceRequestMaterial(models.Model):
    _name = 'maintenance.request.material'
    _description = 'Maintenance Request Material' 
    
    maintenance_request_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
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
    description = fields.Char(
        string='Description',
        required=True,
    )

    @api.onchange('product_id')
    def set_uom(self):
        for rec in self:
            rec.uom_id = rec.product_id.uom_id
            rec.description = rec.product_id.name

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
