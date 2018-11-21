# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Coral UI module.
"""

from logging import getLogger as get_logger

from urwid import (
    Padding,
    Pile, Columns,
    Text, Divider,
)

from .bar import Bar
from .graph import Graph


log = get_logger(__name__)


PALETTE = """
STYLE NAME            | FOREGROUND           | BACKGROUND
====================================================================
bg background         | light gray           | black
bg 1                  | white                | dark blue | standout
bg 1 smooth           | dark blue            | black
bg 2                  | white                | dark cyan | standout
bg 2 smooth           | dark cyan            | black
bar complete          | white                | dark blue | standout
bar incomplete        | white                | dark cyan | standout
bar smooth            | dark blue            | black
"""


class CoralUI:
    """
    FIXME: Document.
    """
    palette = [
        tuple(cell.strip() for cell in line.split('|'))
        for line in PALETTE.strip().splitlines()[2:]
    ]

    def __init__(self):

        self.temp_coolant = Graph('Coolant')
        self.temp_gpu = Graph('GPU')
        self.temp_cpu = Graph('CPU')

        self.pump = Bar('Pump/Fans')

        self.load_gpu = Graph('GPU')
        self.load_cpu = Graph('CPU')

        self.memory = Graph('Memory')
        self.network = Graph('Network')

        self.disk_os = Bar('C:// "Windows"')
        self.disk_apps = Bar('D:// "Storage"')

        self.topmost = Padding(Pile([
            ('pack', Divider(' ')),
            ('pack', Text('Temperature', align='center')),
            Columns([
                self.temp_coolant,
                self.temp_gpu,
                self.temp_cpu,
            ], dividechars=1),
            ('pack', Divider(' ')),
            self.pump,
            ('pack', Divider(' ')),
            ('pack', Text('Load', align='center')),
            Columns([
                self.load_gpu,
                self.load_cpu,
            ], dividechars=1),
            ('pack', Divider(' ')),
            self.memory,
            ('pack', Divider(' ')),
            self.network,
            ('pack', Divider(' ')),
            ('pack', Text('Disk', align='center')),
            Columns([
                self.disk_os,
                self.disk_apps,
            ], dividechars=1),
        ]), right=1, left=1)

        # FIXME: Just for testing
        for graph in [
            self.temp_coolant,
            self.temp_gpu,
            self.temp_cpu,
            self.load_gpu,
            self.load_cpu,
            self.memory,
            self.network,
        ]:
            total = 60
            for i in range(total):
                graph.push(value=i + 1, total=total)

        self.pump.push(value=1000, total=2000)
        self.disk_os.push(value=1500, total=4000)
        self.disk_apps.push(value=600, total=1000)

    def set_ui(self, key, value):
        # FIXME: Actually pass data to UI
        log.warning('Unknown UI field {} got value {}'.format(key, value))


__all__ = [
    'CoralUI',
]
