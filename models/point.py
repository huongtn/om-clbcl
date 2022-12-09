# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLPoint(models.Model):
    _name = "clbcl.point"
    _description = "CLBCL Point"
    partner_id = fields.Many2one("res.partner", string='My')
    order_id = fields.Many2one("sale.order", string='Order')
    description = fields.Text(string='Description')
    point = fields.Integer(string='Point')
