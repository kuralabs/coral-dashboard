You may update the OpenHardwareMonitorLib.dll from any updated build.

This was grabbed from the LibreHardwareMonitor project, which is a fork of the
original OpenHardwareMonitor that seems to be abandoned. LibreHardwareMonitor
seems alive and with more contributors and better support at the time of this
writing.

    https://github.com/LibreHardwareMonitor/LibreHardwareMonitor

OpenHardwareMonitorLib.dll is used to grab two metrics:

- CPU temperature from CPU itself.
- CPU FAN speed from motherboard controller.

Those metrics proved very difficult to grab in Windows. In particular because
the "recommended" approach involving "root\\wmi" fails to provide a correct
reading on many systems.
