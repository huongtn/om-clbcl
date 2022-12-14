# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubPartnerProduct(models.Model):
    _name = "clbcl.club.partner.product"
    _description = "CLBCL Club partner product"

    product_id = fields.Many2one("product.product", string='Product')
    club_id = fields.Many2one("clbcl.club", string='Club')
    partner_id = fields.Many2one("res.partner", string='Customer')
    qty = fields.Float(string='Qty', tracking=True)
    is_empty = fields.Boolean(string="Chai rỗng", default=True)
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', store=True)
    categ_id = fields.Many2one('product.category', related='product_tmpl_id.categ_id', store=True)
    category = fields.Text(string="Category", default="Rượu")
