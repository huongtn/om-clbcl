# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    image_128_background = fields.Image(string="Background Image")
    review_count = fields.Integer(string='Review Count', compute='_compute_review_count')
    star = fields.Float(string='Star', compute='_compute_star')

    def _compute_review_count(self):
        for rec in self:
            review_count = self.env['clbcl.product.review'].search_count([('product_tmpl_id', '=', rec.id)])
            rec.review_count = review_count

    def _compute_star(self):
        for rec in self:
            if rec.review_count <= 0:
                rec.star = 0
            else:
                star = 0
                reviews = self.env['clbcl.product.review'].search([('product_tmpl_id', '=', rec.id)])
                for review in reviews:
                    star += review.star
                rec.star = star / rec.review_count
