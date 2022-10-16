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
    def create_otp(self, **rec):
        self.search([('phone_number', '=', rec['phone_number'])]).unlink()
        request.env['clbcl.user.otp'].create({
            'otp': "{}".format(randint(100000, 999999)),
            'expired_at': datetime.datetime.now() + timedelta(minutes=2),
            'phone_number': rec['phone_number']
        })

        # send otp here
        return {'status': 200, 'response': 'Sent OTP', 'message': 'Success'}

    @http.route('/setpasss', type='json', auth='public', methods=['POST'])
    def set_passs(self, **rec):
        old_record = request.env['res.users'].search(
            [('login', '=', rec['phone_number'])])

        old_record.write({
            'password': rec['password']
        })
        return {'status': 200, 'response': old_record.login, 'message': 'Success'}

    @http.route('/signup', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def sign_up(self, **rec):

        user = request.env['res.users'].create({
            'name': rec['phone_number'],
            'login': rec['phone_number'],
            'password': rec['password'],
            'active': False
        })
        request.env['clbcl.user.otp'].create({
            'otp': "{}".format(randint(100000, 999999)),
            'expired_at': datetime.datetime.now() + timedelta(minutes=2),
            'phone_number': rec['phone_number']
        })
        # send otp here
        return {'status': 200, 'response': user.login, 'message': 'Success'}

    @http.route('/verifyOTP', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def verify_otp(self, **rec):
        otp = request.env['clbcl.user.otp'].search([
            ('phone_number', '=', rec['phone_number']),
            ('otp', '=', rec['otp'])
        ])
        if otp.id:
            request.env['clbcl.user.otp'].search([('phone_number', '=', rec['phone_number'])]).unlink()
            user = request.env['res.users'].search([('login', '=', rec['phone_number']),
                                                    ('active', '=', False)])
            if user.id:
                user.write({
                    'active': True
                })

            return {'status': 200, 'message': 'OTP hợp lệ'}
        else:
            return {'status': 400, 'message': 'OTP không hợp lệ'}

    @http.route('/verifyVoucher', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def verify_voucher(self, **rec):
        voucher = request.env['clbcl.voucher'].search([
            ('code', '=', rec['code']),
            ('to_date', '>=', datetime.datetime.now()),
            ('min_amount', '<=', rec['order_amount'])
        ])
        if voucher.id:
            if voucher.type == 'amount':
                return {'status': 200, 'discount_amount': voucher.discount, 'message': 'Mã khuyễn mãi hợp lệ'}
            else:
                return {'status': 200,
                        'discount_amount': max(voucher.discount * rec['order_amount'] / 100, voucher.max_discount),
                        'message': 'Mã khuyễn mãi hợp lệ'}
        else:
            return {'status': 400, 'message': 'Mã khuyễn mãi không hợp lệ'}

    @http.route('/createBooking', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def create_booking(self, **rec):
        clubBooking = request.env['clbcl.club.booking'].create({
            'club_id': rec['club_id'],
            'partner_id': rec['partner_id'],
            'date_time': rec['date_time'],
            'table': rec['table'],
            'participant_count': rec['participant_count']
        })
        if clubBooking.id:
            for friend in rec['friends']:
                friendInfo = request.env['clbcl.friend'].search([('id', '=', friend)])
                request.env['clbcl.club.booking.friend'].create({
                    'booking_id': clubBooking.id,
                    'friend_id': friend,
                    'phone': friendInfo.phone
                })
            for product in rec['products']:
                request.env['clbcl.club.booking.product'].create({
                    'booking_id': clubBooking.id,
                    'product_id': product[0],
                    'qty': product[1]
                })
        return {'status': 200, 'message': 'Thêm mới thành công'}

    @http.route('/getBookings', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_bookings(self, **rec):
        myBookings = request.env['clbcl.club.booking'].search_read([('partner_id', '=', rec['partner_id'])])
        friendBookings = []
        user = request.env['res.users'].search([('partner_id', '=', rec['partner_id'])])
        friends = request.env['clbcl.club.booking.friend'].search([('phone', '=', user.login)])
        for friend in friends:
            bookings = request.env['clbcl.club.booking'].search_read([('id', '=', friend.booking_id.id)])
            for booking in bookings:
                friendBookings.append(booking)

        return {'status': 200, 'myBookings': myBookings, 'friendBookings': friendBookings}

    @http.route('/getBookingById', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_booking_byid(self, **rec):
        booking = request.env['clbcl.club.booking'].search_read([('id', '=', rec['id'])])
        products = request.env['clbcl.club.booking.product'].search_read([('booking_id', '=', rec['id'])])
        friends = request.env['clbcl.club.booking.friend'].search_read([('booking_id', '=', rec['id'])])
        return {'status': 200, 'booking': booking[0], 'products': products, 'friends': friends}

    @http.route('/createMoveProducts', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def create_move_products(self, **rec):
        clubMove = request.env['clbcl.club.move'].create({
            'from_club_id': rec['from_club_id'],
            'to_club_id': rec['to_club_id'],
            'partner_id': rec['partner_id']
        })
        if clubMove.id:
            for product in rec['products']:
                request.env['clbcl.club.move.product'].create({
                    'move_id': clubMove.id,
                    'product_id': product[0],
                    'qty': product[1]
                })
                from_old_record = request.env['clbcl.club.partner.product'].search(
                    [('product_id', '=', product[0])
                        , ('partner_id', '=', rec['partner_id'])
                        , ('club_id', '=', rec['from_club_id'])
                        , ('is_empty', '=', False)])
                if from_old_record.id:
                    if from_old_record.qty < product[1]:
                        return {'status': 400, 'message': 'Số lượng sản phẩm không đủ'}
                    else:
                        from_old_record.write({
                            'qty': from_old_record.qty - product[1]
                        })
                        to_old_record = request.env['clbcl.club.partner.product'].search(
                            [('product_id', '=', product[0])
                                , ('partner_id', '=', rec['partner_id'])
                                , ('club_id', '=', rec['to_club_id'])
                                , ('is_empty', '=', False)])
                        if to_old_record.id:
                            to_old_record.write({
                                'qty': to_old_record.qty + product[1]
                            })
                        else:
                            request.env['clbcl.club.partner.product'].create({
                                'product_id': product[0],
                                'partner_id': rec['partner_id'],
                                'club_id': rec['to_club_id'],
                                'qty': product[1],
                                'is_empty': False,
                                'variants': ""
                            })
                else:
                    return {'status': 400, 'message': 'Số lượng sản phẩm không đủ'}
            return {'status': 200, 'message': 'Thêm mới thành công'}

    @http.route('/getMyBookmarks', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_bookmarks(self, **rec):
        myBookmarks = request.env['clbcl.product.bookmark'].search_read([('partner_id', '=', rec['partner_id'])])
        productIds = []
        for myBookmark in myBookmarks:
            productIds.append(myBookmark['product_id'][0])

        return {'status': 200, 'productIds': productIds}

    @http.route('/addBookmark', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def add_bookmark(self, **rec):
        request.env['clbcl.product.bookmark'].search([('partner_id', '=', rec['partner_id']),
                                                      ('product_id', '=', rec['product_id'])]).unlink()
        request.env['clbcl.product.bookmark'].create({
            'partner_id': rec['partner_id'],
            'product_id': rec['product_id']
        })
        return {'status': 200, 'message': 'added successful'}

    @http.route('/removeBookmark', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def remove_bookmark(self, **rec):
        request.env['clbcl.product.bookmark'].search([('partner_id', '=', rec['partner_id']),
                                                      ('product_id', '=', rec['product_id'])]).unlink()
        return {'status': 200, 'message': 'removed successful'}

    @http.route('/getMyPoints', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_points(self, **rec):
        return {'status': 200,
                'points': request.env['clbcl.point'].search_read([('partner_id', '=', rec['partner_id'])])}

    @http.route('/addPoint', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def add_point(self, **rec):
        request.env['clbcl.point'].create({
            'point': rec['point'],
            'partner_id': rec['partner_id'],
        })
        return {'status': 200, 'message': 'ok'}

    @http.route('/getproductsbyclub', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_products_byclub(self, **rec):
        stocks = request.env['clbcl.club.partner.product'].search_read([('partner_id', '=', rec['partner_id']),
                                                                        ('club_id', '=', rec['club_id']),
                                                                        ('is_empty', '=', False),
                                                                        ('qty', '>', 0)
                                                                        ])
        products = {
            'foods': [],
            'wines': []
        }
        for stock in stocks:
            product = request.env['product.product'].search_read([('id', '=', stock['product_id'][0])])
            productDetails = {
                'product': {
                    'id': product[0]['id'],
                    'name': product[0]['name'],
                    'description': product[0]['description'],
                    'display_name': product[0]['display_name'],
                    'categ_id': product[0]['categ_id'],
                    'list_price': product[0]['list_price'],
                    'lst_price': product[0]['lst_price'],
                    'tax_string': product[0]['tax_string'],
                    'taxes_id': product[0]['taxes_id'],
                    'standard_price': product[0]['standard_price'],
                    'star': product[0]['star'],
                    'review_count': product[0]['review_count'],
                    'light_bold': product[0]['light_bold'],
                    'smooth_tannic': product[0]['smooth_tannic'],
                    'dry_sweet': product[0]['dry_sweet'],
                    'soft_acidic': product[0]['soft_acidic'],
                    'product_template_variant_value_ids': product[0]['product_template_variant_value_ids']
                },
                'qty': stock['qty']
            }
            if 'Đồ ăn' in productDetails['product']['categ_id'][1]:
                products['foods'].append(productDetails)
            else:
                products['wines'].append(productDetails)
        return {'status': 200, 'products': products}

    @http.route('/getMyFriends', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_friends(self, **rec):
        user = request.env['res.users'].search([('partner_id', '=', rec['partner_id'])])
        sendingFriends = request.env['clbcl.friend'].search_read([('partner_id', '=', rec['partner_id'])])
        receivingFriends = request.env['clbcl.friend'].search_read([('phone', '=', user.login)])
        myFriends = {
            'friends': [],
            'sendingFriends': [],
            'receivingFriends': []
        }
        for friend in sendingFriends:
            if friend['status'] == 'Đồng ý':
                myFriends['friends'].append(friend)
            else:
                myFriends['sendingFriends'].append(friend)

        for friend in receivingFriends:
            if friend['status'] == 'Đồng ý':
                myFriends['friends'].append(friend)
            else:
                myFriends['receivingFriends'].append(friend)
        return {'status': 200, 'myFriends': myFriends}

    @http.route('/getMyGifts', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_gift(self, **rec):
        sending_gifts = request.env['clbcl.send.gift'].search_read([('partner_id', '=', rec['partner_id'])])
        receiving_gifts = request.env['clbcl.send.gift'].search_read([('to_partner_id', '=', rec['partner_id'])])
        my_gifts = {
            'gifts': [],
            'sending_gifts': [],
            'receiving_gift': []
        }
        for gift in sending_gifts:
            if gift['status'] == 'Đã nhận':
                my_gifts['gifts'].append(gift)
            else:
                my_gifts['sending_gifts'].append(gift)

        for gift in receiving_gifts:
            if gift['status'] == 'Đã nhận':
                my_gifts['gifts'].append(gift)
            else:
                my_gifts['receiving_gift'].append(gift)
        return {'status': 200, 'my_gifts': my_gifts}

    @http.route('/createSendGift', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def create_send_gift(self, **rec):
        send_gift = request.env['clbcl.send.gift'].create({
            'club_id': rec['club_id'],
            'partner_id': rec['partner_id'],
            'to_partner_id': rec['to_partner_id'],
            'first_product_id': rec['products'][0][0]
        })
        if send_gift.id:
            for product in rec['products']:
                request.env['clbcl.send.gift.product'].create({
                    'send_gift_id': send_gift.id,
                    'product_id': product[0],
                    'qty': product[1]
                })
        return {'status': 200, 'message': 'Thêm mới thành công'}

    @http.route('/acceptSendGift', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def accept_send_gift(self, **rec):
        for send_gift_id in rec['send_gift_id']:
            send_gifts = request.env['clbcl.send.gift'].search_read([('id', '=', send_gift_id)])
            for send_gift in send_gifts:
                products = request.env['clbcl.send.gift.product'].search_read([('send_gift_id', '=', 1)])
                for product in products:
                    from_old_record = request.env['clbcl.club.partner.product'].search_read(
                        [('product_id', '=', product['product_id'][0])
                            , ('partner_id', '=', send_gift['partner_id'][0])
                            , ('club_id', '=', send_gift['club_id'][0])
                            , ('is_empty', '=', False)])
                    if from_old_record.id:
                        if from_old_record.qty < product['qty']:
                            return {'status': 400, 'message': 'Số lượng sản phẩm không đủ'}
                        else:
                            from_old_record.write({
                                'qty': from_old_record.qty - product['qty']
                            })
                            to_record = request.env['clbcl.club.partner.product'].search_read(
                                [('product_id', '=', product['product_id'][0])
                                    , ('partner_id', '=', send_gift['to_partner_id'][0])
                                    , ('club_id', '=', send_gift['club_id'][0])
                                    , ('is_empty', '=', False)])
                            if to_record.id:
                                to_record.write({
                                    'qty': to_record.qty + product['qty']
                                })
                            else:
                                request.env['clbcl.club.partner.product'].create({
                                    'product_id': product['product_id'][0],
                                    'partner_id': send_gift['to_partner_id'][0],
                                    'club_id': send_gift['club_id'][0],
                                    'qty': product['qty'],
                                    'is_empty': False,
                                    'variants': ""
                                })
                    else:
                        return {'status': 400, 'message': 'Số lượng sản phẩm không đủ'}

                send_gift.write({
                        'status': 'Đã nhận'
                })

        return {'status': 200, 'message': 'Cập nhật thành công'}
