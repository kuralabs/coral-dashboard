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
    AttrMap,
    Columns,
    WidgetWrap,
    ProgressBar,
)


log = get_logger(__name__)


class OptionalTextProgressBar(ProgressBar):

    def __init__(self, *args, has_text=True, **kwargs):
        self._has_text = has_text
        super().__init__(*args, **kwargs)

    def get_text(self):
        if self._has_text:
            return super().get_text()
        return ''


class Bar(WidgetWrap):
    def __init__(self, identifier, left_tpl, right_tpl, rows=3):

        self._identifier = identifier
        self._left_tpl = left_tpl
        self._right_tpl = right_tpl

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

        middle = ceil(rows / 2) - 1
        self.bars = [
            OptionalTextProgressBar(
                '{} normal'.format(identifier),
                '{} complete'.format(identifier),
                satt='{} smooth'.format(identifier),
                has_text=(middle == r),
            ) for r in range(rows)
        ]

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
            ] + [
                ('pack', bar)
                for bar in self.bars
            ])
        )

    def push(self, value, total):

        # Calculate proportion
        quotient = (value / total) * 100.0

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

        for bar in self.bars:
            bar.set_completion(quotient)


__all__ = [
    'Bar',
]
