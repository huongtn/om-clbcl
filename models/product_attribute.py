# -*- coding: utf-8 -*-

from odoo import  fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    image_128 = fields.Image(string="Image")
    is_filter = fields.Boolean(string="Filter", default=True)