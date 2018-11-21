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
    Pile,
    Text,
    Filler,
    AttrMap,
    Columns,
    Divider,
)


log = get_logger(__name__)


class CoralUI:
    """
    FIXME: Document.
    """
    palette = [
        ('widget_header',   'white,bold',   'dark cyan',),
        ('section_header',  'white',        'dark magenta',),
        ('style1',          'black',        'light gray'),
        ('style2',          'white',        'black'),
    ]

    def __init__(self):
        self.widgets_config = [
            { 'title': 'Temperature', 'sections': ['Coolant', 'GPU', 'CPU'] },
            { 'title': 'Load', 'sections': ['GPU', 'CPU']}
        ]

        self.header = Text(('style1', u' Hello World '), align='center')
        map1 = AttrMap(self.header, 'style1')

        self.widgets = Pile([self.get_widget(w) for w in self.widgets_config])
        fill = Filler(Pile([map1, self.widgets]), 'top')
        self.topmost = AttrMap(fill, 'style2')

    def get_widget(self, w):
        header = Text(('widget_header', w['title']))
        header_map = AttrMap(header, 'widget_header')

        div = Divider(u'=')
        div_map = AttrMap(div, 'widget_header')
        space = Divider(u' ')

        sections = [self.get_section(s) for s in w['sections']]
        cols = Columns(sections, dividechars=1)

        pile = Pile([header_map, div_map, cols, space])

        return pile

    def get_section(self, title):
        header = Text(('section_header', title), align='center')
        header_map = AttrMap(header, 'section_header')

        pile = Pile([header_map])

        return pile

__all__ = [
    'CoralUI',
]
