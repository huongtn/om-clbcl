# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubPartnerProduct(models.Model):
    _name = "clbcl.club.partner.product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Club partner product"

    product_id = fields.Many2one("product.product", string='Product')
    club_id = fields.Many2one("clbcl.club", string='Club')
    partner_id = fields.Many2one("res.partner", string='Customer')
    qty = fields.Float(string='Qty', tracking=True)
    variants = fields.Text(string='Variants')
    # product_template_id = fields.Integer(string='Product template', related='product_id.product_tmpl_id', tracking=True, store=True)
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', store=True)













