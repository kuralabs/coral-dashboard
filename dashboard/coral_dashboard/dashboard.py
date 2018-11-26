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

from ujson import (
    dumps as udumps,
    loads as uloads,
)
from aiohttp import web
from urwid import AsyncioEventLoop, MainLoop
from aiohttp_remotes import XForwardedRelaxed

from .ui.coral import CoralUI
from .schema import validate_schema


log = get_logger(__name__)


def dumps(obj):
    """
    JSON dumps helper using ujson.

    :param dict obj: Python object to dump as JSON.

    :return: JSON formatted string.
    :rtype: str
    """
    return udumps(obj, ensure_ascii=False, escape_forward_slashes=False)


def loads(json):
    """
    JSON loads helper using ujson.

    :param str json: JSON formatted string.

    :return: Python object loaded from JSON.
    :rtype: dict
    """
    return uloads(json, precise_float=True)


class Dashboard:
    """
    Main Dashboard application.

    This class manages the web application (and their endpoints) and the
    terminal UI application in a single AsyncIO loop.

    :param int port: A TCP port to serve from.
    """

    def __init__(self, port, logs=None):

        # Build Web App
        self.port = port
        self.logs = logs
        self.webapp = web.Application(middlewares=[
            # Just in case someone wants to use it behind a reverse proxy
            # Not sure why someone will want to do that though
            XForwardedRelaxed().middleware,
        ])
        self.webapp.router.add_get('/api/logs', self.api_logs)
        self.webapp.router.add_post('/api/push', self.api_push)

        # Build Terminal UI App
        self.ui = CoralUI()
        self.tuiapp = MainLoop(
            self.ui.topmost,
            self.ui.palette,
            event_loop=AsyncioEventLoop(loop=get_event_loop())
        )

    def run(self):
        """
        Blocking method that starts the event loop.
        """

        self.tuiapp.start()
        self.webapp.on_shutdown.append(lambda app: self.tuiapp.stop())

        # This is aiohttp blocking call that starts the loop. By default, it
        # will use the asyncio default loop. It would be nice that we could
        # specify the loop. For this application it is OK, but definitely in
        # the future we should identify how to share a loop explicitly.
        web.run_app(
            self.webapp,
            port=self.port,
            print=None,
        )

    async def api_logs(self, request):
        """
        Endpoint to get dashboard logs.
        """
        if self.logs is None:
            return 'No logs configured'
        return web.FileResponse(self.logs)

    async def api_push(self, request):
        """
        Endpoint to push data to the dashboard.
        """

        # Check media type
        if request.content_type != 'application/json':
            raise web.HTTPUnsupportedMediaType(
                text=(
                    'Invalid Content-Type "{}". '
                    'Only "application/json" is supported.'
                ).format(request.content_type)
            )

        # Log request
        metadata = {
            'remote': request.remote,
            'agent': request.headers['User-Agent'],
            'content_type': request.content_type,
        }

        message = (
            'Request from {remote} using {content_type} with user '
            'agent {agent}'
        ).format(**metadata)
        log.info(message)

        # Parse JSON request
        body = await request.text()
        try:
            payload = loads(body)
        except ValueError:
            log.error('Invalid JSON payload:\n{}'.format(body))
            raise web.HTTPBadRequest(
                text='Invalid JSON payload'
            )

        # Validate payload
        errors, validated = validate_schema('push', payload)
        if errors:
            raise web.HTTPBadRequest(
                text='Invalid PUSH request:\n{}'.format(errors)
            )

        # Push data to UI
        self.ui.push(validated)

        return web.json_response(metadata, dumps=dumps)


__all__ = [
    'Dashboard',
]
