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

from collections import OrderedDict
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

load_gpu background       | light gray           | black
load_gpu bar1             | white                | dark blue
load_gpu bar2             | white                | dark cyan
load_gpu bar1 smooth      | dark blue            | black
load_gpu bar2 smooth      | dark cyan            | black

load_cpu background       | light gray           | black
load_cpu bar1             | white                | dark blue
load_cpu bar2             | white                | dark cyan
load_cpu bar1 smooth      | dark blue            | black
load_cpu bar2 smooth      | dark cyan            | black

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

        self.tree = OrderedDict()
        self.widgets = [
            # None - Divider
            # String - Text
            # WidgetType, identifier, title, unit - Widget
            # [Widgets] - Columns
            None,
            "Temperature",
            [
                (Graph, 'temp_coolant', 'Coolant', '°C'),
                (Graph, 'temp_gpu', 'GPU', '°C'),
                (Graph, 'temp_cpu', 'CPU', '°C'),
            ],
            None,
            (Bar, 'pump', 'Pump/Fans', 'RPM'),
            None,
            "Load",
            [
                (Graph, 'load_gpu', 'GPU', '%'),
                (Graph, 'load_cpu', 'CPU', '%'),
            ],
            None,
            "Memory",
            (Graph, 'memory', 'Memory', 'GB'),
            None,
            "Network",
            (Graph, 'network', 'Network', 'Mbps'),
            None,
            "Disk",
            [
                (Bar, 'disk_os', 'C:// "Windows"', 'GB'),
                (Bar, 'disk_apps', 'D:// "Storage"', 'GB'),
            ]
        ]

        rows = []
        for desc in self.widgets:
            if type(desc) is tuple:
                instance = self.get_widget_instance(desc)
                rows.append(instance)
                continue

            if desc is None:
                rows.append(('pack', Divider(' ')))
                continue

            if type(desc) is str:
                rows.append(('pack', Text(desc, align='center')))
                continue

            rows.append(Columns([
                self.get_widget_instance(column)
                for column in desc
            ], dividechars=1))

        self.palette = palette
        self.topmost = Padding(Pile(rows), right=1, left=1)

        # FIXME: Just for testing
        for widget in self.tree.values():
            if isinstance(widget, Graph):
                total = 60
                for i in range(total):
                    widget.push(value=i + 1, total=total)
                continue

            if isinstance(widget, Bar):
                widget.push(value=1000, total=2000)

    def get_widget_instance(self, desc):
        widget, identifier, title, unit = desc
        instance = widget(identifier, title, unit)
        self.tree[identifier] = instance

        return instance

    def set_ui(self, key, value):
        # FIXME: Actually pass data to UI
        log.warning('Unknown UI field {} got value {}'.format(key, value))


__all__ = [
    'CoralUI',
]
