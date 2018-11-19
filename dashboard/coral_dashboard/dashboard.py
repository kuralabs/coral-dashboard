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
Coral dashboard RESTful API and UI module.
"""

from asyncio import get_event_loop
from logging import getLogger as get_logger

from aiohttp import web
from ujson import dumps as udumps
from urwid import AsyncioEventLoop, MainLoop
from urwid import (
    Text,
    Filler,
)

log = get_logger(__name__)


def dumps(obj):
    """
    JSON dumps helper using ujson.

    :param dict obj: Python object to dump as JSON.

    :return: JSON formatted string.
    :rtype: str
    """
    return udumps(obj, ensure_ascii=False, escape_forward_slashes=False)


class Dashboard:
    def __init__(self, path=None, port=None):

        assert path is not None or port is not None, \
            '"path" or "port" must be passed to the Dashboard constructor'

        # Build Web App
        self.path = path
        self.port = port
        self.app = web.Application()
        self.app.router.add_post('/api/push', self.push)

        # Build UI App
        self.txt = Text(u"Hello World")
        topmost = Filler(self.txt, 'top')
        self.uiloop = MainLoop(  # noqa
            topmost,
            event_loop=AsyncioEventLoop(loop=get_event_loop())
        )

    def run(self):

        # This is aiohttp blocking call that starts the loop. By default, it
        # will use the aiohttp default loop. It would be nice that we could
        # specify the loop, for this application it is OK, but definitely in
        # the future we should identify how to share a loop explicitly.
        self.uiloop.start()
        self.app.on_shutdown.append(lambda app: self.uiloop.stop())
        web.run_app(self.app, path=self.path, port=self.port)

    async def push(self, request):
        results = {
            'remote': request.remote,
            'agent': request.headers['User-Agent'],
        }

        message = 'Request from {remote} with user agent {agent}'.format(
            remote=request.remote,
            agent=request.headers['User-Agent'],
        )
        log.info(message)
        self.txt.set_text(message)

        return web.json_response(results, dumps=dumps)


__all__ = [
    'Dashboard',
]
