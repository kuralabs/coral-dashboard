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
coral_dashboard executable module entry point.
"""

from sys import exit
from os import getuid, getpid
from logging import getLogger as get_logger

from setproctitle import setproctitle

from . import __version__
from .dashboard import Dashboard
from .args import parse_args, InvalidArgument


log = get_logger(__name__)


def main():
    """
    Application main function.
    """
    try:
        args = parse_args()
    except InvalidArgument as e:
        log.error(e)
        exit(-1)

    setproctitle('coral-dashboard@{}'.format(
        args.port if args.port is not None else args.path
    ))

    log.info('Starting Coral Dashboard {}'.format(__version__))
    log.info('Started by user UID {} using PID {}'.format(
        getuid(),
        getpid(),
    ))
    log.info('Logs at {}'.format(args.logs))
    log.info('Listening on http://0.0.0.0:{}/'.format(args.port))

    dashboard = Dashboard(args.port, logs=args.logs)
    dashboard.run()
    exit(0)


if __name__ == '__main__':
    main()


__all__ = [
    'main',
]
