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
    AttrMap,
)

from .bar import Bar
from .graph import Graph


log = get_logger(__name__)


CORAL_PALETTE = """
STYLE NAME                | FOREGROUND           | BACKGROUND
========================================================================

################
# Graph Styles #
################

# Temperature

temp_coolant background   |                      | black
temp_coolant bar1         |                      | light red
temp_coolant bar1 smooth  | light red            | black
temp_coolant bar2         |                      | dark red
temp_coolant bar2 smooth  | dark red             | black
temp_coolant title        | white, bold          | default
temp_coolant label        | white, bold          | default

temp_gpu background       |                      | black
temp_gpu bar1             |                      | light green
temp_gpu bar1 smooth      | light green          | black
temp_gpu bar2             |                      | dark green
temp_gpu bar2 smooth      | dark green           | black
temp_gpu title            | white, bold          | default
temp_gpu label            | white, bold          | default

temp_cpu background       |                      | black
temp_cpu bar1             |                      | light blue
temp_cpu bar1 smooth      | light blue           | black
temp_cpu bar2             |                      | dark blue
temp_cpu bar2 smooth      | dark blue            | black
temp_cpu title            | white, bold          | default
temp_cpu label            | white, bold          | default

# Load

load_gpu background       |                      | black
load_gpu bar1             |                      | dark green
load_gpu bar1 smooth      | dark green           | black
load_gpu bar2             |                      | light gray
load_gpu bar2 smooth      | light gray           | black
load_gpu title            | white, bold          | default
load_gpu label            | white, bold          | default

load_cpu background       |                      | black
load_cpu bar1             |                      | dark blue
load_cpu bar1 smooth      | dark blue            | black
load_cpu bar2             |                      | light gray
load_cpu bar2 smooth      | light gray           | black
load_cpu title            | white, bold          | default
load_cpu label            | white, bold          | default

# Memory

memory background         |                      | black
memory bar1               |                      | white
memory bar1 smooth        | white                | black
memory bar2               |                      | light gray
memory bar2 smooth        | light gray           | black
memory title              | white, bold          | default
memory label              | white, bold          | default

# Network

network background        |                      | black
network bar1              |                      | light magenta
network bar1 smooth       | light magenta        | black
network bar2              |                      | dark magenta
network bar2 smooth       | dark magenta         | black
network title             | white, bold          | default
network label             | white, bold          | default

################
# Bar Styles   #
################

pump normal               | white                | dark gray
pump complete             | white                | dark red
pump smooth               | dark gray            | white
pump title                | white, bold          | default
pump label                | white, bold          | default

disk_os normal            | white                | dark gray
disk_os complete          | white                | dark cyan
disk_os smooth            | dark gray            | white
disk_os title             | white, bold          | default
disk_os label             | white, bold          | default

disk_apps normal          | white                | dark gray
disk_apps complete        | white                | brown
disk_apps smooth          | dark gray            | black
disk_apps title           | white, bold          | default
disk_apps label           | white, bold          | default

####################
#  General Styles  #
####################

section title             | black, bold          | white
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


class CoralUI:
    """
    FIXME: Document.
    """
    palette = parse_palette(CORAL_PALETTE)

    def __init__(self):

        self.tree = OrderedDict()
        self.widgets = [
            # None - Divider
            # String - Text
            # (WidgetType, identifier, title, unit) - Widget
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
        for descriptor in self.widgets:

            # Descriptor for an instance of a Graph or a Bar
            if type(descriptor) is tuple:
                widget = self._get_widget_instance(*descriptor)

                if isinstance(widget, Bar):
                    widget = ('pack', widget)

            # Descriptor for a divider
            elif descriptor is None:
                widget = ('pack', Divider(' '))

            # Descriptor for a section title
            elif type(descriptor) is str:
                title = Text(('section title', descriptor), align='center')
                widget = ('pack', AttrMap(title, 'section title'))

            # Descriptor for a columns
            # IMPORTANT:
            #     With this implementation, you may only have columns of the
            #     same widget type, either all columns are graphs, or all
            #     columns are bars.
            elif type(descriptor) is list:
                columns = [
                    self._get_widget_instance(*column)
                    for column in descriptor
                ]
                widget = Columns(columns, dividechars=1)

                if any(isinstance(column, Bar) for column in columns):
                    widget = ('pack', widget)

            else:
                raise RuntimeError(
                    'Unknown descriptor type {} for {}'.format(
                        type(descriptor),
                        descriptor,
                    )
                )

            rows.append(widget)

        self.topmost = Padding(Pile(rows), right=1, left=1)

        # FIXME: Just for testing
        for widget in self.tree.values():
            if isinstance(widget, Graph):
                total = 60
                for i in range(total):
                    widget.push(value=i + 1, total=total)
                continue

        self.tree['disk_os'].push(value=1500, total=4000)
        self.tree['pump'].push(value=1000, total=2000)
        self.tree['disk_apps'].push(value=600, total=1000)

    def _get_widget_instance(self, widget, identifier, title, unit):
        instance = widget(identifier, title, unit)
        self.tree[identifier] = instance
        return instance

    def push(self, data):
        for key, value in data.items():
            if key not in self.tree:
                log.warning(
                    'Unknown UI field {} got value {}'.format(key, value)
                )
                continue

            self.tree[key].push(**value)


__all__ = [
    'CoralUI',
]
