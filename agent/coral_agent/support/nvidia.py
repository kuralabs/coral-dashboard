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
Helper to access Nvidia GPU metrics using their NVML API.

    https://docs.nvidia.com/deploy/nvml-api/index.html

This requires Nvidia propietary drivers installed in the system.
"""

from collections import OrderedDict
from logging import getLogger as get_logger

from py3nvml import py3nvml as nvml
nvml.nvmlInit()


log = get_logger(__name__)


class NvidiaGPU:

    def __init__(self, pci_bus_id=None, index=None):
        if pci_bus_id is not None:
            self.handle = nvml.nvmlDeviceGetHandleByPciBusId(pci_bus_id)
        else:
            if index is None:
                index = 0
            self.handle = nvml.nvmlDeviceGetHandleByIndex(index)

    @property
    def load(self):
        rates = nvml.nvmlDeviceGetUtilizationRates(self.handle)
        return float(rates.gpu)  # int between 0-100

    @property
    def temperature(self):
        temperature = nvml.nvmlDeviceGetTemperature(
            self.handle,
            0,  # nvmlTemperatureSensors_t.NVML_TEMPERATURE_GPU
        )
        return float(temperature)  # int celsius

    @property
    def threshold_shutdown(self):
        threshold = nvml.nvmlDeviceGetTemperatureThreshold(
            self.handle,
            0,  # NVML_TEMPERATURE_THRESHOLD_SHUTDOWN
        )
        return float(threshold)

    @property
    def threshold_slowdown(self):
        threshold = nvml.nvmlDeviceGetTemperatureThreshold(
            self.handle,
            1,  # NVML_TEMPERATURE_THRESHOLD_SLOWDOWN
        )
        return float(threshold)

    @property
    def name(self):
        return nvml.nvmlDeviceGetName(self.handle)

    @classmethod
    def available_devices(cls):

        devices = OrderedDict()

        device_count = nvml.nvmlDeviceGetCount()
        for i in range(device_count):
            handle = nvml.nvmlDeviceGetHandleByIndex(i)

            devices[i] = {
                'name': nvml.nvmlDeviceGetName(handle),
                'pci_bus_id': nvml.nvmlDeviceGetPciInfo(handle).busId,
            }

        return devices


__all__ = [
    'NvidiaGPU',
]
