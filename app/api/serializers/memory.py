# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


memory_post_model = api.model('Memory POST model', {
    'device_id': fields.String(required=True),
    'timestamp': fields.Integer(required=True, min=0),
    'total': fields.Integer(required=True, min=0),
    'available': fields.Integer(required=True, min=0),
    'used': fields.Integer(required=True, min=0),
    'free': fields.Integer(required=True, min=0),
    'active': fields.Integer(required=False, min=0),
    'inactive': fields.Integer(required=False, min=0),
    'buffers': fields.Integer(required=False, min=0),
    'cached': fields.Integer(required=False, min=0),
    'shared': fields.Integer(required=False, min=0),
    'slab': fields.Integer(required=False, min=0)
})

memory_model = api.inherit('Memory model', memory_post_model, {
    'id': fields.Integer(required=True)
})

history_container = api.model('Memory history container', {
    'history': fields.List(fields.Nested(memory_model), required=True)
})