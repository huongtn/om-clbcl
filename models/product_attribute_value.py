# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    image = fields.Text(string='Base64 Image')