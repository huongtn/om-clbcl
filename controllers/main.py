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

    @http.route('/create_otp', type='json', auth='public', methods=['POST'])
    def create_otp(self, **rec):
        user = request.env['res.users'].search([('login', '=', rec['phone_number'])])
        if rec['forgot_password']:
            if user.id:
                print(1)
            else:
                return {'status': 400, 'message': 'SĐT không tồn tại'}
        else:
            if user.id:
                return {'status': 400, 'message': 'SĐT đã đăng ký'}
        request.env['clbcl.user.otp'].search([('phone_number', '=', rec['phone_number'])]).unlink()
        request.env['clbcl.user.otp'].create({
            'otp': "123456",
            'expired_at': datetime.datetime.now() + timedelta(minutes=2),
            'phone_number': rec['phone_number']
        })

        # send otp here
        return {'status': 200, 'response': 'Sent OTP', 'message': 'Success'}

    @http.route('/set_passs', type='json', auth='public', methods=['POST'])
    def set_passs(self, **rec):
        old_record = request.env['res.users'].search(
            [('login', '=', rec['phone_number'])])

        old_record.write({
            'password': rec['password']
        })
        return {'status': 200, 'response': old_record.login, 'message': 'Success'}

    @http.route('/sign_up', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def sign_up(self, **rec):
        old_user = request.env['res.users'].search([('login', '=', rec['phone_number'])])
        if old_user.id:
            return {'status': 400, 'message': 'SĐT đã được đăng ký'}
        else:
            user = request.env['res.users'].create({
                'name': rec['phone_number'],
                'login': rec['phone_number'],
                'password': rec['password'],
                # 'sel_groups_1_9_10': 9,
                'active': False
            })
            request.env['clbcl.user.otp'].create({
                'otp': "{}".format(randint(100000, 999999)),
                'expired_at': datetime.datetime.now() + timedelta(minutes=2),
                'phone_number': rec['phone_number']
            })
            # send otp here
            return {'status': 200, 'response': user.login, 'message': 'Success'}

    @http.route('/verify_otp', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def verify_otp(self, **rec):
        # return {'status': 200, 'message': 'OTP hợp lệ'}
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

    @http.route('/verify_voucher', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def verify_voucher(self, **rec):
        voucher = request.env['clbcl.voucher'].search([
            ('code', '=', rec['code']),
            ('partner_id', '=', rec['partner_id']),
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

    @http.route('/exchange_voucher', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def exchange_voucher(self, **rec):
        original_voucher = request.env['clbcl.voucher'].search([
            ('id', '=', rec['voucher_id']),
            ('to_date', '>=', datetime.datetime.now()),
            ('point', '=', rec['point'])
        ])
        if original_voucher.id:
            voucher = request.env['clbcl.voucher'].create({
                'title': original_voucher.title,
                'code': original_voucher.code,
                'description': 'Đổi ' + str(rec['point']) + ' điểm, ngày ' + str(datetime.datetime.now()),
                'from_date': datetime.datetime.now(),
                'count': 1,
                'point': rec['point'],
                'type': original_voucher.type,
                'discount': original_voucher.discount,
                'min_amount': original_voucher.min_amount,
                'max_discount': original_voucher.max_discount,
                'partner_id': rec['partner_id']
            })
            if voucher.id:
                voucher.write({
                    'code': original_voucher.code + ' ' + str(voucher.id).zfill(5)
                })
                request.env['clbcl.point'].create({
                    'description': 'Đổi ' + str(rec['point']) + ' điểm, voucher ' + original_voucher.code,
                    'point': (-1) * rec['point'],
                    'partner_id': rec['partner_id'],
                })
            return {'status': 200, 'message': 'Đổi voucher thành công'}
        else:
            return {'status': 400, 'message': 'Mã khuyễn mãi không hợp lệ'}

    @http.route('/create_booking', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def create_booking(self, **rec):
        clubBooking = request.env['clbcl.club.booking'].create({
            'club_id': rec['club_id'],
            'partner_id': rec['partner_id'],
            'date_time': rec['date_time'],
            'table': rec['table'],
            'participant_count': rec['participant_count']
        })
        if clubBooking.id:
            clubBooking.write({
                'code': 'B' + str(clubBooking.id).zfill(5)
            })
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

    @http.route('/edit_booking', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def edit_booking(self, **rec):
        old_booking = request.env['clbcl.club.booking'].search([('id', '=', rec['id'])])
        if old_booking.id:
            old_booking.write({
                'club_id': rec['club_id'],
                'partner_id': rec['partner_id'],
                'date_time': rec['date_time'],
                'table': rec['table'],
                'participant_count': rec['participant_count']
            })
            request.env['clbcl.club.booking.friend'].search([('booking_id', '=', old_booking.id)]).unlink()
            for friend in rec['friends']:
                friendInfo = request.env['clbcl.friend'].search([('id', '=', friend)])
                request.env['clbcl.club.booking.friend'].create({
                    'booking_id': old_booking.id,
                    'friend_id': friend,
                    'phone': friendInfo.phone
                })
            request.env['clbcl.club.booking.product'].search([('booking_id', '=', old_booking.id)]).unlink()
            for product in rec['products']:
                request.env['clbcl.club.booking.product'].create({
                    'booking_id': old_booking.id,
                    'product_id': product[0],
                    'qty': product[1]
                })
        return {'status': 200, 'message': 'Cập nhật thành công'}

    @http.route('/get_bookings', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_bookings(self, **rec):
        my_bookings = request.env['clbcl.club.booking'].search_read([('partner_id', '=', rec['partner_id'])])
        friendBookings = []
        user = request.env['res.users'].search([('partner_id', '=', rec['partner_id'])])
        friends = request.env['clbcl.club.booking.friend'].search([('phone', '=', user.login)])
        for friend in friends:
            bookings = request.env['clbcl.club.booking'].search_read([('id', '=', friend.booking_id.id)])
            for booking in bookings:
                friendBookings.append(booking)

        return {'status': 200, 'my_bookings': my_bookings, 'friend_bookings': friendBookings}

    @http.route('/get_booking_byid', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_booking_byid(self, **rec):
        booking = request.env['clbcl.club.booking'].search_read([('id', '=', rec['id'])])
        products = request.env['clbcl.club.booking.product'].search_read([('booking_id', '=', rec['id'])])
        friends = request.env['clbcl.club.booking.friend'].search_read([('booking_id', '=', rec['id'])])
        return {'status': 200, 'booking': booking[0], 'products': products, 'friends': friends}

    @http.route('/create_move_products', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
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
                                'is_empty': False
                            })
                else:
                    return {'status': 400, 'message': 'Số lượng sản phẩm không đủ'}
            return {'status': 200, 'message': 'Thêm mới thành công'}

    @http.route('/get_my_bookmarks', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_bookmarks(self, **rec):
        myBookmarks = request.env['clbcl.product.bookmark'].search_read([('partner_id', '=', rec['partner_id'])])
        productIds = []
        for myBookmark in myBookmarks:
            productIds.append(myBookmark['product_id'][0])

        return {'status': 200, 'productIds': productIds}

    @http.route('/add_bookmark', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def add_bookmark(self, **rec):
        request.env['clbcl.product.bookmark'].search([('partner_id', '=', rec['partner_id']),
                                                      ('product_id', '=', rec['product_id'])]).unlink()
        request.env['clbcl.product.bookmark'].create({
            'partner_id': rec['partner_id'],
            'product_id': rec['product_id']
        })
        return {'status': 200, 'message': 'added successful'}

    @http.route('/remove_bookmark', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def remove_bookmark(self, **rec):
        request.env['clbcl.product.bookmark'].search([('partner_id', '=', rec['partner_id']),
                                                      ('product_id', '=', rec['product_id'])]).unlink()
        return {'status': 200, 'message': 'removed successful'}

    @http.route('/get_my_points', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_points(self, **rec):
        partner = request.env['res.partner'].search([('id', '=', rec['partner_id'])])
        return {'status': 200,
                'create_date': partner[0].create_date,
                'rank': 'Hạng vàng',
                'points': request.env['clbcl.point'].search_read([('partner_id', '=', rec['partner_id'])],
                                                                 order='id desc')}

    @http.route('/add_point', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def add_point(self, **rec):
        request.env['clbcl.point'].create({
            'point': rec['point'],
            'partner_id': rec['partner_id'],
        })
        return {'status': 200, 'message': 'ok'}

    @http.route('/get_products_byclub', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
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

    @http.route('/get_products_all_clubs', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_products_all_clubs(self, **rec):
        club_products = []
        clubs = request.env['clbcl.club'].search([])
        for club in clubs:
            stocks = request.env['clbcl.club.partner.product'].search_read([('partner_id', '=', rec['partner_id']),
                                                                            ('club_id', '=', club.id),
                                                                            ('is_empty', '=', False),
                                                                            ('qty', '>', 0)
                                                                            ])
            products = {
                'id': club.id,
                'club_name': club.club_name,
                'area': club.area,
                'address': club.address,
                'phone': club.phone,
                'note': club.note,
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
            club_products.append(products)
        return {'status': 200, 'club_products': club_products}

    @http.route('/get_my_friends', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_friends(self, **rec):
        user = request.env['res.users'].search([('partner_id', '=', rec['partner_id'])])
        sending_friends = request.env['clbcl.friend'].search_read([('partner_id', '=', rec['partner_id'])])
        receiving_friends = request.env['clbcl.friend'].search_read([('phone', '=', user.login)])
        my_friends = {
            'friends': [],
            'sending_friends': [],
            'receiving_friends': []
        }
        for friend in sending_friends:
            if friend['status'] == 'Đồng ý':
                my_friends['friends'].append(friend)
            else:
                my_friends['sending_friends'].append(friend)

        for friend in receiving_friends:
            if friend['status'] == 'Đồng ý':
                my_friends['friends'].append(friend)
            else:
                my_friends['receiving_friends'].append(friend)
        return {'status': 200, 'my_friends': my_friends}

    @http.route('/get_my_gifts', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_my_gifts(self, **rec):
        sending_gifts = request.env['clbcl.send.gift'].search_read([('partner_id', '=', rec['partner_id'])])
        receiving_gifts = request.env['clbcl.send.gift'].search_read([('to_partner_id', '=', rec['partner_id'])])
        my_gifts = {
            'gifts': [],
            'sending_gifts': [],
            'receiving_gift': []
        }
        for gift in sending_gifts:
            my_gifts['sending_gifts'].append(gift)
            if gift['status'] == 'Đã nhận':
                my_gifts['gifts'].append(gift)

        for gift in receiving_gifts:
            my_gifts['receiving_gift'].append(gift)
            if gift['status'] == 'Đã nhận':
                my_gifts['gifts'].append(gift)
        return {'status': 200, 'my_gifts': my_gifts}

    @http.route('/create_send_gift', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def create_send_gift(self, **rec):
        for club in rec['clubs']:
            send_gift = request.env['clbcl.send.gift'].create({
                'club_id': club['club_id'],
                'partner_id': rec['partner_id'],
                'to_partner_id': rec['to_partner_id'],
                'first_product_id': club['products'][0][0]
            })
            if send_gift.id:
                send_gift.write({
                    'code': 'GI' + str(send_gift.id).zfill(5)
                })
                for product in club['products']:
                    request.env['clbcl.send.gift.product'].create({
                        'send_gift_id': send_gift.id,
                        'product_id': product[0],
                        'qty': product[1]
                    })
        return {'status': 200, 'message': 'Thêm mới thành công'}

    @http.route('/accept_send_gift', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def accept_send_gift(self, **rec):
        for send_gift_id in rec['send_gift_id']:
            send_gifts = request.env['clbcl.send.gift'].search([('id', '=', send_gift_id)])
            for send_gift in send_gifts:
                products = request.env['clbcl.send.gift.product'].search_read([('send_gift_id', '=', 1)])
                for product in products:
                    from_old_record = request.env['clbcl.club.partner.product'].search(
                        [('product_id', '=', product['product_id'][0])
                            , ('partner_id', '=', send_gift.partner_id.id)
                            , ('club_id', '=', send_gift.club_id.id)
                            , ('is_empty', '=', False)])
                    if from_old_record.id:
                        if from_old_record.qty < product['qty']:
                            return {'status': 400, 'message': 'Số lượng sản phẩm không đủ'}
                        else:
                            from_old_record.write({
                                'qty': from_old_record.qty - product['qty']
                            })
                            to_record = request.env['clbcl.club.partner.product'].search(
                                [('product_id', '=', product['product_id'][0])
                                    , ('partner_id', '=', send_gift.to_partner_id.id)
                                    , ('club_id', '=', send_gift.club_id.id)
                                    , ('is_empty', '=', False)])
                            if to_record.id:
                                to_record.write({
                                    'qty': to_record.qty + product['qty']
                                })
                            else:
                                request.env['clbcl.club.partner.product'].create({
                                    'product_id': product['product_id'][0],
                                    'partner_id': send_gift.to_partner_id.id,
                                    'club_id': send_gift.club_id.id,
                                    'qty': product['qty'],
                                    'is_empty': False
                                })
                    else:
                        return {'status': 400, 'message': 'Số lượng sản phẩm không đủ'}

                send_gift.write({
                    'status': 'Đã nhận'
                })

        return {'status': 200, 'message': 'Cập nhật thành công'}

    @http.route('/get_bank_info', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_bank_info(self, **rec):
        order = request.env['sale.order'].search([('id', '=', rec['order_id'])])
        banks = request.env['clbcl.bank.info'].search_read([])

        return {'status': 200, 'banks': banks, 'order_name': order.name, 'amount_total': order.amount_total,
                'voucher_discount': order.voucher_discount}

    @http.route('/get_attributes', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_attributes(self, **rec):
        attributes = request.env['product.attribute'].search_read([])
        all_attributes = []
        for attribute in attributes:
            attribute_values = request.env['product.attribute.value'].search_read([('id', 'in', attribute['value_ids'])])
            all_attribute_values = []
            for attribute_value in attribute_values:
                group = ''
                name = attribute_value['name']
                index = attribute_value['name'].find("/")
                if index > 0:
                    group = attribute_value['name'][0:index]
                    name = attribute_value['name'][index+1:len(attribute_value['name'])]
                all_attribute_values.append({
                    'id': attribute_value['id'],
                    'name': name,
                    'group': group
                })
            all_attributes.append({
                'id': attribute['id'],
                # 'value_ids': attribute['value_ids'],
                'sequence': attribute['sequence'],
                # 'attribute_line_ids': attribute['attribute_line_ids'],
                # 'product_tmpl_ids': attribute['product_tmpl_ids'],
                'display_type': attribute['display_type'],
                'display_name': attribute['display_name'],
                'attribute_values': all_attribute_values
            })

        return {'status': 200, 'attributes': all_attributes}

    @http.route('/get_product_details', type='json', auth='public', methods=['POST'], website=True, sitemap=False)
    def get_product_details(self, **rec):
        product = request.env['product.product'].search_read([('id', '=', rec['product_id'])])
        product_template = request.env['product.template'].search_read([('id', '=', product[0]['product_tmpl_id'][0])])

        attributes = request.env['product.template.attribute.value'].search_read([('id', 'in', product[0]['product_template_variant_value_ids'])])
        all_attributes = []
        for attribute in attributes:
            all_attributes.append({
                'name': attribute['name'],
                'key': attribute['attribute_line_id'][1]
            })
        attributes_lines = request.env['product.template.attribute.line'].search_read(
            [('id', 'in', product_template[0]['valid_product_template_attribute_line_ids'])])

        for attributes_line in attributes_lines:
            if attributes_line['value_count'] == 1:
                tmp_attributes = request.env['product.template.attribute.value'].search_read(
                    [('id', '=', attributes_line['value_ids'][0])])

                all_attributes.append({
                    'name': attributes_line['attributes_line'][1],
                    'key': tmp_attributes[0]['name']
                })
        return {'status': 200, 'product': {
            "product_variant_count":product[0]['product_variant_count'],
            "type":product[0]['type'],
            "is_published":product[0]['is_published'],
            "id":product[0]['id'],
            "priority":product[0]['priority'],
            "name":product[0]['name'],
            "product_tmpl_id":product[0]['product_tmpl_id'],
            "product_template_variant_value_ids":product[0]['product_template_variant_value_ids'],
            "sale_ok":product[0]['sale_ok'],
            "purchase_ok":product[0]['purchase_ok'],
            "active":product[0]['active'],
            "description":product[0]['description'],
            "public_categ_ids":product[0]['public_categ_ids'],
            "description":product[0]['description'],
            "display_name":product[0]['display_name'],
            "star":product[0]['star'],
            "review_count":product[0]['review_count'],
            "light_bold":product[0]['light_bold'],
            "smooth_tannic":product[0]['smooth_tannic'],
            "dry_sweet":product[0]['dry_sweet'],
            "soft_acidic":product[0]['soft_acidic'],
            "summary1":product[0]['summary1'],
            "summary2":product[0]['summary2'],
            "summary3":product[0]['summary3'],
            "public_categ_ids":product[0]['public_categ_ids'],
        }, 'attributes': all_attributes, 'product_template': product_template[0]}