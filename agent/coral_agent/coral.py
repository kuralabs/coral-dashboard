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
Coral palette and UI description module.
"""

from sys import platform
from collections import OrderedDict
from logging import getLogger as get_logger

from .agent import GenericAgent
from .palette import parse_palette


log = get_logger(__name__)


CORAL_PALETTE = """
STYLE NAME                | FOREGROUND           | BACKGROUND
========================================================================

################
# Graph Styles #
################

# Temperature

temp_coolant background   |                      | black
temp_coolant bar1         |                      | light red
temp_coolant bar1 smooth  | light red            | black
temp_coolant bar2         |                      | dark red
temp_coolant bar2 smooth  | dark red             | black
temp_coolant title        | white, bold          |
temp_coolant label        | white, bold          |

temp_gpu background       |                      | black
temp_gpu bar1             |                      | light green
temp_gpu bar1 smooth      | light green          | black
temp_gpu bar2             |                      | dark green
temp_gpu bar2 smooth      | dark green           | black
temp_gpu title            | white, bold          |
temp_gpu label            | white, bold          |

temp_cpu background       |                      | black
temp_cpu bar1             |                      | light blue
temp_cpu bar1 smooth      | light blue           | black
temp_cpu bar2             |                      | dark blue
temp_cpu bar2 smooth      | dark blue            | black
temp_cpu title            | white, bold          |
temp_cpu label            | white, bold          |

# Load

load_gpu background       |                      | black
load_gpu bar1             |                      | dark gray
load_gpu bar1 smooth      | dark gray            | black
load_gpu bar2             |                      | dark green
load_gpu bar2 smooth      | dark green           | black
load_gpu title            | white, bold          |
load_gpu label            | white, bold          |

load_cpu background       |                      | black
load_cpu bar1             |                      | dark gray
load_cpu bar1 smooth      | dark gray            | black
load_cpu bar2             |                      | dark blue
load_cpu bar2 smooth      | dark blue            | black
load_cpu title            | white, bold          |
load_cpu label            | white, bold          |

# Memory

memory background         |                      | black
memory bar1               |                      | white
memory bar1 smooth        | white                | black
memory bar2               |                      | light gray
memory bar2 smooth        | light gray           | black
memory title              | white, bold          |
memory label              | white, bold          |

# Network

network background        |                      | black
network bar1              |                      | light magenta
network bar1 smooth       | light magenta        | black
network bar2              |                      | dark magenta
network bar2 smooth       | dark magenta         | black
network title             | white, bold          |
network label             | white, bold          |

################
# Bar Styles   #
################

pump normal               | white                | dark gray
pump complete             | white                | dark red
pump smooth               | dark gray            | white
pump title                | white, bold          |
pump label                | white, bold          |

disk_os normal            | white                | dark gray
disk_os complete          | white                | dark cyan
disk_os smooth            | dark gray            | white
disk_os title             | white, bold          |
disk_os label             | white, bold          |

disk_apps normal          | white                | dark gray
disk_apps complete        | white                | brown
disk_apps smooth          | dark gray            | black
disk_apps title           | white, bold          |
disk_apps label           | white, bold          |

####################
#  General Styles  #
####################

section title             | black, bold          | white
popup                     | black, bold          | white
"""


# None - Divider
# String - Text
# (WidgetType, identifier, title, unit) - Widget
# [Widgets] - Columns
CORAL_WIDGETS = [
    'Temperature',
    [
        {
            'widget': 'graph',
            'identifier': 'temp_coolant',
            'title': 'Coolant',
            'unit': '°C',
            'symbol': '°',
        }, {
            'widget': 'graph',
            'identifier': 'temp_gpu',
            'title': 'GPU',
            'unit': '°C',
            'symbol': '°',
        }, {
            'widget': 'graph',
            'identifier': 'temp_cpu',
            'title': 'CPU',
            'unit': '°C',
            'symbol': '°',
        },
    ],
    None,
    {
        'widget': 'bar',
        'identifier': 'pump',
        'title': 'Pump',
        'unit': 'RPM',
        # maxvalue is determined by the datasheet of the pump connected
        # to the Coral. Currently a Swiftech Maelstrom D5 Series using a
        # MCP655 / Laing D5 PWM motor.whose technical specifications available
        # below [1] shows an RPM range of 800 - 4800.
        #
        #     [1] https://www.swiftech.com/maelstrom-d5.aspx#tab3
        #
        # Another source of information may be the article published by
        # TechPowerUp available below [2] which shows a graph for the D5 at PWM
        # duty cycle of 0% at ~800 RPM and at duty cycle 100% at ~4500, somehow
        # confirming the range.
        #
        #     [2] https://www.techpowerup.com/reviews/Swiftech/MCP655/4.html
        #
        'maxvalue': 4800,
    },
    None,
    'Load',
    [
        {
            'widget': 'graph',
            'identifier': 'load_gpu',
            'title': 'GPU',
            'unit': '%',
        }, {
            'widget': 'graph',
            'identifier': 'load_cpu',
            'title': 'CPU',
            'unit': '%',
        },
    ],
    None,
    'Memory',
    {
        'widget': 'graph',
        'identifier': 'memory',
        'title': 'Memory',
        'unit': 'MB',
    },
    None,
    'Network',
    {
        'widget': 'graph',
        'identifier': 'network',
        'title': 'Network',
        'unit': 'Mbps',
    },
    None,
    'Disk',
    [
        {
            'widget': 'bar',
            'identifier': 'disk_os',
            'title': 'C:// "Windows"',
            'unit': 'GB',
        }, {
            'widget': 'bar',
            'identifier': 'disk_apps',
            'title': 'D:// "Archive"',
            'unit': 'GB',
        },
    ]
]


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


KB = 1024
MB = KB ** 2
GB = KB ** 3


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

        import psutil
        self._psutil = psutil

        from py3nvml import py3nvml as nv
        self._nv = nv
        self._nv.nvmlInit()
        self._gpu = self._nv.nvmlDeviceGetHandleByIndex(0)

        # [Windows] Open OpenHardwareMonitorLib.dll from package data
        self._ohm_handler = None

        if platform == 'win32':
            from clr import AddReference
            from pkg_resources import resource_filename
            AddReference(
                resource_filename(__package__, 'OpenHardwareMonitorLib.dll')
            )

            from OpenHardwareMonitor import Hardware

            handler = Hardware.Computer()
            handler.MainboardEnabled = True
            handler.CPUEnabled = True
            handler.Open()

            self._ohm_handler = handler

    def collect_temp_coolant(self):
        raise NotImplementedError()

    def collect_temp_gpu(self):
        temperature = self._nv.nvmlDeviceGetTemperature(
            self._gpu,
            0,  # nvmlTemperatureSensors_t.NVML_TEMPERATURE_GPU
        )
        return {
            'overview': float(temperature),  # int celsius
            'value': None,
            'total': None,
        }

    def collect_temp_cpu(self):
        # FIXME:
        if platform == 'win32':
            raise NotImplementedError()

            # Something with self._ohm_handler...
            # return {
            #     'overview': None,
            #     'value': None,
            #     'total': None,
            # }

        raise NotImplementedError()

    def collect_pump(self):
        # FIXME:
        if platform == 'win32':
            raise NotImplementedError()

            # Something with self._ohm_handler...
            # return {
            #     'overview': None,
            #     'value': None,
            #     'total': None,
            # }

        raise NotImplementedError()

    def collect_load_gpu(self):
        rates = self._nv.nvmlDeviceGetUtilizationRates(self._gpu)
        return {
            'overview': float(rates.gpu),  # int between 0-100
            'value': None,
            'total': None,
        }

    def collect_load_cpu(self):
        percent = self._psutil.cpu_percent()
        return {
            'overview': percent,
            'value': None,
            'total': None,
        }

    def collect_memory(self):
        # Given in bytes, must pass in MB
        memory = self._psutil.virtual_memory()
        return {
            'overview': None,
            'value': memory['used'] / MB,
            'total': memory['total'] / MB,
        }

    def collect_network(self):
        raise NotImplementedError()

    def collect_disk_os(self):
        # Given in bytes, must pass in GB
        usage = self._psutil.disk_usage('C:\\')
        return {
            'overview': None,
            'value': usage['used'] / GB,
            'total': usage['total'] / GB,
        }

    def collect_disk_apps(self):
        # Given in bytes, must pass in GB
        usage = self._psutil.disk_usage('D:\\')
        return {
            'overview': None,
            'value': usage['used'] / GB,
            'total': usage['total'] / GB,
        }


__all__ = [
    'CORAL_PALETTE',
    'CORAL_WIDGETS',
    'CoralAgent',
]
