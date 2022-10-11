# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"
    image_128 = fields.Image(string="Image")
    image_128_active = fields.Image(string="Image Active")
