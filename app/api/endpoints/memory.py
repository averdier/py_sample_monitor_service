# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Namespace, Resource, abort
from ..serializers.memory import memory_post_model, memory_model, history_container
from ..parsers import memory_parser
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
    @ns.expect(memory_parser)
    def get(self):
        """
        Return memory history
        """
        args = memory_parser.parse_args()
        if list(args.values()) != [None, None, None]:
            status_list = []
            if args.get('device_id'):
                status_list = MemoryStatus.query.filter_by(device_id=args['device_id'])

            if (args.get('percent') and not args.get('target')) or (args.get('target') and not args.get('percent')):
                abort(400, error='percent or target missing')

            if args.get('percent') and args['percent'] not in ['over', 'below']:
                abort(400, error='Unknown direction')

            if args.get('percent') and args.get('device_id'):
                if args['percent'] == 'over':
                    status_list = status_list.filter(MemoryStatus.percent >= args['target'])
                else:
                    status_list = status_list.filter(MemoryStatus.percent <= args['target'])

            elif not args.get('device_id'):
                if args['percent'] == 'over':
                    status_list = MemoryStatus.query.filter(MemoryStatus.percent >= args['target'])
                else:
                    status_list = MemoryStatus.query.filter(MemoryStatus.percent <= args['target'])

            return {'history': [m for m in status_list.all()]}

        else:
            return {'history': [m for m in MemoryStatus.query.all()]}

    @ns.marshal_with(memory_model)
    @ns.expect(memory_post_model)
    def post(self):
        """
        Add memory status
        """
        data = request.json

        m = MemoryStatus(
            device_id=data['device_id'].replace(' ', ''),
            timestamp=data['timestamp'],
            total=data['total'],
            available=data['available'],
            percent=data['percent'],
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
