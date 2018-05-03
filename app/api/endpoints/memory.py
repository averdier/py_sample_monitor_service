# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Namespace, Resource, abort
from ..serializers.memory import memory_post_model, memory_model, history_container
from app.extensions import db
from app.models import MemoryStatus


ns = Namespace('memory', description='Memory related operations.')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API memory endpoints
#
# ================================================================================================

@ns.route('/')
class MemoryCollection(Resource):

    @ns.marshal_with(history_container)
    def get(self):
        """
        Return memory history
        """
        return {'history': [m for m in MemoryStatus.query.all()]}

    @ns.marshal_with(memory_model)
    @ns.expect(memory_post_model)
    def post(self):
        """
        Add memory status
        """
        data = request.json

        m = MemoryStatus(
            device_id=data['device_id'],
            timestamp=data['timestamp'],
            total=data['total'],
            available=data['available'],
            used=data['used'],
            free=data['free'],
            active=data.get('active', None),
            inactive=data.get('inactive', None),
            buffers=data.get('buffers', None),
            cached=data.get('cached', None),
            shared=data.get('shared', None),
            slab=data.get('slab', None)
        )

        db.session.add(m)
        db.session.commit()

        return m


@ns.route('/<id>')
class MemoryItem(Resource):

    @ns.marshal_with(memory_model)
    def get(self, id):
        """
        Return memory
        """
        return MemoryStatus.query.get_or_404(id)

    @ns.response(204, 'Memory status successfully deleted.')
    def delete(self, id):
        """
        Delete memory status
        """
        m = MemoryStatus.query.get_or_404(id)

        db.session.delete(m)
        db.session.commit()

        return 'Memory status successfully deleted.', 204
