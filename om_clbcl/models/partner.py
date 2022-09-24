# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    user_id = fields.Many2one("res.users", string='User for login')


