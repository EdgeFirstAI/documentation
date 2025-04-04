# GPS Topics

The GPS topic is managed by the `navsat` service and handles publishing the GPS location of the device.


The GPS topic is published under the `/gps` topic. Tracking parameters are configurable through the `navsat` service. See navsat service configuration documentation for details.

## /gps
The `/gps` topic publishes information about the device's position and altitude using the [NatSatFix](../api/sensor_msgs.md#navsatfix) schema.
