# -*- coding: utf-8 -*-

from .extensions import db


class MemoryStatus(db.Model):
    """
    Memory status model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.String, nullable=False, index=True)
    timestamp = db.Column(db.Integer, nullable=False, index=True)
    total = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    used = db.Column(db.Integer, nullable=False)
    free = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer)
    inactive = db.Column(db.Integer)
    buffers = db.Column(db.Integer)
    cached = db.Column(db.Integer)
    shared = db.Column(db.Integer)
    slab = db.Column(db.Integer)
