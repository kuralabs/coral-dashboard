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
Helper to collect network metrics.
"""

from time import time
from logging import getLogger as get_logger

from psutil import net_io_counters


log = get_logger(__name__)


class Interface:

    def __init__(self, interface):

        if interface not in self.__class__.interfaces():
            raise ValueError(
                'Unknown interface "{}"'.format(interface)
            )

        self._interface = interface
        self._network_cache = None
        self._network_data = None
        self._update_network_cache()

    @classmethod
    def interfaces(cls):
        return list(net_io_counters(pernic=True).keys())

    def _update_network_cache(self):
        counters = net_io_counters(pernic=True)[self._interface]

        # Fetch current statistics
        ctime = time()
        cstats = {
            key: getattr(counters, key)
            for key in ('bytes_recv', 'bytes_sent')
        }

        self._network_cache = {
            'time': ctime,
            'stats': cstats,
        }

    def _update_network_data(self):
        """
        psutil's net_io_counters() gives us bytes sent and received at the
        interface since boot, thankfully handling overflow. We want to
        transform this value to an average transmission rate in bits per
        second in the latest sampling frequency window.
        """

        # Fetch old statistics
        otime = self._network_cache['time']
        ostats = self._network_cache['stats']

        # Fetch current statistics
        self._update_network_cache()
        ctime = self._network_cache['time']
        cstats = self._network_cache['stats']

        # Calculate deltas
        dtime = ctime - otime
        dstats = {
            # First, calculate the difference of bytes transfered between
            # before and now. Then, divide the difference by the elapsed time,
            # which will give you the average bytes transfered in a second.
            # Convert that to bits (multiply by 8) and we are done.
            key: int(((cstats[key] - ostats[key]) / dtime) * 8)
            for key in ostats.keys()
        }

        # Update last network deltas
        self._network_data = dstats

    def update(self):
        self._update_network_data()

    @property
    def rx(self):
        return self._network_data['bytes_recv']

    @property
    def tx(self):
        return self._network_data['bytes_sent']


__all__ = [
    'Interface',
]
