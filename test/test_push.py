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
from logging import getLogger as get_logger

from requests import post
from requests.exceptions import ConnectionError


log = get_logger(__name__)


def test_push(dashboard):
    endpoint = 'http://localhost:{}/api/push'.format(dashboard.port)

    disk_os = 60
    disk_apps = 500

    while dashboard.is_alive():
        data = {
            'temp_coolant': {
                'overview': uniform(24.0, 90.0),
                'value': None,
                'total': None,
            },
            'temp_gpu': {
                'overview': uniform(24.0, 90.0),
                'value': None,
                'total': None,
            },
            'temp_cpu': {
                'overview': uniform(24.0, 90.0),
                'value': None,
                'total': None,
            },
            'load_gpu': {
                'overview': uniform(0.0, 100.0),
                'value': None,
                'total': None,
            },
            'load_cpu': {
                'overview': uniform(0.0, 100.0),
                'value': None,
                'total': None,
            },
            'memory': {
                'overview': None,
                'value': randint(512, 4096),
                'total': 4096,
            },
            'network': {
                'overview': None,
                'value': randint(0, 1000),
                'total': 1000,
            },
            'pump': {
                'overview': None,
                'value': randint(600, 1400),
                'total': 1400,
            },
            'disk_os': {
                'overview': None,
                'value': disk_os,
                'total': 256,
            },
            'disk_apps': {
                'overview': None,
                'value': disk_apps,
                'total': 4096,
            },
        }

        try:
            response = post(
                endpoint,
                headers={
                    'user-agent': 'coral/testsuite',
                    'content-type': 'application/json',
                },
                json={'data': data},
            )
            assert response.status_code == 200

        except ConnectionError as e:
            if dashboard.is_alive():
                raise e

        disk_os += randint(0, 1)
        disk_apps += 1

        sleep(1)
