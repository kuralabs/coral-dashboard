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
Helper to access included OpenHardwareMonitor functionality.

We actually use a build of its fork, LibreHardwareMonitor, which is better
maintained. Or better said, OHM is abandoned, but thankfully many required PRs
(like support for Coffee Lake) were merged in its fork long ago.

    https://github.com/LibreHardwareMonitor/LibreHardwareMonitor

This module has only been tested in Windows, and at least for Coral it is
only required in that OS.

We load the package included OpenHardwareMonitorLib.dll using "Python for .NET"
that allows to integrate Python and the .NET Common Language Runtime (CLR).

    https://github.com/pythonnet/pythonnet
"""

from pkg_resources import resource_filename

from clr import AddReference
AddReference(
    resource_filename(__package__, 'data/OpenHardwareMonitorLib.dll')
)

from OpenHardwareMonitor import Hardware  # noqa


class Computer:
    def __init__(self, features):
        self.handler = Hardware.Computer()

        for feature in features:
            feature_toggle = '{}Enabled'.format(feature)
            if not hasattr(self.handler, feature_toggle):
                raise ValueError('Unknown feature "{}"'.format(feature))
            setattr(self.handler, feature_toggle, True)

        self.handler.Open()


__all__ = [
    'Computer',
]
