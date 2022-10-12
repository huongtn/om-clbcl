# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClub(models.Model):
    _name = "clbcl.club"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Club"
    _rec_name = 'club_name'

    club_name = fields.Char(string='Name', required=True, tracking=True)
    address = fields.Text(string='Address')
    phone = fields.Text(string='Phone')
    note = fields.Text(string='Note')
    image = fields.Binary(string="Club Image")
    active = fields.Boolean(string="Active", default=True)
    area = fields.Selection([
        ('hanoi', 'Hà nội'),
        ('hochiminh', 'Hồ chí minh'),
        ('other', 'Khác'),
    ], required=True, default='hanoi', tracking=True)

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('club_name'):
            default['club_name'] = _("%s (Copy)", self.club_name)
        default['note'] = "Copied Record"
        return super(CLBCLClub, self).copy(default)
