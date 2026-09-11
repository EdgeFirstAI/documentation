# GPS Topics

The GPS topic is managed by the `navsat` service and handles publishing the GPS location of the device.  The service reads the position from the `gpsd` daemon which interfaces with the GNSS receiver, the receiver also disciplines the system clock through `chrony`.

The GPS topic is published under the `gps` topic, relative to the device [hostname namespace](index.md#hostname-namespaces).  The topic name and the `gpsd` address are configurable in `/etc/default/navsat`.

## gps

The `gps` topic publishes information about the device's position and altitude using the [NavSatFix](../api/sensor_msgs.md#navsatfix) schema.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | [GPS Page](../../platforms/quickstart/maivin/webui.md#the-gps-page)
Foxglove | [Map Example](https://docs.foxglove.dev/docs/visualization/panels/map)
SDK | [GPS Example](../dev/examples/gps.md#gps-schema-example)
