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

from logging import getLogger as get_logger


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
        'title': 'Pump/Fans',
        'unit': 'RPM',
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
            'title': 'D:// "Storage"',
            'unit': 'GB',
        },
    ]
]

__all__ = [
    'CORAL_PALETTE',
    'CORAL_WIDGETS',
]
