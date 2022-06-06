# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    picking_id = fields.Many2one(
        'stock.picking',
        string='Stock Picking',
    )


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_account_move_line(self, move):#To pass jobcosting details to the vendor billline(s)
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move=move)
        res.update({
            'job_cost_id': self.job_cost_id.id,
            'job_cost_line_id': self.job_cost_line_id.id,
        })
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

