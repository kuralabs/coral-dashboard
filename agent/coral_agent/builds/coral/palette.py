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
Coral build dashboard color palette.
"""


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
temp_coolant left_label   | white, bold          |
temp_coolant right_label  | white, bold          |

temp_gpu background       |                      | black
temp_gpu bar1             |                      | light green
temp_gpu bar1 smooth      | light green          | black
temp_gpu bar2             |                      | dark green
temp_gpu bar2 smooth      | dark green           | black
temp_gpu left_label       | white, bold          |
temp_gpu right_label      | white, bold          |

temp_cpu background       |                      | black
temp_cpu bar1             |                      | light blue
temp_cpu bar1 smooth      | light blue           | black
temp_cpu bar2             |                      | dark blue
temp_cpu bar2 smooth      | dark blue            | black
temp_cpu left_label       | white, bold          |
temp_cpu right_label      | white, bold          |

# Load

load_gpu background       |                      | black
load_gpu bar1             |                      | dark gray
load_gpu bar1 smooth      | dark gray            | black
load_gpu bar2             |                      | dark green
load_gpu bar2 smooth      | dark green           | black
load_gpu left_label       | white, bold          |
load_gpu right_label      | white, bold          |

load_cpu background       |                      | black
load_cpu bar1             |                      | dark gray
load_cpu bar1 smooth      | dark gray            | black
load_cpu bar2             |                      | dark blue
load_cpu bar2 smooth      | dark blue            | black
load_cpu left_label       | white, bold          |
load_cpu right_label      | white, bold          |

# Memory

memory background         |                      | black
memory bar1               |                      | white
memory bar1 smooth        | white                | black
memory bar2               |                      | light gray
memory bar2 smooth        | light gray           | black
memory left_label         | white, bold          |
memory right_label        | white, bold          |

# Network

network_rx background     |                      | black
network_rx bar1           |                      | light magenta
network_rx bar1 smooth    | light magenta        | black
network_rx bar2           |                      | dark magenta
network_rx bar2 smooth    | dark magenta         | black
network_rx left_label     | white, bold          |
network_rx right_label    | white, bold          |

network_tx background     |                      | black
network_tx bar1           |                      | light magenta
network_tx bar1 smooth    | light magenta        | black
network_tx bar2           |                      | dark magenta
network_tx bar2 smooth    | dark magenta         | black
network_tx left_label     | white, bold          |
network_tx right_label    | white, bold          |

################
# Bar Styles   #
################

pump normal               | white                | dark gray
pump complete             | white                | dark red
pump smooth               | dark gray            | white
pump left_label           | white, bold          |
pump right_label          | white, bold          |

disk_os normal            | white                | dark gray
disk_os complete          | white                | dark cyan
disk_os smooth            | dark gray            | white
disk_os left_label        | white, bold          |
disk_os right_label       | white, bold          |

disk_apps normal          | white                | dark gray
disk_apps complete        | white                | brown
disk_apps smooth          | dark gray            | black
disk_apps left_label      | white, bold          |
disk_apps right_label     | white, bold          |

####################
#  General Styles  #
####################

section title             | black, bold          | white
popup                     | black, bold          | white
"""


__all__ = [
    'CORAL_PALETTE',
]
