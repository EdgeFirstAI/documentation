# IMU Topics

The imu topics are managed by the `imu` service and handles publishing the orientation of the device. The service also supports publishing the angular velocity and linear acceleration of the device

The imu topic is published under the `/imu` topic.

## /imu

The `/imu` topic publishes information about the device's orientation, angular velocity, and linear acceleration using the [Imu](../api/sensor_msgs.md#imu) schema.

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

**Usage** | **Link**
:------------------:|:------------------:
WebUI | []()
Foxglove | [IMU Data Plotting Example](../../platforms/foxglove.md#imu-data-plotting)
SDK | [IMU Example](../dev/examples/imu.md#imu-schema-example)
