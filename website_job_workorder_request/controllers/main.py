# -*- coding: utf-8 -*-

import base64
from odoo import http, _
from odoo.http import request
# from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.portal.controllers.portal import CustomerPortal as website_account

class website_account(website_account):

    def _prepare_portal_layout_values(self):
        values = super(website_account, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        custom_wo_joborder_count = request.env['project.task'].sudo().search_count([('custom_wo_job_partner_id','=', partner.id)])
        values.update({
            'custom_wo_joborder_count': custom_wo_joborder_count,
        })
        return values

    def _prepare_custom_job_workorder_values(self, post):
        job_order_category_ids = request.env['custom.job.order.category'].search([])
        return {
            'custom_job_order_category_ids': job_order_category_ids,
        }

    @http.route(['/page/custom_wo_job_workorder'], type='http', auth="public", website=True)
    def custom_wo_show_joborder(self, **post):
        #return request.render("job_workorder_website_request.job_workorder")
        values = self._prepare_custom_job_workorder_values(post)
        return request.render("website_job_workorder_request.custom_wo_job_order", values)

    @http.route(['/custom_wo_job_order/custom_wo_website_joborder_submitted'], type='http', auth="public", methods=['POST'], website=True)
    def custom_wo_joborder_submitted(self, **post):
#        partner = request.env.user.partner_id odoo13
        vale = {
#            'job_partner_id' : partner.id, odoo13
            'name': post.get('name'),
            'custom_wo_job_partner_name': post.get('your_name'),
            'custom_wo_job_partner_email': post.get('email'),
            'custom_wo_job_partner_phone': post.get('phone'),
            'description': post.get('description'),
            'priority': post.get('priority'),
            'custom_wo_is_job_order' : True,
            'custom_wo_custome_client_user_id': request.env.user.id,
        }
        if post.get('custom_wo_job_category') != 'Select category':
            vale.update({'custom_wo_job_category': post.get('custom_wo_job_category')})
        if post.get("custom_wo_job_category_id"):
            vale.update({'custom_wo_job_category_id': int(post.get('custom_wo_job_category_id'))})
#        partner_id = request.env['res.partner'].sudo().search([('email', '=', post.get('email'))]) odoo13
        if request.env.user.has_group('base.group_public'):
            custom_partner_id = request.env['res.partner'].sudo().search([('email', '=', post.get('email'))], limit=1)
            if custom_partner_id:
                partner_id = custom_partner_id.id
            else:
                partner_id = False
        else:
            partner_id = request.env.user.partner_id.id
        if partner_id:
            vale.update({
                'custom_wo_job_partner_id': partner_id,
            })
#        project_id = request.env['project.project'].sudo().search([('code', '=', post.get('project_code'))], limit=1)
        project_id = request.env['project.project'].sudo().search([('custome_code', '=', post.get('project_code'))], limit=1)
        if project_id:
            vale.update({
                'project_id': project_id.id,
            })
        workorder_id = request.env['project.task'].sudo().create(vale)
        local_context = http.request.env.context.copy()
        local_context.update({
            'partner_name':  post.get('your_name'),
            'email': post.get('email'),
            'subject': workorder_id.name,
            #'job_number': workorder_id.job_number,
            'custom_wo_joborder_number': workorder_id.custom_wo_number,
        })
        #issue_template = http.request.env.ref('job_workorder_website_request.email_template_job_order')
        issue_template = http.request.env.ref('website_job_workorder_request.custom_wo_email_template_job_order_send_view')
        issue_template.sudo().with_context(local_context).send_mail(request.uid, force_send=False)
        attachment_list = request.httprequest.files.getlist('attachment')
        if workorder_id and attachment_list:
            for image in attachment_list:
                if post.get('attachment'):
                    attachments = {
                               'res_name': image.filename,
                               'res_model': 'project.task',
                               'res_id': workorder_id,
                               'datas': base64.b64encode(image.read()),
                               'type': 'binary',
                              # 'datas_fname': image.filename,
                               'name': image.filename,
                           }
                    attachment_obj = http.request.env['ir.attachment']
                    attach = attachment_obj.sudo().create(attachments)
        if len(attachment_list) > 0:
            group_msg = _('Customer has sent %s attachments to this joborder. Name of attachments are: ') % (len(attachment_list))
            for attach in attachment_list:
                group_msg = group_msg + '\n' + attach.filename
            group_msg = group_msg + '\n'  +  '. You can see top attachment menu to download attachments.'
            workorder_id.sudo().message_post(body=group_msg,message_type='comment')
        values = {
            'order':workorder_id
        }
        return request.render('website_job_workorder_request.custom_wo_website_thanks_mail_send', values)

    @http.route(['/my/custom_wo_joborders', '/my/custom_wo_joborders/page/<int:page>'], type='http', auth="user", website=True)
    def custom_wo_my_joborders(self, page=1, date_begin=None, date_end=None, joborder=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        pager = request.website.pager(
            url="/my/custom_wo_joborders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=values['custom_wo_joborder_count'],
            page=page,
            step=self._items_per_page
        )
        domain = [('custom_wo_job_partner_id','=', partner.id)]
        custom_wo_job_order_ids = request.env['project.task'].sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'sortby': sortby,
            'custom_wo_job_orders': custom_wo_job_order_ids,
            'page_name': 'custom_wo_portal_joborder',
            'default_url': '/my/custom_wo_joborders',
            'pager': pager
        })
        #return request.render("job_workorder_website_request.my_portal_job_order", values)
        return request.render("website_job_workorder_request.custom_wo_my_portal_job_order", values)
        
    @http.route(['/my/custom_wo_joborder/<int:custom_wo_joborder>'], type='http', auth="user", website=True)
    def custom_wo_joborder_print(self, custom_wo_joborder, access_token=None, **kw):
        #if request.env['res.users'].browse(request.session.uid).user_has_groups('odoo_portal_payslip_employee.group_employee_payslip'):
        # print report as sudo, since it require access to taxes, payment term, ... and portal
        # does not have those access rights.
        pdf, _ = request.env.ref('website_job_workorder_request.custom_wo_joborder_report').sudo().render_qweb_pdf([custom_wo_joborder])
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
