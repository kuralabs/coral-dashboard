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
Module implementing the main data visualization widget.
"""

from logging import getLogger as get_logger

from urwid import (
    Text,
    Pile,
    Columns,
    BarGraph,
    WidgetWrap,
)


log = get_logger(__name__)


class Graph(WidgetWrap):
    def __init__(self, title):
        self.title = Text(title, align='left')
        self.label = Text('', align='right')

        self.data = []
        self.graph = BarGraph(
            # FIXME: Parametrize styles
            ['bg background', 'bg 1', 'bg 2'],
            satt={
                (1, 0): 'bg 1 smooth',
                (2, 0): 'bg 2 smooth',
            }
        )

        super().__init__(
            Pile([
                ('pack', Columns([
                    self.title,
                    self.label,
                ], dividechars=1)),
                self.graph,
            ])
        )

    def push(self, percent=None, value=None, total=None):

        label = '{:.2f}%'

        if percent is None:
            if value is None or total is None:
                raise RuntimeError(
                    'value and total must be passed when pushing data without '
                    'the percent'
                )
            percent = (float(value) / float(total)) * 100.0
            label = '{} [{}/{}]'.format(label, value, total)

        self.label.set_text(label.format(percent))

        entry = [percent, 0] if len(self.data) & 1 else [0, percent]
        self.data.append(entry)
        self.graph.set_data(self.data, 100.0)


__all__ = [
    'Graph',
]
