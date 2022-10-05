# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
from random import randint, randrange
import datetime
from datetime import timedelta
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class CLBCLController(http.Controller):

    @http.route('/createotp', type='json', auth='public', methods=['POST'])
    def createotp(self, **rec):
        self.search([('phone_number', '=', rec['phone_number'])]).unlink()
        request.env['clbcl.user.otp'].create({
            'otp': "{}".format(randint(100000, 999999)),
            'expired_at': datetime.datetime.now() + timedelta(minutes=2),
            'phone_number': rec['phone_number']
        })

        # send otp here
        return {'status': 200, 'response': 'Sent OTP', 'message': 'Success'}

    @http.route('/setpasss', type='json', auth='public', methods=['POST'])
    def setpasss(self, **rec):
        old_record = request.env['res.users'].search(
            [('login', '=', rec['phone_number'])])

        # old_record.write({
        #     'password': rec['password']
        # })
        return {'status': 200, 'response': old_record.login, 'message': 'Success'}

    @http.route('/signup', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def signUp(self, **rec):

        user = request.env['res.users'].create({
            'name': rec['phone_number'],
            'login': rec['phone_number'],
            'password': rec['password']
        })
        request.env['clbcl.user.otp'].create({
            'otp': "{}".format(randint(100000, 999999)),
            'expired_at': datetime.datetime.now() + timedelta(minutes=2),
            'phone_number': rec['phone_number']
        })
        # send otp here
        return {'status': 200, 'response': user.login, 'message': 'Success'}

    @http.route('/verifyOTP', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def verifyOTP(self, **rec):
        otp = request.env['clbcl.user.otp'].search([
            ('phone_number', '=', rec['phone_number']),
            ('otp', '=', rec['otp'])
        ])
        if otp.id:
            request.env['clbcl.user.otp'].search([('phone_number', '=', rec['phone_number'])]).unlink()
            return {'status': 200, 'message': 'OTP hợp lệ'}
        else:
            return {'status': 400, 'message': 'OTP không hợp lệ'}

   
