# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLPoint(models.Model):
    _name = "clbcl.point"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Point"
    partner_id = fields.Many2one("res.partner", string='My')
    order_id = fields.Many2one("sale.order", string='Order')
    point = fields.Integer(string='Point')
