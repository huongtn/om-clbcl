# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from random import randint, randrange
import datetime
from datetime import timedelta



class CLBCLUserOtp(models.Model):
    _name = "clbcl.user.otp"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL user otp"

    phone_number = fields.Text(string='Phone Number')
    otp = fields.Text(string='OTP')
    expired_at = fields.Datetime(string='ExpiredAt')

    @api.model
    def create(self, values):
        self.search([('phone_number', '=', values['phone_number'])]).unlink()
        values['otp'] = "{}".format(randint(100000, 999999))
        values['expired_at'] = datetime.datetime.now() + timedelta(minutes=2)
        res = super(CLBCLUserOtp, self).create(values)
        return res














