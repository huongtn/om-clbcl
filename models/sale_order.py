# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"
    club_id = fields.Many2one("clbcl.club", string='Club')
    first_product_template_id = fields.Integer(string="First Product Tempate ID")
    voucher_id = fields.Many2one("clbcl.voucher", string='Voucher')
    voucher_discount = fields.Integer(string="Voucher Discount")
    clbcl_status = fields.Selection([
        ('Chờ lấy hàng', 'Chờ lấy hàng'),
        ('Đang giao', 'Đang giao'),
        ('Đã hủy', 'Đã hủy'),
        ('Hoàn thành', 'Hoàn thành')
    ], required=True, default='Chờ lấy hàng', tracking=True)
    clbcl_payment_status = fields.Selection([
        ('Chưa thanh toán', 'Chưa thanh toán'),
        ('Khách hàng thanh toán', 'Khách hàng thanh toán'),
        ('Xác nhận thanh toán', 'Xác nhận thanh toán'),
        ('Khác', 'Khác')
    ], required=True, default='Chưa thanh toán', tracking=True)
    @api.model_create_multi
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        self.env['clbcl.point'].create({
            'partner_id': res.partner_id.id,
            'order_id': res.id,
            'point': res.amount_total / 100,
            'expired_at': datetime.datetime.now() + timedelta(days=30),
        })
        if res.club_id:
            for rec in res:
                order_lines = self.env['sale.order.line'].search([('order_id', '=', rec.id)])
                for order_line in order_lines:
                    old_record = self.env['clbcl.club.partner.product'].search(
                        [('product_id', '=', order_line.product_id.id)
                            , ('partner_id', '=', rec.partner_id.id)
                            , ('club_id', '=', rec.club_id.id)
                            , ('is_empty', '=', False)])
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
                            'is_empty': False
                        })
        return res

    def write(self, values):
        # if self.ids:
        #     customers = self.filtered(lambda record: record.customer_rank)
        #     if len(customers) > 0:
        #         self.env['customer.index'].create({'updated': ','.join([str(x) for x in customers.ids])})
        return super(SaleOrder, self).write(values)
