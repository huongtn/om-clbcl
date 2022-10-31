# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubBooking(models.Model):
    _name = "clbcl.club.booking"
    _description = "CLBCL Club booking"
    code = fields.Text(string='Code')
    club_id = fields.Many2one("clbcl.club", string='Club')
    partner_id = fields.Many2one("res.partner", string='Customer')
    date_time = fields.Datetime(string='Date time')
    table = fields.Text(string='Table')
    status = fields.Selection([
        ('Riêng tư', 'Riêng tư'),
        ('Tiêu chuẩn', 'Tiêu chuẩn')
    ], required=True, default='Tiêu chuẩn', tracking=True)
    participant_count = fields.Integer(string='Participant Count')
    status = fields.Selection([
        ('Chờ xác nhận', 'Chờ xác nhận'),
        ('Xác nhận', 'Xác nhận'),
        ('Đang diễn ra', 'Đang diễn ra'),
        ('Đã hoàn tất', 'Đã hoàn tất'),
        ('Đã bị hủy', 'Đã bị hủy'),
    ], required=True, default='Chờ xác nhận', tracking=True)
    product_count = fields.Integer(string='Product', compute='get_product_count')

    def get_product_count(self):
        try:
            count = self.env['clbcl.club.booking.product'].search_count([('booking_id', '=', self.id)])
            self.product_count = count
        except:
            self.product_count = 0

    def write(self, values):
        if 'status' in values:
            if values['status'] == 'Đã hoàn tất':
                print('id', self.id)
                print('partner_id', self.partner_id.id)
                print('club_id', self.club_id.id)
                products = self.env['clbcl.club.booking.product'].search([('booking_id', '=', self.id)])
                for product in products:
                    old_record = self.env['clbcl.club.partner.product'].search(
                        [('product_id', '=', product.product_id.id)
                            , ('partner_id', '=', self.partner_id.id)
                            , ('club_id', '=', self.club_id.id)
                            , ('is_empty', '=', False)
                            , ('qty', '>=', product.qty)])
                    if old_record.id:
                        old_record.write({
                            'qty': old_record.qty - product.qty
                        })
                        old_empty_record = self.env['clbcl.club.partner.product'].search(
                            [('product_id', '=', product.product_id.id)
                                , ('partner_id', '=', self.partner_id.id)
                                , ('club_id', '=', self.club_id.id)
                                , ('is_empty', '=', True)])
                        if old_empty_record.id:
                            old_empty_record.write({
                                'qty': old_empty_record.qty + product.qty
                            })
                        else:
                            self.env['clbcl.club.partner.product'].create({
                                'product_id': product.product_id.id,
                                'partner_id': self.partner_id.id,
                                'club_id': self.club_id.id,
                                'qty': product.qty,
                                'is_empty': True
                            })
                        return super(CLBCLClubBooking, self).write(values)
                    else:
                        return 'Sản phẩm không có trong kho'
            else:
                return super(CLBCLClubBooking, self).write(values)
        else:
            return super(CLBCLClubBooking, self).write(values)

    def open_booking_products(self):
        return {
            'name': _('Products'),
            'domain': [('booking_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'clbcl.club.booking.product',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
