# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    club_id = fields.Many2one("clbcl.club", string='Club')

    @api.model_create_multi
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        for rec in res:
            order_lines = self.env['sale.order.line'].search([('order_id', '=', rec.id)])
            for order_line in order_lines:
                old_record = self.env['clbcl.club.partner.product'].search(
                    [('product_id', '=', order_line.product_id.id)
                        , ('partner_id', '=', rec.partner_id.id)
                        , ('club_id', '=', rec.club_id.id)])
                if old_record.id:
                    old_record.write({
                        'qty': old_record.qty + order_line.product_uom_qty
                    })
                else:
                    self.env['clbcl.club.partner.product'].create({
                        'product_id': order_line.product_id.id,
                        'partner_id': rec.partner_id.id,
                        'club_id': rec.club_id.id,
                        'qty': order_line.product_uom_qty,
                        'variants': ""
                    })
        return res

    def write(self, values):
        # if self.ids:
        #     customers = self.filtered(lambda record: record.customer_rank)
        #     if len(customers) > 0:
        #         self.env['customer.index'].create({'updated': ','.join([str(x) for x in customers.ids])})
        return super(SaleOrder, self).write(values)
