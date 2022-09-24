# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    club_id = fields.Many2one("clbcl.club", string='Club')

