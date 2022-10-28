# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubBookingFriend(models.Model):
    _name = "clbcl.club.booking.friend"
    _description = "CLBCL Club booking friend"

    booking_id = fields.Many2one("clbcl.club.booking", string='Club Booking')
    friend_id = fields.Many2one("clbcl.friend", string='Friend')
    phone = fields.Text(string='Phone Number')
    status = fields.Selection([
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Hoàn tác gửi', 'Hoàn tác gửi'),
        ('Đã hủy gửi', 'Đã hủy gửi'),
        ('Đã được chấp nhận', 'Đã được chấp nhận'),
        ('Từ chối', 'Từ chối'),
    ], required=True, default='Chờ xác nhận', tracking=True)
