# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubFriend(models.Model):
    _name = "clbcl.friend"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Friend"
    partner_id = fields.Many2one("res.partner", string='My')
    friend_partner_id = fields.Many2one("res.partner", string='Friend Partner', compute='_compute_friend_partner_id')
    name = fields.Text(string="Name")
    phone = fields.Text(string="Phone")

    def _compute_friend_partner_id(self):
        for rec in self:
            users = self.env['res.users'].search([('login', '=', rec.phone)])
            if users.id: 
                for user in users:
                    rec.friend_partner_id = user.partner_id.id














