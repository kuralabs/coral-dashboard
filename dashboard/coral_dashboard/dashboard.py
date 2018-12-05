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
Coral dashboard RESTful API manager.
"""

from functools import wraps
from datetime import datetime
from asyncio import get_event_loop, sleep
from logging import getLogger as get_logger

from ujson import (
    dumps as udumps,
    loads as uloads,
)
from aiohttp import web
from pprintpp import pformat
from urwid import MainLoop, AsyncioEventLoop
from aiohttp_remotes import XForwardedRelaxed
from aiohttp_cors import setup as CorsConfig, ResourceOptions

from .ui.manager import UIManager
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


def schema(schema_id):
    """
    Decorator to assign a schema name to an endpoint handler.
    """
    def decorator(handler):
        handler.__schema_id__ = schema_id
        return handler
    return decorator


class Dashboard:
    """
    Main Dashboard application.

    This class manages the web application (and their endpoints) and the
    terminal UI application in a single AsyncIO loop.

    :param int port: A TCP port to serve from.
    """

    DEFAULT_HEARTBEAT_MAX = 10

    def __init__(self, port, logs=None):

        # Build Web App
        self.port = port
        self.logs = logs
        self.webapp = web.Application(middlewares=[
            # Just in case someone wants to use it behind a reverse proxy
            # Not sure why someone will want to do that though
            XForwardedRelaxed().middleware,
            # Handle unexpected and HTTP exceptions
            self._middleware_exceptions,
            # Handle media type validation
            self._middleware_media_type,
            # Handle schema validation
            self._middleware_schema,
        ])

        self.webapp.router.add_get('/api/logs', self.api_logs)
        self.webapp.router.add_post('/api/config', self.api_config)
        self.webapp.router.add_post('/api/push', self.api_push)
        self.webapp.router.add_post('/api/message', self.api_message)

        # Enable CORS in case someone wants to build a web agent
        self.cors = CorsConfig(
            self.webapp, defaults={
                '*': ResourceOptions(
                    allow_credentials=True,
                    expose_headers='*',
                    allow_headers='*',
                )
            }
        )
        for route in self.webapp.router.routes():
            self.cors.add(route)

        # Create task for the push hearbeat
        event_loop = get_event_loop()

        self.timestamp = None
        self.heartbeat = event_loop.create_task(self._check_last_timestamp())

        # Build Terminal UI App
        self.ui = UIManager()
        self.tuiapp = MainLoop(
            self.ui.topmost,
            pop_ups=True,
            palette=self.ui.palette,
            event_loop=AsyncioEventLoop(loop=event_loop),
        )

    def run(self):
        """
        Blocking method that starts the event loop.
        """

        self.tuiapp.start()
        self.webapp.on_shutdown.append(lambda app: self.tuiapp.stop())
        self.webapp.on_shutdown.append(lambda app: self.heartbeat.cancel())

        # This is aiohttp blocking call that starts the loop. By default, it
        # will use the asyncio default loop. It would be nice that we could
        # specify the loop. For this application it is OK, but definitely in
        # the future we should identify how to share a loop explicitly.
        web.run_app(
            self.webapp,
            port=self.port,
            print=None,
        )

    async def _check_last_timestamp(self):
        """
        FIXME: Document.
        """
        while True:
            if self.timestamp is not None:
                now = datetime.now()
                elapsed = now - self.timestamp

                if elapsed.seconds >= self.DEFAULT_HEARTBEAT_MAX:
                    self.ui.topmost.show(
                        'WARNING! Lost contact with agent {} '
                        'seconds ago!'.format(elapsed.seconds)
                    )
            await sleep(1)

    async def _middleware_exceptions(self, app, handler):
        """
        Middleware that handlers the unexpected exceptions and HTTP standard
        exceptions.

        Unexpected exceptions are then returned as HTTP 500.
        HTTP exceptions are returned in JSON.

        :param app: Main web application object.
        :param handler: Function to be executed to dispatch the request.

        :return: A handler replacement function.
        """

        @wraps(handler)
        async def wrapper(request):

            # Log connection
            metadata = {
                'remote': request.remote,
                'agent': request.headers['User-Agent'],
                'content_type': request.content_type,
            }

            message = (
                'Connection from {remote} using {content_type} '
                'with user agent {agent}'
            ).format(**metadata)
            log.info(message)

            try:
                return await handler(request)

            except web.HTTPException as e:
                return web.json_response(
                    {
                        'error': e.reason
                    },
                    status=e.status,
                )

            except Exception as e:
                response = {
                    'error': ' '.join(str(arg) for arg in e.args),
                }
                log.exception('Unexpected server exception:\n{}'.format(
                    pformat(response)
                ))

                return web.json_response(response, status=500)

        return wrapper

    async def _middleware_media_type(self, app, handler):
        """
        Middleware that handlers media type request and respones.

        It checks for media type in the request, tries to parse the JSON and
        converts dict responses to standard JSON responses.

        :param app: Main web application object.
        :param handler: Function to be executed to dispatch the request.

        :return: A handler replacement function.
        """

        @wraps(handler)
        async def wrapper(request):

            # Check media type
            if request.content_type != 'application/json':
                raise web.HTTPUnsupportedMediaType(
                    text=(
                        'Invalid Content-Type "{}". '
                        'Only "application/json" is supported.'
                    ).format(request.content_type)
                )

            # Parse JSON request
            body = await request.text()
            try:
                payload = loads(body)
            except ValueError:
                log.error('Invalid JSON payload:\n{}'.format(body))
                raise web.HTTPBadRequest(
                    text='Invalid JSON payload'
                )

            # Log request and responses
            log.info('Request:\n{}'.format(pformat(payload)))
            response = await handler(request, payload)
            log.info('Response:\n{}'.format(pformat(response)))

            # Convert dictionaries to JSON responses
            if isinstance(response, dict):
                return web.json_response(response)
            return response

        return wrapper

    async def _middleware_schema(self, app, handler):
        """
        Middleware that validates the request against the schema defined for
        the handler.

        :param app: Main web application object.
        :param handler: Function to be executed to dispatch the request.

        :return: A handler replacement function.
        """

        schema_id = getattr(handler, '__schema_id__', None)
        if schema_id is None:
            return handler

        @wraps(handler)
        async def wrapper(request, payload):

            # Validate payload
            validated, errors = validate_schema(schema_id, payload)
            if errors:
                raise web.HTTPBadRequest(
                    text='Invalid {} request:\n{}'.format(schema_id, errors)
                )

            return await handler(request, validated)

        return wrapper

    async def api_logs(self, request):
        """
        Endpoint to get dashboard logs.
        """
        if self.logs is None:
            raise web.HTTPNotFound(text='No logs configured')
        return web.FileResponse(self.logs)

    # FIXME: Let's disable schema validation for now
    # @schema('config')
    async def api_config(self, request, validated):
        """
        Endpoint to configure UI.
        """
        tree = self.ui.build(validated['widgets'], validated['title'])
        self.tuiapp.screen.register_palette(validated['palette'])
        self.tuiapp.draw_screen()
        return tree

    @schema('push')
    async def api_push(self, request, validated):
        """
        Endpoint to push data to the dashboard.
        """
        self.timestamp = datetime.now()

        # Push data to UI
        pushed = self.ui.push(validated['data'], validated['title'])
        self.tuiapp.draw_screen()

        return {
            'pushed': pushed,
        }

    # FIXME: Let's disable schema validation for now
    # @schema('message')
    async def api_message(self, request, validated):
        """
        Endpoint to a message in UI.
        """
        message = validated.pop('message')

        if message:
            self.ui.topmost.show(message, **validated)
        else:
            self.ui.topmost.hide()

        self.tuiapp.draw_screen()

        return {
            'message': message,
        }


__all__ = [
    'Dashboard',
]
