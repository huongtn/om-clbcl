# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CLBCLBankInfo(models.Model):
    _name = "clbcl.bank.info"
    _description = "CLBCL Bank Info"
    bank_name = fields.Text(string="Tên ngân hàng")
    image_url = fields.Text(string="Ảnh")
    bank_account = fields.Text(string="Tên chủ tài khoản")
    bank_account_number = fields.Text(string="Số tài khoản")
    payment_content = fields.Text(string="Nội dung chuyển khoản")