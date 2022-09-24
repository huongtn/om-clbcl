# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    club_id = fields.Many2one("clbcl.club", string='Club')
    # only calculate when show on view
    is_calculated = fields.Boolean(string='Calculated', compute='_compute_club_partner_product')

    def _compute_club_partner_product(self):
        for rec in self:
            print('11111')
            # order_lines = self.env['sale.order.line'].search(['order_id', '=', rec.id])
            # order_lines = self.env['sale.order.line'].search(['order_id', 'in', rec.ids])
            order_lines = self.env['sale.order.line'].search([])
            print('2222', rec.club_id)
            print('3333', rec.partner_id)
            for order_line in order_lines:
                self.env['clbcl.club.partner.product'].create({
                    'product_id': order_line.product_id,
                    'partner_id': rec.partner_id,
                    'club_id': rec.club_id[0],
                    'qty': order_line.product_uom_qty,
                    'variants': ""
                })
            rec.is_calculated = True

