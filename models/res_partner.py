# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    default_partner_shipping_id = fields.Integer(string='Default Partner Shipping ID')
    province_id = fields.Many2one("clbcl.province", string='province')
    district_id = fields.Many2one("clbcl.district", string='district')
    ward_id = fields.Many2one("clbcl.ward", string='ward')
