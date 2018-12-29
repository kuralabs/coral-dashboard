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
    AttrMap,
    BarGraph,
    WidgetWrap,
)


log = get_logger(__name__)


class ScalableBarGraph(BarGraph):

    def __init__(self, *args, align='left', **kwargs):
        assert align in ['left', 'right']
        self._align = align
        super().__init__(*args, **kwargs)

    def calculate_bar_widths(self, size, bardata):
        """
        Fixes a bug in urwid 2.0.1 causing a::

            File ".../urwid/graphics.py", line 397, in calculate_bar_widths
                len(bardata), maxcol / self.bar_width)
            TypeError: can't multiply sequence by non-int of type 'float'

        Fixed in https://github.com/urwid/urwid/pull/325 (merged) but not yet
        released.
        """
        (maxcol, maxrow) = size

        if self.bar_width is not None:
            return [self.bar_width] * min(
                len(bardata), maxcol // self.bar_width
            )

        return super().calculate_bar_widths(size, bardata)

    def _get_data(self, size):
        """
        This function is called by render to retrieve the data for the graph.

        This implementation will truncate the bardata list returned if not all
        bars will fit within maxcol.

        This is basically a copy-paste of the original widget, but uses the
        "align" parameter to decide what part of the data array to return.
        """
        (maxcol, maxrow) = size
        bardata, top, hlines = self.data
        widths = self.calculate_bar_widths((maxcol, maxrow), bardata)

        if len(bardata) > len(widths):
            if self._align == 'right':
                return bardata[:len(widths)], top, hlines
            return bardata[-len(widths):], top, hlines
        return bardata, top, hlines


class Graph(WidgetWrap):
    MAX_ENTRIES = 200

    def __init__(self, identifier, left_tpl, right_tpl):

        self._identifier = identifier
        self._left_tpl = left_tpl
        self._right_tpl = right_tpl

        self._data = [(0, 0)] * self.MAX_ENTRIES
        self._data_count = 0

        self.left_label = Text(
            self._left_tpl.format(
                quotient=0.0,
                value=0.0,
                total=0.0,
            ),
            align='left',
        )
        self.right_label = Text(
            self._right_tpl.format(
                quotient=0.0,
                value=0.0,
                total=0.0,
            ),
            align='right',
        )

        self.graph = ScalableBarGraph(
            [
                '{} background'.format(identifier),
                '{} bar1'.format(identifier),
                '{} bar2'.format(identifier),
            ],
            satt={
                (1, 0): '{} bar1 smooth'.format(identifier),
                (2, 0): '{} bar2 smooth'.format(identifier),
            },
            align='left',
        )
        self.graph.set_bar_width(1)

        super().__init__(
            Pile([
                ('pack', Columns([
                    AttrMap(
                        self.left_label,
                        '{} left_label'.format(identifier)
                    ),
                    AttrMap(
                        self.right_label,
                        '{} right_label'.format(identifier)
                    ),
                ], dividechars=1)),
                self.graph,
            ])
        )

    def push(self, value, total):

        # Calculate proportion
        quotient = min(max((value / total), 0.0), 1.0) * 100.0

        # Update labels
        self.left_label.set_text(
            self._left_tpl.format(
                quotient=quotient,
                value=value,
                total=total,
            )
        )
        self.right_label.set_text(
            self._right_tpl.format(
                quotient=quotient,
                value=value,
                total=total,
            )
        )

        # Append new entry to data buffer
        entry = (quotient, 0) if self._data_count & 1 else (0, quotient)
        self._data.append(entry)

        # Trim the buffer to MAX_ENTRIES and update data
        del self._data[0]
        self._data_count += 1

        self.graph.set_data(self._data, 100.0)


__all__ = [
    'Graph',
]
