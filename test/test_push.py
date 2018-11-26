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

from time import sleep
from random import randint, uniform

from requests import post


def test_push(dashboard):
    disk_os = 60
    disk_apps = 500

    while dashboard.returncode is None:
        # FIXME: Do not hardwire port, make class that parametrizes this
        data = {
            'temp_coolant': {
                'percent': uniform(24.0, 90.0),
                'value': None,
                'total': None,
            },
            'temp_gpu': {
                'percent': uniform(24.0, 90.0),
                'value': None,
                'total': None,
            },
            'temp_cpu': {
                'percent': uniform(24.0, 90.0),
                'value': None,
                'total': None,
            },
            'load_gpu': {
                'percent': uniform(0.0, 100.0),
                'value': None,
                'total': None,
            },
            'load_cpu': {
                'percent': uniform(0.0, 100.0),
                'value': None,
                'total': None,
            },
            'memory': {
                'percent': None,
                'value': randint(512, 4096),
                'total': 4096,
            },
            'network': {
                'percent': None,
                'value': randint(0, 1000),
                'total': 1000,
            },
            'pump': {
                'percent': None,
                'value': randint(600, 1400),
                'total': 1400,
            },
            'disk_os': {
                'percent': None,
                'value': disk_os,
                'total': 256,
            },
            'disk_apps': {
                'percent': None,
                'value': disk_apps,
                'total': 4096,
            },
        }

        try:
            response = post(  # noqa
                'http://localhost:5000/api/push',
                headers={
                    'user-agent': 'coral/testsuite',
                    'content-type': 'application/json',
                },
                json={"data": data},
            )

        # FIXME: Clean user shutdown of the test doesn't seems to be working
        except Exception as e:
            sleep(1)
            if dashboard.returncode is None:
                raise e

        disk_os += randint(0, 1)
        disk_apps += 1

        sleep(1)
