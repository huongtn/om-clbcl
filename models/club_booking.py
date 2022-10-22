# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubBooking(models.Model):
    _name = "clbcl.club.booking"
    _description = "CLBCL Club booking"
    code = fields.Text(string='Code')
    club_id = fields.Many2one("clbcl.club", string='Club')
    partner_id = fields.Many2one("res.partner", string='Customer')
    date_time = fields.Datetime(string='Date time')
    table = fields.Text(string='Table')
    participant_count = fields.Integer(string='Participant Count')
    status = fields.Selection([
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Xác nhận', 'Xác nhận'),
        ('Hủy', 'Hủy'),
        ('Hoàn thành', 'Hoàn thành'),
    ], required=True, default='Chờ xác nhận', tracking=True)
