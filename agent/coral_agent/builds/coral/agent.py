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
Agent for the Coral build.
"""

from sys import platform
from collections import OrderedDict
from logging import getLogger as get_logger

import psutil

from .palette import CORAL_PALETTE
from .widgets import CORAL_WIDGETS
from ...agent import GenericAgent
from ...palette import parse_palette


log = get_logger(__name__)


WINDOWS = platform == 'win32'


if WINDOWS:
    PATH_OS = 'C://'
    PATH_ARCHIVE = 'D://'
    NETWORK_INTERFACE = 'Ethernet'
else:
    PATH_OS = '/'
    PATH_ARCHIVE = '/media/archive'
    NETWORK_INTERFACE = 'eth0'


KB = 1024
MB = KB ** 2
GB = KB ** 3


def _find_identifiers(alist):
    result = []

    if not isinstance(alist, list):
        return result

    for element in alist:
        if isinstance(element, dict) and 'identifier' in element:
            result.append(element['identifier'])
            continue
        result.extend(_find_identifiers(element))

    return result


class CoralAgent(GenericAgent):

    USER_AGENT = 'coral/agent'
    TITLE = 'Coral Dashboard - {{version}} - {timestamp}'
    METRICS = OrderedDict([
        (identifier, 'collect_{}'.format(identifier))
        for identifier in _find_identifiers(CORAL_WIDGETS)
    ])
    PALETTE = parse_palette(CORAL_PALETTE)
    WIDGETS = CORAL_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from ..support.network import Interface
        self._interface = Interface(NETWORK_INTERFACE)

        from ..support.nvidia import NvidiaGPU
        self._gpu = NvidiaGPU(index=0)

        self._ohm = None
        if WINDOWS:
            from ..support.ohm import Computer
            self._ohm = Computer(['Mainboard', 'CPU'])

    def collect_temp_coolant(self):
        """
        What's the maximum acceptable temperature for the coolant?
        The following link has some interesting opinions:

            https://www.reddit.com/r/watercooling/comments/6487e4/max_acceptable_coolant_temperature/

        Coral uses XSPC FLX flexible tubing, that seems to be stable up
        to 60°C:

            http://www.xs-pc.com/soft-tubing-fittings/flx-1610mm-2m-clear

        Also, Coral's pump, Swiftech Maelstrom D5 also has a rating of
        60°C maximum.

        http://www.swiftech.com/maelstrom-d5.aspx#tab3
        """
        raise NotImplementedError()

    def collect_temp_gpu(self):

        return {
            'value': self._gpu.temperature,
            # Coral has an Nvidia GeForce GTX 1080 Ti
            # TJMax may be fetched using Nvidia NVML API. In NVML the function
            # nvmlDeviceGetTemperatureThreshold allows to retrieve two
            # temperature thresholds:
            #
            # - Slowdown: temperature where the GPU will start throttling.
            # - Shutdown: temperature where the GPU will shutdown to protect
            #   itself.
            #
            # On Coral's GPU, slowdown shows as 93°C, shutdown is set to 96°C.
            # For monitoring, we decided to put 93 as the max value for the
            # graph.
            'total': self._gpu.threshold_slowdown,
        }

    def collect_temp_cpu(self):
        # FIXME:
        if WINDOWS:
            raise NotImplementedError()

            # Something with self._ohm_handler...
            # return {
            #     'overview': None,
            #     'value': None,
            #     'total': None,
            # }

        raise NotImplementedError()

    def collect_pump(self):
        """
        Total is determined by the datasheet of the pump connected to the
        Coral. Currently a Swiftech Maelstrom D5 Series using a MCP655 / Laing
        D5 PWM motor.whose technical specifications available below [1] shows
        an RPM range of 800 - 4800.

            [1] https://www.swiftech.com/maelstrom-d5.aspx#tab3

        Another source of information may be the article published by
        TechPowerUp available below [2] which shows a graph for the D5 at PWM
        duty cycle of 0% at ~800 RPM and at duty cycle 100% at ~4500, somehow
        confirming the range.

            [2] https://www.techpowerup.com/reviews/Swiftech/MCP655/4.html

        """

        # FIXME:
        if WINDOWS:
            raise NotImplementedError()

            # Something with self._ohm_handler...
            # return {
            #     'overview': None,
            #     'value': None,
            #     'total': 4800,
            # }

        raise NotImplementedError()

    def collect_load_gpu(self):
        return {
            'value': self._gpu.load,
            'total': 100.0,
        }

    def collect_load_cpu(self):
        percent = psutil.cpu_percent()
        return {
            'value': percent,
            'total': 100.0,
        }

    def collect_memory(self):
        # Given in bytes, must pass in MB
        memory = psutil.virtual_memory()
        return {
            'value': memory.used / MB,
            'total': memory.total / MB,
        }

    def collect_network_rx(self):
        # Update network data just once, use it for RX and TX
        self._interface.update()

        return {
            # Given in bps, must pass in Mbps
            'value': self._interface.rx / MB,
            # Coral's uses motherboard (Gigabyte's Z370 AORUS Gaming 3 rev 1.0)
            # integrated network interface (Killer E2500 Gaming Network) which
            # is a gigabit Ethernet interface.
            'total': 1000.0,
        }

    def collect_network_tx(self):
        return {
            # Given in bps, must pass in Mbps
            'value': self._interface.tx / MB,
            # Full-duplex, right?
            'total': 1000.0,
        }

    def collect_disk_os(self):
        # Given in bytes, must pass in GB
        usage = psutil.disk_usage(PATH_OS)
        return {
            'value': usage.used / GB,
            'total': usage.total / GB,
        }

    def collect_disk_apps(self):
        # Given in bytes, must pass in GB
        usage = psutil.disk_usage(PATH_ARCHIVE)
        return {
            'value': usage.used / GB,
            'total': usage.total / GB,
        }


__all__ = [
    'CoralAgent',
]
