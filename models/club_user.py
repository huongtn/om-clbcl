# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ClubUser(models.Model):
    _inherit = "res.users"
    club_id = fields.Many2one("clbcl.club", string='Club')

