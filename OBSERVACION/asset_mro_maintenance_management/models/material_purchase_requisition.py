# -*- encoding: utf-8 -*-

from odoo import api, fields, models


class PurchaseRequisition(models.Model):
    _inherit = "material.purchase.requisition"
    
    maintenance_request_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
        readonly=True,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
