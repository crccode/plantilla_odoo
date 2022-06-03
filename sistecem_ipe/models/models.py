# -*- coding: utf-8 -*-

from odoo import api, fields, models



class Lead(models.Model):
    _inherit = 'crm.lead'

    nombre_completo_propuesta = fields.Char(string='Nombre Completo de propuesta')
    monto_en_dolares = fields.Monetary('Valor en Dolares', currency_field='secondary_currency', tracking=True, compute="_compute_monto_en_dolares")
    moneda_de_oferta = fields.Boolean(string="Propuesta en Dolares")
    secondary_currency = fields.Many2one("res.currency", string='Moneda secundaria', compute='_secondary_currency')

    codigo_de_entidad = fields.Char(string='Codigo de entidad contratante')
    solicitud_boleta = fields.Boolean(string='Solicitud de Boleta')
    tipo_de_contrato = fields.Selection(
    [('marco', 'Contrato Marco'),
     ('oservicio', 'Orden de Servicio'),
    ('standard', 'Contrato Estándar'),
     ('ocambio', 'Contrato Orden de Cambio')],string='Tipo de Contrato')
    boleta_garantia = fields.Many2one('sistecem.boleta', string="Boleta de Garantía")
    moneda_boleta = fields.Many2one('res.currency', string='Moneda de Boleta')
    monto_boleta_bs = fields.Float(string='Monto de Boleta Bs')
    monto_boleta_dolar = fields.Float(string='Monto de Boleta $us')

    metodo_seleccion = fields.Selection(
    [('bajo', 'Precio Evaluado más bajo'),
    ('calidad', 'Calidad Técnica Costo'),
     ('fijo', 'Presupuesto Fijo'),
     ('indef', 'Indefinido')],string='Método de Seleccion')

    tipo_invitacion = fields.Selection(
        [('directa', 'Invitación Directa'),
         ('publica', 'Licitación Pública'),
         ('corta', 'Lista Corta'),
         ('marcos', 'Contrato Marco'),
         ('indef', 'Indefinido')], string='Tipo de Invitación')

    date_deadline = fields.Date('Validez de propuesta', help="Fecha de cierre")

    @api.depends('expected_revenue','create_date')
    def _compute_monto_en_dolares(self):
        currency = self.company_currency
         # = [monedaActual]._convert(
        # [monto] , [moneda a transformar] , [ compañia] , [fecha_de_calculo de  tasa ]
        # )
        self.monto_en_dolares = currency._convert(
            self.expected_revenue,
            self.secondary_currency,
            self.company_id,
            self.create_date or fields.Date.context_today(self),
        )

    def _secondary_currency(self):
        self.secondary_currency=  self.env['res.currency'].search([('name', '=', 'USD')])

