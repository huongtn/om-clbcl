# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, http
from random import randint, randrange
import datetime
from datetime import timedelta



class CLBCLDistrict(models.Model):
    _name = "clbcl.district"
    _description = "CLBCL District"

    name = fields.Text(string='Name')
    code = fields.Text(string='Code')
    province_id = fields.Many2one("clbcl.province", string='province')













