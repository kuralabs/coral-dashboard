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
Argument management module.
"""

import logging
from pathlib import Path

from colorlog import ColoredFormatter

from . import __version__


log = logging.getLogger(__name__)


class InvalidArgument(Exception):
    """
    Custom exception to raise when a command line argument or combination of
    arguments are invalid.
    """


def validate_args(args):
    """
    Validate that arguments are valid.

    :param args: An arguments namespace.
    :type args: :py:class:`argparse.Namespace`

    :return: The validated namespace.
    :rtype: :py:class:`argparse.Namespace`
    """

    # Determine path to logs
    logs = Path(args.logs)
    try:
        logs.touch(exist_ok=True)
    except (IsADirectoryError, PermissionError, Exception) as e:
        raise InvalidArgument(
            'Invalid location for logs: {}'.format(str(e))
        )
    args.logs = logs.resolve()

    # Configure logging
    logfrmt = (
        '  {thin_white}{asctime}{reset} | '
        '{log_color}{levelname:8}{reset} | '
        '{message}'
    )

    verbosity_levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    formatter = ColoredFormatter(fmt=logfrmt, style='{')

    stream = logging.FileHandler(str(args.logs))
    stream.setFormatter(formatter)

    level = verbosity_levels.get(args.verbosity, logging.DEBUG)
    logging.basicConfig(handlers=[stream], level=level)

    log.debug('Verbosity at level {}'.format(args.verbosity))

    return args


def parse_args(argv=None):
    """
    Argument parsing routine.

    :param argv: A list of argument strings.
    :type argv: list

    :return: A parsed and verified arguments namespace.
    :rtype: :py:class:`argparse.Namespace`
    """
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Coral Dashboard'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='{} v{}'.format(
            parser.description,
            __version__,
        )
    )

    parser.add_argument(
        '-v', '--verbose',
        dest='verbosity',
        help='Increase verbosity level',
        default=0,
        action='count'
    )
    parser.add_argument(
        '--logs',
        help='Log to file',
        default='coral.log',
    )

    parser.add_argument(
        '--port',
        help='TCP port',
        type=int,
        default=5000,
    )

    args = parser.parse_args(argv)
    args = validate_args(args)
    return args


__all__ = [
    'parse_args',
]
