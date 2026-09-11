# IMU Topics

The imu topics are managed by the `imu` service and handles publishing the orientation of the device. The service also supports publishing the angular velocity and linear acceleration of the device

The imu topic is published under the `imu` topic, relative to the device [hostname namespace](index.md#hostname-namespaces), at the sensor report rate of roughly 100 to 140 Hz.  The sensor timeout and Zenoh settings are configured in `/etc/default/imu`, refer to [Configuration](../../platforms/configuration/index.md#configuration-files).

## imu

The `imu` topic publishes information about the device's orientation, angular velocity, and linear acceleration using the [Imu](../api/sensor_msgs.md#imu) schema.

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | [IMU Page](../../platforms/quickstart/maivin/webui.md#the-imu-page)
Foxglove | [IMU Data Plotting Example](../data_collection/foxglove.md#imu-data-plotting)
SDK | [IMU Example](../dev/examples/imu.md#imu-schema-example)
