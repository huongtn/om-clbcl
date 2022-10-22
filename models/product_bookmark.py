# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubMoveProduct(models.Model):
    _name = "clbcl.product.bookmark"
    _description = "CLBCL Product Bookmark"
    product_id = fields.Many2one("product.product", string='Product')
    partner_id = fields.Many2one("res.partner", string='Customer')
