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
UI manager and builder.
"""

from collections import OrderedDict
from logging import getLogger as get_logger

from urwid import (
    AttrMap,
    Text, Divider,
    Pile, Columns,
    PopUpLauncher,
    Filler, LineBox,
    WidgetPlaceholder,
)

from .bar import Bar
from .graph import Graph
from .. import __version__


log = get_logger(__name__)


class MessageShower(PopUpLauncher):

    ICONS = {
        # FIXME: Find more icons
        'WARNING': u'\u26A0',
    }

    def __init__(self, body, width, height):
        self._width = width
        self._height = height
        self._text = Text('', align='center')
        super().__init__(body)

    def show(self, text, icon='WARNING'):
        self._text.set_text(
            '{} {}'.format(self.ICONS[icon], text)
        )
        self.open_pop_up()

    def hide(self):
        self.close_pop_up()

    def create_pop_up(self):
        return self._text

    def get_pop_up_parameters(self):
        return {
            'left': 0,
            'top': 1,
            'overlay_width': self._width,
            'overlay_height': self._height,
        }


class UIManager:

    SUPPORTED_WIDGETS = {
        'graph': Graph,
        'bar': Bar,
    }

    DEFAULT_TITLE = 'Coral Dashboard - {version}'

    def __init__(self):
        self._body = WidgetPlaceholder(Pile([
            Filler(
                Text(
                    'Coral Dashboard Initialized\n'
                    'Waiting for agent ...',
                    align='center',
                ),
            ),
        ]))
        self._wrapper = LineBox(
            self._body,
            title=self.DEFAULT_TITLE.format(version=__version__),
        )

        self.palette = ()
        self.topmost = MessageShower(
            self._wrapper,
            width=32,
            height=7,
        )
        self.tree = OrderedDict()

    def build(self, widgets, title):

        rows = []
        tree = OrderedDict()

        def _instance_and_register(widget, identifier, **kwargs):
            widgetclass = self.SUPPORTED_WIDGETS[widget]
            instance = widgetclass(identifier, **kwargs)
            tree[identifier] = instance
            return instance

        for descriptor in widgets:

            # Descriptor for an instance of a Graph or a Bar
            if type(descriptor) is dict:
                widget = _instance_and_register(**descriptor)

                if isinstance(widget, Bar):
                    widget = ('pack', widget)

            # Descriptor for a divider
            elif descriptor is None:
                widget = ('pack', Divider(' '))

            # Descriptor for a section title
            elif type(descriptor) is str:
                widget = ('pack', AttrMap(
                    Text(descriptor, align='center'),
                    'section title'
                ))

            # Descriptor for columns
            # IMPORTANT:
            #     With this implementation, you may only have columns of the
            #     same widget type, either all columns are graphs, or all
            #     columns are bars.
            elif type(descriptor) is list:
                columns = [
                    _instance_and_register(**column)
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

        # Set new screen
        if title is None:
            title = self.DEFAULT_TITLE

        self._wrapper.set_title(title.format(version=__version__))

        self._body.original_widget = Pile(rows)
        self.tree = tree

        return {
            'tree': list(tree)
        }

    def popup_show(self, message):
        self._body.show()

    def popup_hide(self):
        self._body.hide()

    def push(self, data, title):

        pushed = []

        for key, value in data.items():
            if key not in self.tree:
                log.warning(
                    'Unknown UI field {} got value {}'.format(key, value)
                )
                continue

            self.tree[key].push(**value)
            pushed.append(key)

        if title is None:
            title = self.DEFAULT_TITLE

        self._wrapper.set_title(title.format(version=__version__))

        return pushed


__all__ = [
    'UIManager',
]
