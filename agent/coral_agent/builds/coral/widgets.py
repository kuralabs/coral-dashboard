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
Coral build dashboard widgets definition.

Semantics of the widgets:

- None -> Divider
- String -> Section Title
- Dictionary -> Widget: Graph or Bar
- List -> Columns

"""


CORAL_WIDGETS = [
    'Temperature',
    [
        {
            'widget': 'graph',
            'identifier': 'temp_coolant',
            'left_tpl': 'Coolant',
            'right_tpl': '{value:.0f}°C/{total:.0f}Max',
        }, {
            'widget': 'graph',
            'identifier': 'temp_gpu',
            'left_tpl': 'GPU',
            'right_tpl': '{value:.0f}°C/{total:.0f}TJM',
        }, {
            'widget': 'graph',
            'identifier': 'temp_cpu',
            'left_tpl': 'CPU',
            'right_tpl': '{value:.0f}°C/{total:.0f}TJM',
        },
    ],
    None,
    {
        'widget': 'bar',
        'identifier': 'pump',
        'left_tpl': 'Pump',
        'right_tpl': '{quotient:.1f}% [{value:.0f}/{total:.0f}]RPM',
    },
    None,
    'Load',
    [
        {
            'widget': 'graph',
            'identifier': 'load_gpu',
            'left_tpl': 'GPU',
            'right_tpl': '{quotient:.1f}%',
        }, {
            'widget': 'graph',
            'identifier': 'load_cpu',
            'left_tpl': 'CPU',
            'right_tpl': '{quotient:.1f}%',
        },
    ],
    None,
    'Memory',
    {
        'widget': 'graph',
        'identifier': 'memory',
        'left_tpl': 'Memory',
        'right_tpl': '{quotient:.1f}% [{value:.0f}/{total:.0f}]MB',
    },
    None,
    'Network',
    [
        {
            'widget': 'graph',
            'identifier': 'network_rx',
            'left_tpl': 'Download',
            'right_tpl': '{value:.0f}Mbps',
        }, {
            'widget': 'graph',
            'identifier': 'network_tx',
            'left_tpl': 'Upload',
            'right_tpl': '{value:.0f}Mbps',
        },
    ],
    None,
    'Disk',
    [
        {
            'widget': 'bar',
            'identifier': 'disk_os',
            'left_tpl': '"OS"',
            'right_tpl': '{quotient:.1f}% [{value:.0f}/{total:.0f}]GB',
        }, {
            'widget': 'bar',
            'identifier': 'disk_apps',
            'left_tpl': '"Archive"',
            'right_tpl': '{quotient:.1f}% [{value:.0f}/{total:.0f}]GB',
        },
    ]
]


__all__ = [
    'CORAL_WIDGETS',
]
