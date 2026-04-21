# Radar Topics

The radar topics are managed by the `radarpub` service and handles interfacing with a connected radar to produce radar point clouds and radar cubes.  The service can also stack successive radar points and cluster radar points based on their proximity to each other.  The following is a list of key features provided by the radar service.

- SmartMicro Radars
- Output raw Radarcube
- DBScan clustering of radar points

The radars topics are published under the `/radar` namespace and offers the following sub-topics: `/radar/targets`, `/radar/clusters`, `/radar/cube`, and `/radar/info`. Clustering parameters are configurable through the `radarpub` service. See radarpub service configuration documentation for details.

## /radar/info

The `/radar/info` topic publishes information about the current radar configuration. It describes the state of the center frequency, frequency sweep, range toggle, and detection frequency of the radar.

## /radar/targets

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

**Usage** | **Link**
:------------------:|:------------------:
Web UI | []()
Foxglove | []()
SDK | [Radar Targets Example](../dev/examples/radar.md#radar-targets)

## /radar/clusters

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

This topic is only published if the radarpub service is configured with the clustering task enabled.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | []()
Foxglove | []()
SDK | [Radar Clusters Example](../dev/examples/radar.md#radar-clusters)

## /radar/cube

The `/radar/cube` topic publishes information about the received radar sensor data using the custom [RadarCube](../api/edgefirst_msgs.md#radarcube) schema.

!!! note

    This topic is only published if the radarpub service is configured with the radar cube publishing enabled.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | []()
Foxglove | [Viewing Radar Cube](../data_collection/foxglove.md#viewing-radarcube-messages)
SDK | [Radar Cube Example](../dev/examples/radar.md#radar-cube)

## /radar/info

The `/radar/info` topic publishes information about the current radar configuration. It describes the state of the center frequency, frequency sweep, range toggle, and detection frequency of the radar.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | []()
Foxglove | []()
SDK | [Radar Info Example](../dev/examples/radar.md#radar-info)
