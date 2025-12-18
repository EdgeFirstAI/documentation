# GPS Topics

The GPS topic is managed by the `navsat` service and handles publishing the GPS location of the device.

The GPS topic is published under the `/gps` topic.

## /gps

The `/gps` topic publishes information about the device's position and altitude using the [NatSatFix](../api/sensor_msgs.md#navsatfix) schema.

**Usage** | **Link**
:------------------:|:------------------:
WebUI | []()
Foxglove | [Map Example](https://docs.foxglove.dev/docs/visualization/panels/map)
SDK | [GPS Example](../dev/examples/gps.md#gps-schema-example)
