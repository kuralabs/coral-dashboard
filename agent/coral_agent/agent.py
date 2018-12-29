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
Metrics collector agent.
"""

from time import time, sleep
from datetime import datetime
from collections import OrderedDict
from logging import getLogger as get_logger

from requests import post
from pprintpp import pformat


log = get_logger(__name__)


class GenericAgent:
    """
    :param str dashboard: IP or hostname to dashboard server.
    :param float frequency_s: Sampling frequency in seconds.

    :var str USER_AGENT: User agent to use in requests.
    :var str TITLE: Base template for the dashboard title.
    :var float NOTIFICATION_THRESHOLD: Number of seconds to leave the popup
     open before auto-closing it.
    :var list PALETTE: Palette to configure in the dashboard.
    :var list WIDGETS: Widgets specification to configure in the dashboard.

    Note that this generic agent supposes one screen and one configuration at
    startup, but there is nothing enforcing this workflow. If your application
    wants to change screens and widget layout you may implement an agent
    without this assumption.
    """

    USER_AGENT = 'coral/generic'
    TITLE = 'Generic Dashboard - {{version}} - {timestamp}'
    NOTIFICATION_THRESHOLD = 10.0

    METRICS = OrderedDict()
    PALETTE = []
    WIDGETS = []

    def __init__(self, dashboard, frequency_s):
        self._dashboard = dashboard
        self._frequency_s = frequency_s

        self._run = True
        self._iteration = 0
        self._last_notification = None
        self._endpoint = 'http://{}/api/{{}}'.format(
            self._dashboard,
        )

    def format_title(self, timestamp):
        title = self.TITLE.format(timestamp=(
            datetime
            .fromtimestamp(timestamp)
            .replace(microsecond=0)
            .isoformat()
        ))
        return title

    def format_issues(self, issues):
        return '\n'.join(['Issues Detected:'] + issues)

    def stop(self):
        self._run = False

    def start(self):

        self.config(time(), self.PALETTE, self.WIDGETS)

        while self._run:
            # Timestamp and collect metrics
            timestamp = time()
            metrics, issues = self.collect()

            # Publish metrics
            try:
                if metrics:
                    response = self.publish(timestamp, metrics)
                    log.info(pformat(response))
                else:
                    log.warning(
                        'No metrics collected at iteration {}'.format(
                            self._iteration,
                        )
                    )
            except Exception:
                log.exception(
                    'Exception publishing metrics at iteration {}'.format(
                        self._iteration,
                    )
                )

            # Notify issues
            try:
                if issues:
                    log.warning(
                        '{} issues detected at iteration {}'.format(
                            len(issues), self._iteration,
                        )
                    )
                    response = self.notify(timestamp, issues)
                    self._last_notification = timestamp
                    log.info(pformat(response))

                # Disable popup if notification threshold has passed
                elif (
                    self._last_notification is not None and
                    (timestamp - self._last_notification) >=
                    self.NOTIFICATION_THRESHOLD
                ):
                    response = self.notify(timestamp)
                    self._last_notification = None
                    log.info(pformat(response))

            except Exception:
                log.exception(
                    'Exception notifying issues at iteration {}'.format(
                        self._iteration,
                    )
                )

            # Wait until next sample
            wait = self._frequency_s - (time() - timestamp)
            if wait > 0:
                sleep(wait)
            else:
                log.critical(
                    'Behind schedule by {:.2f}s at iteration {}'.format(
                        wait, self._iteration
                    )
                )
            self._iteration += 1

    def collect(self):
        metrics = OrderedDict()
        issues = []
        for metric, collector in self.METRICS.items():
            try:
                metrics[metric] = getattr(self, collector)()
            except NotImplementedError:
                log.info(
                    '{} metric not implemented. Ignoring ...'.format(
                        metric,
                    )
                )
            except Exception as e:
                log.exception(
                    'Unable to collect metric {} at iteration {}'.format(
                        metric, self._iteration,
                    )
                )
                issues.append('{}: {}'.format(metric, str(e)))

        return metrics, issues

    def config(self, timestamp, palette, widgets):

        title = self.format_title(timestamp)

        response = post(
            self._endpoint.format('config'),
            headers={
                'user-agent': self.USER_AGENT,
                'content-type': 'application/json',
            },
            json={
                'title': title,
                'palette': palette,
                'widgets': widgets,
            },
        )
        response.raise_for_status()
        return response.json()

    def publish(self, timestamp, metrics):
        """
        :param float timestamp: POSIX timestamp since epoch for the current
         bundle. Same as returned by time().
        :param dict metrics: Bundle of metrics to push to the dashboard.

        :return: Response payload from server.
        :rtype: dict
        """
        title = self.format_title(timestamp)

        response = post(
            self._endpoint.format('push'),
            headers={
                'user-agent': self.USER_AGENT,
                'content-type': 'application/json',
            },
            json={
                'title': title,
                'data': metrics,
            },
        )
        response.raise_for_status()
        return response.json()

    def notify(self, timestamp, issues=None):
        """
        :param float timestamp: POSIX timestamp since epoch for the current
         bundle. Same as returned by time().
        :param list issues: List of issues encountered during data collection.
         Or None to remove notification.

        :return: Response payload from server.
        :rtype: dict
        """

        title = self.format_title(timestamp)
        message = '' if issues is None else self.format_issues(issues)

        response = post(
            self._endpoint.format('message'),
            headers={
                'user-agent': self.USER_AGENT,
                'content-type': 'application/json',
            },
            json={
                'title': title,
                'message': message,
                # FIXME: Parametrize
                # 'width': width,
                # 'height': height,
                # 'type': 'WARNING',
            },
        )
        response.raise_for_status()
        return response.json()


__all__ = [
    'GenericAgent',
]
