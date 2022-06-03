# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    job_cost_id = fields.Many2one(
        'job.costing',
        string='Job Cost Center',
    )
    job_cost_line_id = fields.Many2one(
        'job.cost.line',
        string='Job Cost Line',
    )


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    #@api.multi THIS METHOD IS NOT USED ANY MORE SINCE THIS FEATURE HAS BEEN REMOVED IN ODOO 13.
    def button_confirm_unused(self):
        result = super(PurchaseOrder,self).button_confirm()
        cost_line_obj = self.env['job.cost.line']
        for order in self:
            for line in order.order_line:
                cost_id = line.job_cost_id
                if not line.job_cost_line_id:
                    if cost_id:
                        hours = 0.0
                        qty = 0.0
                        date = line.date_planned
                        product_id = line.product_id.id
                        description = line.name
                        if line.product_id.type == 'service':
                            job_type = 'labour'
                            hours = line.product_qty
                        else:
                            job_type = 'material'
                            qty = line.product_qty
                            
                        price = line.price_unit
                        vals={
                            'date':date,
                            'product_id':product_id,
                            'description':description,
                            'job_type':job_type,
                            'product_qty':qty,
                            'cost_price':price,
                            'hours':hours,
                        }
                        job_cost_line_id = cost_line_obj.create(vals)
                        line.job_cost_line_id = job_cost_line_id.id
                        job_cost_line_ids = cost_id.job_cost_line_ids.ids
                        job_cost_line_ids.append(job_cost_line_id.id)
                        if job_cost_line_id.job_type == 'labour':
                            cost_vals={
                                'job_labour_line_ids':[(6,0,job_cost_line_ids)],
                        }
                        else:
                            cost_vals={
                                'job_cost_line_ids':[(6,0,job_cost_line_ids)],
                        }
                        cost_id.update(cost_vals)
        return result
