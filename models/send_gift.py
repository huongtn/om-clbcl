# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLCSendGift(models.Model):
    _name = "clbcl.send.gift"
    _description = "CLBCL Send gift"
    club_id = fields.Many2one("clbcl.club", string='Club')
    partner_id = fields.Many2one("res.partner", string='Customer')
    to_partner_id = fields.Many2one("res.partner", string='To Customer')
    first_product_id = fields.Integer(string="First Product ID")
    status = fields.Selection([
        ('Đã nhận', 'Đã nhận'),
        ('Đang gửi', 'Đang gửi'),
        ('Đã thu hồi', 'Đã thu hồi')
    ], required=True, default='Đang gửi', tracking=True)
