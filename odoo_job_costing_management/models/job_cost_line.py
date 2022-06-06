# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class JobCostLine(models.Model): 
    _name = 'job.cost.line'
    _description = 'Job Cost Line'
    _rec_name = 'description'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            rec.description = rec.product_id.name
            rec.product_qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price#lst_price
    
    @api.depends('product_qty','hours','cost_price','direct_id')
    def _compute_total_cost(self):
        for rec in self:
            if rec.job_type == 'labour':
                rec.product_qty = 0.0
                rec.total_cost = rec.hours * rec.cost_price
            else:
                rec.hours = 0.0
                rec.total_cost = rec.product_qty * rec.cost_price
                
    #@api.depends('purchase_order_line_ids', 'purchase_order_line_ids.product_qty')
    @api.depends('purchase_order_line_ids', 'purchase_order_line_ids.product_qty', 'purchase_order_line_ids.order_id.state')
    def _compute_actual_quantity(self):
        for rec in self:
            #rec.actual_quantity = sum([p.product_qty for p in rec.purchase_order_line_ids])
            rec.actual_quantity = sum([p.order_id.state in ['purchase', 'done'] and p.product_qty for p in rec.purchase_order_line_ids])
            
    @api.depends('timesheet_line_ids','timesheet_line_ids.unit_amount')
    def _compute_actual_hour(self):
        for rec in self:
            rec.actual_hour = sum([p.unit_amount for p in rec.timesheet_line_ids])
    
    #@api.depends('account_invoice_line_ids','account_invoice_line_ids.quantity')
#    @api.depends('account_invoice_line_ids','account_invoice_line_ids.quantity', 'account_invoice_line_ids.invoice_id.state')
    @api.depends('account_invoice_line_ids',
        'account_invoice_line_ids.quantity',
        'account_invoice_line_ids.move_id.state',
        'account_invoice_line_ids.move_id.payment_state'
    )
    def _compute_actual_invoice_quantity(self):
        for rec in self:
            #rec.actual_invoice_quantity = sum([p.quantity for p in rec.account_invoice_line_ids])
#            rec.actual_invoice_quantity = sum([p.invoice_id.state in ['open', 'paid'] and p.quantity or 0.0 for p in rec.account_invoice_line_ids])
            rec.actual_invoice_quantity = sum([p.quantity or 0.0 for p in rec.account_invoice_line_ids if p.move_id.state in ['posted'] or p.move_id.payment_state in ['paid']])
    
    direct_id = fields.Many2one(
        'job.costing',
        string='Job Costing'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        copy=False,
        required=True,
    )
    description = fields.Char(
        string='Description',
        copy=False,
    )
    reference = fields.Char(
        string='Reference',
        copy=False,
    )
    date = fields.Date(
        string='Date',
        required=True,
        copy=False,
    )
    product_qty = fields.Float(
        string='Planned Qty',
        copy=False,
    )
    uom_id = fields.Many2one(
        'uom.uom',#product.uom
        string='Uom',
    )
    cost_price = fields.Float(
        string='Cost / Unit',
        copy=False,
    )
    total_cost = fields.Float(
        string='Cost Price Sub Total',
        compute='_compute_total_cost',
        store=True,
    )
    analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
    )
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        default=lambda self: self.env.user.company_id.currency_id, 
        readonly=True
    )
    job_type_id = fields.Many2one(
        'job.type',
        string='Job Type',
    )
    job_type = fields.Selection(
        selection=[('material','Material'),
                    ('labour','Labour'),
                    ('overhead','Overhead'),
                    ('subcontratista','Sub Contratista')
                ],
        string="Type",
        required=True,
    )
    basis = fields.Char(
        string='Basis'
    )
    hours = fields.Float(
        string='Hours'
    )
    purchase_order_line_ids = fields.One2many(
        'purchase.order.line',
        'job_cost_line_id',
    )
    timesheet_line_ids = fields.One2many(
        'account.analytic.line',
        'job_cost_line_id',
    )
    account_invoice_line_ids = fields.One2many(
#        'account.invoice.line',
        'account.move.line',
        'job_cost_line_id',
    )
    actual_quantity = fields.Float(
        string='Actual Purchased Quantity',
        compute='_compute_actual_quantity',
    )
    actual_invoice_quantity = fields.Float(
        string='Actual Vendor Bill Quantity',
        compute='_compute_actual_invoice_quantity',
    )
    actual_hour = fields.Float(
        string='Actual Timesheet Hours',
        compute='_compute_actual_hour',
    )
