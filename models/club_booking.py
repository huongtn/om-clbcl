# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubBooking(models.Model):
    _name = "clbcl.club.booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Club booking"

    club_id = fields.Many2one("clbcl.club", string='Club')
    partner_id = fields.Many2one("res.partner", string='Customer')
    date_time = fields.Datetime(string='Date time')
    table = fields.Text(string='Table')
    participant_count = fields.Integer(string='Participant Count')
    status = fields.Text(string='Status')
