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
    password = fields.Text(string='password')
    expired_at = fields.Datetime(string='ExpiredAt')

    @api.model
    def create(self, values):
        if values['password']:
            user = self.env['res.users'].create({
                'name': values['phone_number'],
                'login': values['phone_number'],
                'password': values['password']
            })

        self.search([('phone_number', '=', values['phone_number'])]).unlink()
        values['otp'] = "{}".format(randint(100000, 999999))
        values['expired_at'] = datetime.datetime.now() + timedelta(minutes=2)
        res = super(CLBCLUserOtp, self).create(values)
        # send otp here
        return res














