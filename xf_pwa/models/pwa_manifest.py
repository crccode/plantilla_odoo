# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PWAManifest(models.Model):
    _name = 'pwa.manifest'
    _description = 'PWA Manifest'
    _order = 'sequence asc'

    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

    name = fields.Char(
        string='Name',
        required=True,
        help='''
        A string that represents the name of the web application 
        as it is usually displayed to the user
        '''
    )
    short_name = fields.Char(
        string='Short Name',
        required=True,
        help='''
        A string that represents the name of the web application 
        displayed to the user if there is not enough space to display name
        '''
    )
    description = fields.Char(
        string='Description',
        help='''
        A string in which developers can explain what the application does
        '''
    )
    scope = fields.Char(
        string='Scope',
        required=True,
        default='/',
        help='''
        The navigation scope of this web application. 
        If the user navigates outside the scope, 
        it reverts to a normal web page inside a browser tab or window.
        '''
    )
    start_url = fields.Char(
        string='Start URL',
        default='/web',
        required=True,
        help='''
        The start URL of the web application - 
        the preferred URL that should be loaded when the user launches the web application
        '''
    )
    display = fields.Selection(
        string='Display Mode',
        selection=[
            ('fullscreen', 'fullscreen'),
            ('standalone', 'standalone'),
            ('minimal-ui', 'minimal-ui'),
            ('browser', 'browser')
        ],
        default='standalone',
        required=True,
        help='''
        Preferred display mode for the website
        '''
    )
    orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('any', 'any'),
            ('natural', 'natural'),
            ('landscape', 'landscape'),
            ('landscape-primary', 'landscape-primary'),
            ('landscape-secondary', 'landscape-secondary'),
            ('portrait', 'portrait'),
            ('portrait-primary', 'portrait-primary'),
            ('portrait-secondary', 'portrait-secondary'),
        ],
        default='portrait-primary',
        required=True,
    )
    categories = fields.Many2many(
        string='Categories',
        comodel_name='pwa.category',
        relation='pwa_manifest_categories',
        column1='pwa_manifest_id',
        column2='pwa_category_id',
        help='''
        The names of categories that the application supposedly belongs to
        '''
    )
    background_color = fields.Char(
        string='Background Color',
        default='#FFFFFF',
        required=True,
        help='''
        A placeholder background color for the application page to display before its stylesheet is loaded
        '''
    )
    theme_color = fields.Char(
        string='Theme Color',
        default='#0D3858',
        required=True,
        help='''
        The default theme color for the application. This sometimes affects how the OS displays the site
        '''
    )
    icons = fields.One2many(
        string='Icons',
        comodel_name='pwa.icon',
        inverse_name='pwa_manifest_id',
    )


class PWACategory(models.Model):
    _name = 'pwa.category'
    _description = 'PWA Category'
    name = fields.Char(
        string='Name',
        required=True,
    )


class PWAIcon(models.Model):
    _name = 'pwa.icon'
    _description = 'PWA Icon'

    available_purposes = ('monochrome', 'maskable', 'any')

    pwa_manifest_id = fields.Many2one(
        string='PWA Manifest',
        comodel_name='pwa.manifest',
        required=True,
        ondelete='cascade',
    )
    image = fields.Image(
        string='Icon Image',
    )
    sizes = fields.Char(
        string='Sizes',
        help='''
        A string containing space-separated image dimensions.
        For example: 48x48 72x72 96x96 128x128 144x144 152x152 192x192 and so on
        '''
    )
    type = fields.Char(
        string='Type',
        help='''
        A hint as to the media type of the image.
        For example: image/png, image/webp and so on.
        The purpose of this member is to allow a user agent to quickly ignore 
        images with media types it does not support.
        '''
    )
    purpose = fields.Char(
        string='Purpose',
        default='any',
        help='''
        can have one or more of the following values, separated by spaces: monochrome maskable any
        '''
    )
    url = fields.Char(
        string='URL',
        compute='_compute_url'
    )

    def _compute_url(self):
        for icon in self:
            icon.url = '/web/image/{}/{}/image'.format(self._name, icon.id)

    @api.constrains('purpose')
    def _check_purpose(self):
        for icon in self:
            purpose_parts = icon.purpose.split()
            for purpose in purpose_parts:
                if purpose not in self.available_purposes:
                    raise ValidationError(
                        _('Purpose can have one or more of the following values, separated by spaces: %s') % (' '.join(self.available_purposes),)
                    )
