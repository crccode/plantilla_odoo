# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    material_ids = fields.One2many(
        'maintenance.request.material',
        'maintenance_request_id',
        string='Maintenance Request Material',
        copy=True,
    )
    checklist_ids = fields.One2many(
        'maintenance.equipment.checklist',
        'maintenance_request_checklist_id',
        string='Material Equipment Checklist',
        copy=True
    )
    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
    )
    joborder_id = fields.Many2one(
        'project.task',
        required=False,
    )
    requisition_employee_id = fields.Many2one(
        'hr.employee',
        string='Material Requisition Employee',
    )
    is_task = fields.Boolean(
        string='Create Task',
        default=False,
        copy=False,
    )
    is_requisition = fields.Boolean(
        string='Create Requisition',
        default=False,
        copy=False,
    )

    #def _get_type_id(self):
    #    return self.env['purchase.requisition.type'].search([], limit=1)

    #type_id = fields.Many2one(
    #    'purchase.requisition.type',
    #    string="Agreement Type",
    #    required=True,
    #    default=_get_type_id,
    #)

    def _get_picking_in(self):
        #pick_in = self.env.ref#('stock.picking_type_in')
        pick_in = False
        if not pick_in:
            # company = self.env['res.company']._company_default_get(
            # 'purchase.requisition')
            company = self.env.company
            pick_in = self.env['stock.picking.type'].search(
                [('warehouse_id.company_id', '=', company.id),
                 ('code', '=', 'incoming')],
                limit=1,
            )
        return pick_in

    picking_type_id = fields.Many2one('stock.picking.type',
        'Operation Type',
        required=True,
        default=_get_picking_in,
    )

    # @api.multi #odoo13
    def write(self, values):
        for rec in self:
            if values.get('equipment_id', False):
                rec.checklist_ids.unlink()
                rec.material_ids.unlink()
                equipment = self.env['maintenance.equipment'].browse(
                values['equipment_id'])
                for line in equipment.equipment_checklist_ids:
                    checklist_vals = {
                        'name': line.name,
                        'note': line.note,
                        'maintenance_request_checklist_id': rec.id,
                    }
                    checklist = self.env['maintenance.equipment.checklist'].create(
                    checklist_vals)
                for line in equipment.material_ids:
                    if not 'description' in values  or not values.get('description'):
                        #raise ValidationError('Description should not be empty.')
                        # send_me = vals['name']
                        send_me = values.get('name', '/') #values['name'] #odoo13
                    else:
                        # send_me = vals['description']
                        send_me = values['description'] #odoo13
                    material_vals = {
                        'product_id': line.product_id.id,
                        'quantity': line.quantity,
                        'uom_id': line.uom_id.id,
                        'maintenance_request_id': rec.id,
                        'description' : send_me,
                    }
                    material = self.env['maintenance.request.material'].create(
                    material_vals)
                    
        return super(MaintenanceRequest, self).write(values)

    # @api.multi #odoo13
    def create_task(self):
        for rec in self:
            task_vals = {
                'name': rec.name,
                'description': rec.description,
                'user_id': rec.requisition_employee_id.user_id.id,
                # 'is_job_order': True,
                'custom_wo_is_job_order': True, #13
                }
            task = self.env['project.task'].create(task_vals)
            rec.joborder_id = task
            task.write({'maintenance_request_id': rec.id})
            rec.is_task = True
        # res = self.env.ref('website_job_workorder_request.action_website_job_workorder_request')
        res = self.env.ref('website_job_workorder_request.custom_wo_action_website_job_workorder_request') #13
        res = res.read()[0]
        res['domain'] = str([('maintenance_request_id', '=', self.id)])
        return res

    # @api.multi #odoo13
    def show_task(self):
        # res = self.env.ref('website_job_workorder_request.action_website_job_workorder_request')
        res = self.env.ref('website_job_workorder_request.custom_wo_action_website_job_workorder_request') #13
        res = res.read()[0]
        res['domain'] = str([('maintenance_request_id', '=', self.id)])
        return res

    # @api.multi #odoo13
    def create_purchase_requisition(self):
        for rec in self:
            if not rec.material_ids:
                raise UserError(_('Select Material Lines.'))
            if not rec.dest_location_id:
                raise UserError(_('Select Destination Location.'))
            if not rec.requisition_employee_id:
                raise UserError(_('Select Employee.'))
            if not rec.requisition_employee_id.department_id:
                raise UserError(_('Select Department on Employee.'))
            if rec.description:
                name = rec.description
            else:
                name = rec.equipment_id.name
            material_requisition_vals = {
                'request_date': fields.Datetime.now(),
                'department_id': rec.requisition_employee_id.department_id.id,
                'employee_id': rec.requisition_employee_id.id,
                'company_id': self.env.user.company_id.id,
                'reason': name,
                'dest_location_id': rec.dest_location_id.id,
                'name': rec.name,
                #'type_id': rec.type_id.id,
                'maintenance_request_id': rec.id,
                # 'joborder_id': rec.joborder_id.id,
                'custom_wo_joborder_id': rec.joborder_id.id, #13
                # 'picking_type_id': rec.picking_type_id.id,
                'custom_picking_type_id': rec.picking_type_id.id,
                }
            purchase_requisition = self.env['material.purchase.requisition'].create(
            material_requisition_vals)
            for line in rec.material_ids:
                line_vals = {
                    'product_id': line.product_id.id,
                    'qty': line.quantity,
                    'uom': line.product_id.uom_id.id,
                    # 'price_unit': line.product_id.standard_price, #odoo13
                    'description': line.product_id.name,
                    'requisition_type': 'internal',
                    'requisition_id': purchase_requisition.id,
                }
                requisition_line = self.env['material.purchase.requisition.line'].create(line_vals)
        rec.is_requisition = True
        res = self.env.ref('material_purchase_requisitions.action_material_purchase_requisition')
        res = res.read()[0]
        res['domain'] = str([('maintenance_request_id', '=', rec.id)])
        return res

    # @api.multi #odoo13
    def show_purchase_requisition(self):
        res = self.env.ref('material_purchase_requisitions.action_material_purchase_requisition')
        res = res.read()[0]
        res['domain'] = str([('maintenance_request_id', '=', self.id)])
        return res

    @api.model
    def create(self, vals):
        res = super(MaintenanceRequest, self).create(vals)
        if vals.get('equipment_id', False):
            equipment = self.env['maintenance.equipment'].browse(vals['equipment_id'])
            for line in equipment.equipment_checklist_ids:
                checklist_vals = {
                    'name': line.name,
                    'note': line.note,
                    'maintenance_request_checklist_id': res.id,
                }
                checklist = self.env['maintenance.equipment.checklist'].create(
                checklist_vals)
            for line in equipment.material_ids:
                if not 'description' in vals or not vals.get('description'):
                    #raise ValidationError('Description should not be empty.')
                    send_me = vals['name']
                else:
                    send_me = vals['description']
                material_vals = {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'maintenance_request_id': res.id,
                    'description' : send_me,
                }
                material = self.env['maintenance.request.material'].create(
                material_vals)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
