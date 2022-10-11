# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, http
from random import randint, randrange
import datetime
from datetime import timedelta


class CLBCLWard(models.Model):
    _name = "clbcl.ward"
    _description = "CLBCL Ward"

    name = fields.Text(string='Name')
    code = fields.Text(string='Code')
    district_id = fields.Many2one("clbcl.district", string='district')
