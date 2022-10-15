# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLCSendGift(models.Model):
    _name = "clbcl.send.gift.product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Move product"
    send_gift_id = fields.Many2one("clbcl.send.gift", string='Gift ID')
    product_id = fields.Many2one("product.product", string='Product')
    qty = fields.Float(string='Qty', tracking=True)
