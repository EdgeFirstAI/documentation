# Radar Topics

The radar topics are managed by the `radarpub` service and handles interfacing with a connected radar to produce radar point clouds and radar cubes.  The service can also stack successive radar points and cluster radar points based on their proximity to each other.  The service publishes the static transform from the `base_link` frame to the `radar` frame on the `tf_static` topic.  The following is a list of key features provided by the radar service.

- SmartMicro Radars
- Output raw Radarcube
- DBScan clustering of radar points

The radar topics are published under the `radar` namespace and offer the following sub-topics: `radar/targets`, `radar/clusters`, `radar/cube`, and `radar/info`.  Clustering parameters are configurable through the `radarpub` service, see the [radar service configuration](../../platforms/configuration/radar.md) documentation for details.  Topic names are relative to the device [hostname namespace](index.md#hostname-namespaces).

## radar/targets

The `/radar/targets` topic publishes information about the received radar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will have the fields `x`, `y`, `z`, `speed`, `power`, and `rcs` (radar cross section), all with the Float32 datatype.

| Field Name | Datatype | Units | Notes                                              |
|------------|----------|-------|----------------------------------------------------|
| x          | float32  | m     | Represent XYZ location of the point                |
| y          | float32  | m     | Represent XYZ location of the point                |
| z          | float32  | m     | Represent XYZ location of the point                |
| speed      | float32  | m/s   | Only measures speed towards or away from the radar |
| power      | float32  |       |                                                    |
| rcs        | float32  |       | Radar cross section                                |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | [Radar Page](../../platforms/quickstart/raivin/webui.md#the-radar-page) |
| Foxglove | [3D Panel](https://docs.foxglove.dev/docs/visualization/panels/3d) |
| SDK | [Radar Targets Example](../dev/examples/radar.md#radar-targets) |

## radar/clusters

The `/radar/clusters` topic publishes information about the received radar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will have the fields `x`, `y`, `z`, `speed`, `power`, `rcs` (radar cross section), and `cluster_id`.

| Field Name | Datatype | Units | Notes                                                                                              |
|------------|----------|-------|----------------------------------------------------------------------------------------------------|
| x          | float32  | m     | Represent XYZ location of the point                                                                |
| y          | float32  | m     | Represent XYZ location of the point                                                                |
| z          | float32  | m     | Represent XYZ location of the point                                                                |
| speed      | float32  | m/s   | Only measures speed towards or away from the radar                                                 |
| power      | float32  |       |                                                                                                    |
| rcs        | float32  |       | Radar cross section                                                                                |
| cluster_id | float32  |       | Will always be integer valued. 0 means not clustered. Otherwise same cluster id means same cluster |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

This topic is only published if the radarpub service is configured with the [clustering](../../platforms/configuration/radar.md#clustering) task enabled.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | [Radar Page](../../platforms/quickstart/raivin/webui.md#the-radar-page) |
| Foxglove | [3D Panel](https://docs.foxglove.dev/docs/visualization/panels/3d) |
| SDK | [Radar Clusters Example](../dev/examples/radar.md#radar-clusters) |

## radar/cube

The `/radar/cube` topic publishes information about the received radar sensor data using the custom [RadarCube](../api/edgefirst_msgs.md#radarcube) schema.

!!! note

    This topic is only published if the radarpub service is configured with the [radar cube](../../platforms/configuration/radar.md#enable-cube) publishing enabled.  The cube consumes about 240 Mbps on the sensor Ethernet link and a CPU core, enable it only when training or running a RadarExp fusion model.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | |
| Foxglove | [Viewing Radar Cube](../data_collection/foxglove.md#viewing-radarcube-messages) |
| SDK | [Radar Cube Example](../dev/examples/radar.md#radar-cube) |

## radar/info

The `/radar/info` topic publishes information about the current radar configuration using the custom [RadarInfo](../api/edgefirst_msgs.md#radarinfo) schema. It describes the state of the center frequency, frequency sweep, range toggle, and detection sensitivity of the radar.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | |
| Foxglove | Raw Messages panel |
| SDK | [Radar Info Example](../dev/examples/radar.md#radar-info) |
