# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClub(models.Model):
    _name = "clbcl.club"
    _description = "CLBCL Club"
    _rec_name = 'club_name'

    club_name = fields.Char(string='Name', required=True, tracking=True)
    address = fields.Text(string='Address')
    phone = fields.Text(string='Phone')
    note = fields.Text(string='Note')
    image = fields.Binary(string="Club Image")
    image_1 = fields.Binary(string="Club Image 1")
    image_2 = fields.Binary(string="Club Image 2")
    image_3 = fields.Binary(string="Club Image 3")
    image_4 = fields.Binary(string="Club Image 4")
    image_5 = fields.Binary(string="Club Image 5")

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
