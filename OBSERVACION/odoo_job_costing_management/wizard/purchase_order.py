# -*- coding: utf-8 -*-

from datetime import date,time

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class PurchaseOrderWizard(models.TransientModel):
    _name = 'purchase.order.wizard'

    supplier_ids = fields.Many2many(
        'res.partner',
        string='Suppliers',
        required=True,
    )
    product_line_ids = fields.One2many(
        'product.lines',
        'product_line_id',
        'Product Lines'
    )

    @api.model
    def default_get(self, fields):
        rec = super(PurchaseOrderWizard, self).default_get(fields)
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        picking = self.env[active_model].browse(active_ids)
        vals = []
        for line in picking.move_lines:
            vals.append((0,0,{'product_id': line.product_id.id,
                             'quantity': line.product_uom_qty,
                             'product_uom': line.product_uom.id,
                             'qty_available': line.product_id.qty_available,
                              }))
        rec.update({'product_line_ids': vals})
        return rec

    #@api.multi
    def _prepare_purchase_order(self, vendor):
        self.ensure_one()
        stock_pick_obj = self.env['stock.picking'].browse(self._context.get('active_ids', []))
        
        fpos = self.env['account.fiscal.position'].with_context(\
                company_id=vendor.company_id.id).get_fiscal_position(vendor.id)
        
        purchase_req_vals = {
            'partner_id': vendor.id,
            'company_id': vendor.company_id.id,
            'currency_id': vendor.property_purchase_currency_id.id \
                            or self.env.user.company_id.currency_id.id,
            'origin': stock_pick_obj.name,
            'payment_term_id': vendor.property_supplier_payment_term_id.id,
            'fiscal_position_id': fpos,
#            'date_order' : datetime.today(),
            #'picking_id':vendor.id
        }
        return purchase_req_vals

    #@api.multi
    def create_purchase_requistion(self):
        picking = self.env['stock.picking'].browse(self._context.get('active_ids', []))
        purchase_obj = self.env['purchase.order']
        order_lines = self.env['purchase.order.line']
        order_ids = []
        date_planned = datetime.today()
        for rec in self.supplier_ids:
            purchase_order = self._prepare_purchase_order(rec)
            purchase = purchase_obj.sudo().create(purchase_order)
            order_ids.append(purchase.id)
            for line in self.product_line_ids:
                # Create Purchase order Lines
                line_vals =  {
                         'product_id': line.product_id.id,
                         'name':line.product_id.name,
                         'product_qty': line.quantity,
                         'product_uom': line.product_uom.id,
                         'date_planned': datetime.today(),
                         'price_unit': line.product_id.standard_price,
#                          'qty_available': line.product_id.qty_available,
                         'order_id': purchase.id,
                         }
                purchase_order_line = order_lines.sudo().create(line_vals)
                purchase_order_line.order_id = purchase.id
        picking[0].purchase_order_ids = order_ids


class ProductLines(models.TransientModel):
    _name = 'product.lines'

    product_id = fields.Many2one(
        'product.product',
        string='Product'
    )
    quantity = fields.Integer(
        'Quantity'
    )
    product_uom = fields.Many2one(
        'uom.uom',#product.uom
        'Unit of Measure'
    )
    qty_available = fields.Float(
        'Quantity On Hand',
    )
    product_line_id = fields.Many2one(
        'purchase.order.wizard'
        'Purchase Order wizard'
    )
