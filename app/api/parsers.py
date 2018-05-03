# -*- coding: utf-8 -*-

from . import api


memory_parser = api.parser()
memory_parser.add_argument('device_id', required=False, type=str, help='Device ID'),
memory_parser.add_argument('percent', required=False, type=str, help='Percent direction sorting (over | below)')
memory_parser.add_argument('target', required=False, type=float, help='Target of sorting')