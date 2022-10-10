# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubMoveProductItem(models.Model):
    _name = "clbcl.club.move.product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Move product"
    move_id = fields.Many2one("clbcl.club.move", string='Move ID')
    product_id = fields.Many2one("product.product", string='Product')
    qty = fields.Float(string='Qty', tracking=True)










