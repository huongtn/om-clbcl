# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubMoveProduct(models.Model):
    _name = "clbcl.club.move"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Move"
    from_club_id = fields.Many2one("clbcl.club", string='From Club')
    to_club_id = fields.Many2one("clbcl.club", string='To Club')
    partner_id = fields.Many2one("res.partner", string='Customer')
