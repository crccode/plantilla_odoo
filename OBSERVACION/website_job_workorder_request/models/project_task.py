# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    #@api.multi
    @api.depends('custom_wo_purchase_requisition_ids')
    def customwo_purchase_requisition_count(self):
        for rec in self:
            rec.custom_wo_purchase_requisition_count = len(rec.custom_wo_purchase_requisition_ids)

    custom_wo_number = fields.Char(
        string='Number',
        readonly=True,
    )
    custom_wo_job_partner_id = fields.Many2one(
        'res.partner',
        string = "Website Customer"
    )
    custom_wo_job_partner_name = fields.Char(
        string = "Website Customer Name"
    )
    custom_wo_job_partner_email = fields.Char(
        string = "Website Customer Email"
    )
    custom_wo_job_partner_phone = fields.Char(
        string = "Website Customer Phone"
    )
    custom_wo_job_category = fields.Selection(
        selection = [
            ('new_request', 'New Request'),
            ('maintenance', 'Maintenance'),
            ('repair', 'Repair'),
            ('technical', 'Technical'),
            ('other', 'Other')
        ],
        string = "Job Order Category",
    )#UNUSED
    custom_wo_job_category_id = fields.Many2one(
        'custom.job.order.category',
        string="Job Order Category",
    )
    custom_wo_is_job_order = fields.Boolean(
        string = "Is Job Order",
        defulat=False,
    )
    custom_wo_purchase_requisition_ids = fields.One2many(
        'material.purchase.requisition',
        'custom_wo_joborder_id',
        string='Purchase Requisitions',
    )
    custom_wo_purchase_requisition_count = fields.Integer(
        compute='customwo_purchase_requisition_count',
        store=True,
     )
     
    custom_wo_custome_client_user_id = fields.Many2one(
        'res.users',
        string="Job Order Created User",
        readonly = True,
        track_visibility='always'
    )

    @api.model
    def create(self, vals):
        number = self.env['ir.sequence'].next_by_code('job.order.seq')
        if vals.get('custom_wo_custome_client_user_id', False):
            client_user_id = self.env['res.users'].browse(int(vals.get('custom_wo_custome_client_user_id')))
            if client_user_id:
                vals.update({'company_id': client_user_id.company_id.id,
                'custom_wo_number': number})
        else:
            vals.update({'custom_wo_custome_client_user_id': self.env.user.id,
            'custom_wo_number': number})
        return super(ProjectTask, self).create(vals)

#    @api.model
#    def create(self, vals):
#        number = self.env['ir.sequence'].next_by_code('job.order.seq')
#        vals.update({
#            'number': number
#            })
#        return super(ProjectTask, self).create(vals)

    #@api.multi
    def custom_wo_send_joborder(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('website_job_workorder_request', 'custom_wo_email_template_job_order_to_customer')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'project.task',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            #'custom_layout': "sale.mail_template_data_notification_email_sale_order",
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    #@api.multi
    def custom_wo_show_purchase_requisition(self):
#        sel.ensure_one()
        self.ensure_one()
        res = self.env.ref('material_purchase_requisitions.action_material_purchase_requisition')
        res = res.read()[0]
        res['domain'] = str([('id','in', self.custom_wo_purchase_requisition_ids.ids)])
        return res

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    custome_code = fields.Char(
        string="Reference",
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
