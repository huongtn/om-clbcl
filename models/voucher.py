# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubPartnerProduct(models.Model):
    _name = "clbcl.voucher"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Voucher"

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    title = fields.Text(string="Title")
    description = fields.Text(string="Description")
    code = fields.Text(string='Code')
    discount = fields.Integer(string='Discount')
    count = fields.Integer(string='Count')
    remain_count = fields.Integer(string='Remain Count', compute='_compute_remain_count')
    min_amount = fields.Integer(string='Min Amount')
    max_discount = fields.Integer(string='Max Discount')
    type = fields.Selection([
        ('amount', 'Số tiền'),
        ('percentage', '%')
    ], required=True, default='amount', tracking=True)

    def _compute_remain_count(self):
        for rec in self:
            remain_count = rec.count - self.env['sale.order'].search_count([('voucher_id', '=', rec.id)])
            rec.remain_count = remain_count
