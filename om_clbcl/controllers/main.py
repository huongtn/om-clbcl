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
        rec['expired_at'] = datetime.datetime.now() + timedelta(minutes=2)
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

    @http.route('/verifyVoucher', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def verifyVoucher(self, **rec):
        voucher = request.env['clbcl.voucher'].search([
            ('code', '=', rec['code']),
            ('to_date', '>=', datetime.datetime.now()),
            ('min_amount', '<=',  rec['order_amount'])
                                                          ])
        if voucher.id:
            if voucher.type == 'amount':
                return {'status': 200, 'discount_amount': voucher.discount, 'message': 'Mã khuyễn mãi hợp lệ'}
            else:
                return {'status': 200, 'discount_amount': max(voucher.discount * rec['order_amount']/100, voucher.max_discount), 'message': 'Mã khuyễn mãi hợp lệ'}
        else:
            return {'status': 400,  'message': 'Mã khuyễn mãi không hợp lệ'}

    @http.route('/createBooking', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def createBooking(self, **rec):
        clubBooking = request.env['clbcl.club.booking'].create({
            'club_id': rec['club_id'],
            'partner_id': rec['partner_id'],
            'date_time': rec['date_time'],
            'table': rec['table'],
            'participant_count': rec['participant_count']
        })
        if clubBooking.id:
            for friend in rec['friends']:
                request.env['clbcl.club.booking.friend'].create({
                    'booking_id': clubBooking.id,
                    'friend_id': friend
                })
            for product in rec['products']:
                request.env['clbcl.club.booking.product'].create({
                    'booking_id': clubBooking.id,
                    'product_id': product[0],
                    'qty': product[1]
                })
        return {'status': 200, 'message': 'Thêm mới thành công'}