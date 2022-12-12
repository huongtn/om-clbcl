# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"
    image_128_active = fields.Image(string="Image Active")
