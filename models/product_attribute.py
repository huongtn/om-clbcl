# -*- coding: utf-8 -*-

from odoo import  fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    image_128 = fields.Image(string="Image")
