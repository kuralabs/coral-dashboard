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
Module implementing the main bar widget.
"""

from logging import getLogger as get_logger

from math import ceil

from urwid import (
    Text,
    Pile,
    Columns,
    WidgetWrap,
    ProgressBar,
)


log = get_logger(__name__)


class CoralBar(ProgressBar):

    def __init__(self, *args, has_text=True, **kwargs):
        self._has_text = has_text
        super().__init__(*args, **kwargs)

    def get_text(self):
        if self._has_text:
            return super().get_text()

        return ''


class Bar(WidgetWrap):
    def __init__(self, identifier, title, unit, rows=3):

        self._identifier = identifier
        self._title = title
        self._unit = unit

        self.title = Text(
            '{} ({})'.format(title, unit),
            align='left'
        )
        self.label = Text('', align='right')

        middle = ceil(rows / 2) - 1
        self.bars = [
            CoralBar(
                '{} complete'.format(identifier),
                '{} incomplete'.format(identifier),
                satt='{} smooth'.format(identifier),
                has_text=(middle == r),
            ) for r in range(rows)
        ]

        super().__init__(
            Pile([
                ('pack', Columns([
                    self.title,
                    self.label,
                ], dividechars=1)),
            ] + [
                ('pack', bar)
                for bar in self.bars
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

        for bar in self.bars:
            bar.set_completion(percent)


__all__ = [
    'Bar',
]
