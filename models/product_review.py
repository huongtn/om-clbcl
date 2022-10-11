# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from random import randint, randrange
import datetime
from datetime import timedelta


class CLBCLProductReview(models.Model):
    _name = "clbcl.product.review"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL product review"
    product_id = fields.Many2one("product.product", string='Product')
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', store=True)
    partner_id = fields.Many2one("res.partner", string='Customer')
    star = fields.Integer(string='Start', tracking=True)
    comment = fields.Text(string='Variants')
