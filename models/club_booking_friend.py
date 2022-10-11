# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubBookingFriend(models.Model):
    _name = "clbcl.club.booking.friend"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Club booking friend"

    booking_id = fields.Many2one("clbcl.club.booking", string='Club Booking')
    friend_id = fields.Many2one("clbcl.friend", string='Friend')
    phone = fields.Text(string='Phone Number')
    status = fields.Text(string='Status')
