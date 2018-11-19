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
    Text,
    Filler,
    AttrMap,
)


log = get_logger(__name__)


class CoralUI:
    """
    FIXME: Document.
    """
    palette = [
        ('style1', 'black', 'light gray'),
        ('style2', 'black', 'dark red'),
        ('style3', 'black', 'dark blue'),
    ]

    def __init__(self):
        self.header = Text(('style1', u" Hello World "), align='center')
        map1 = AttrMap(self.header, 'style2')
        fill = Filler(map1)
        self.topmost = AttrMap(fill, 'style3')


__all__ = [
    'CoralUI',
]
