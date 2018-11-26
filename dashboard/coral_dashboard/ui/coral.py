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


_PALETTE = """
STYLE NAME                | FOREGROUND           | BACKGROUND
========================================================================

################
# Graph Styles #
################

temp_coolant background   | light gray           | black
temp_coolant bar1         | white                | dark blue
temp_coolant bar2         | white                | dark cyan
temp_coolant bar1 smooth  | dark blue            | black
temp_coolant bar2 smooth  | dark cyan            | black

temp_gpu background       | light gray           | black
temp_gpu bar1             | white                | dark blue
temp_gpu bar2             | white                | dark cyan
temp_gpu bar1 smooth      | dark blue            | black
temp_gpu bar2 smooth      | dark cyan            | black

temp_cpu background       | light gray           | black
temp_cpu bar1             | white                | dark blue
temp_cpu bar2             | white                | dark cyan
temp_cpu bar1 smooth      | dark blue            | black
temp_cpu bar2 smooth      | dark cyan            | black

gpu background            | light gray           | black
gpu bar1                  | white                | dark blue
gpu bar2                  | white                | dark cyan
gpu bar1 smooth           | dark blue            | black
gpu bar2 smooth           | dark cyan            | black

cpu background            | light gray           | black
cpu bar1                  | white                | dark blue
cpu bar2                  | white                | dark cyan
cpu bar1 smooth           | dark blue            | black
cpu bar2 smooth           | dark cyan            | black

memory background         | light gray           | black
memory bar1               | white                | dark blue
memory bar2               | white                | dark cyan
memory bar1 smooth        | dark blue            | black
memory bar2 smooth        | dark cyan            | black

network background        | light gray           | black
network bar1              | white                | dark blue
network bar2              | white                | dark cyan
network bar1 smooth       | dark blue            | black
network bar2 smooth       | dark cyan            | black

################
# Bar Styles   #
################

pump complete             | white                | dark blue
pump incomplete           | white                | dark cyan
pump smooth               | dark blue            | black

disk_os complete          | white                | dark blue
disk_os incomplete        | white                | dark cyan
disk_os smooth            | dark blue            | black

disk_apps complete        | white                | dark blue
disk_apps incomplete      | white                | dark cyan
disk_apps smooth          | dark blue            | black
"""


def parse_palette(palette):
    result = []

    for line in palette.strip().splitlines()[2:]:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        result.append(
            tuple(cell.strip() for cell in line.split('|'))
        )

    return result


CORAL_PALETTE = parse_palette(_PALETTE)


class CoralUI:
    """
    FIXME: Document.
    """

    def __init__(self, palette=CORAL_PALETTE):

        self.temp_coolant = Graph(
            'temp_coolant',
            'Coolant',
            '°C',
        )
        self.temp_gpu = Graph(
            'temp_gpu',
            'GPU',
            '°C',
        )
        self.temp_cpu = Graph(
            'temp_cpu',
            'CPU',
            '°C',
        )

        self.pump = Bar(
            'pump',
            'Pump/Fans',
            'RPM',
        )

        self.load_gpu = Graph(
            'gpu',
            'GPU',
            '%',
        )
        self.load_cpu = Graph(
            'cpu',
            'CPU',
            '%',
        )

        self.memory = Graph(
            'memory',
            'Memory',
            'GB',
        )
        self.network = Graph(
            'network',
            'Network',
            'Mbps',
        )

        self.disk_os = Bar(
            'disk_os',
            'C:// "Windows"',
            'GB',
        )
        self.disk_apps = Bar(
            'disk_apps',
            'D:// "Storage"',
            'GB',
        )

        self.palette = palette
        self.topmost = Padding(Pile([
            ('pack', Divider(' ')),
            ('pack', Text('Temperature', align='center')),
            Columns([
                self.temp_coolant,
                self.temp_gpu,
                self.temp_cpu,
            ], dividechars=1),
            ('pack', Divider(' ')),
            ('pack', self.pump),
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
            ('pack', Columns([
                self.disk_os,
                self.disk_apps,
            ], dividechars=1)),
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
