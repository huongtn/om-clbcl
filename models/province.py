# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, http
from random import randint, randrange
import datetime
from datetime import timedelta



class CLBCLProvince(models.Model):
    _name = "clbcl.province"
    _description = "CLBCL Province"

    name = fields.Text(string='Name')
    code = fields.Text(string='Code')














