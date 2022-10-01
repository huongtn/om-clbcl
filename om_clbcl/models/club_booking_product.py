# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLClubBookingProduct(models.Model):
    _name = "clbcl.club.booking.product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CLBCL Club booking product"

    booking_id = fields.Many2one("clbcl.club.booking", string='Club Booking')
    product_id = fields.Many2one("product.product", string='Product')
    qty = fields.Float(string='Qty', tracking=True)













