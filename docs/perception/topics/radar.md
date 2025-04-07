# Radar Topics

The radar topics are managed by the `radarpub` service and handles interfacing with a conencted radar to produce radar point clouds and radar cubes.  The service can also stack successive radar points and cluster radar points based on their proximity to each other.  The following is a list of key features provided by the radar service.

- SmartMicro Radars
- Output raw Radarcube
- DBScan clustering of radar points

The radars topics are published under the `/radar` namespace and offers the following sub-topics: `/radar/targets`, `/radar/clusters`, `/radar/cube`, and `/radar/info`. Clustering parameters are configurable through the `radarpub` service. See radarpub service configuration documentation for details.

## /radar/targets

The `/radar/targets` topic publishes information about the received radar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will have the fields `x`, `y`, `z`, `speed`, `power`, and `rcs` (radar cross section), all with the Float32 datatype. 

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

## /radar/clusters
The `/radar/clusters` topic publishes information about the received radar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will have the fields `x`, `y`, `z`, `speed`, `power`, `rcs` (radar cross section), and `cluster_id`, all with the Float32 datatype. While `cluster_id` is formatted as a Float32 datatype, the values contained by the field will be an integer. A cluster ID of 0 means the point is not considered in a cluster, otherwise any points with the same cluster ID are in the same cluster.

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up. 

This topic is only published if the radarpub service is configured with the clustering task enabled.

## /radar/cube
The `/radar/cube` topic publishes information about the received radar sensor data using the custom [RadarCube](../api/edgefirst_msgs.md#radarcube) schema. 


This topic is only published if the radarpub service is configured with the radar cube task enabled.

## /radar/info
The `/radar/info` topic publishes information about the current radar configuration. It describes the state of the center frequency, frequency sweep, range toggle, and detection frequency of the radar. 