# LiDAR Topics

The lidar topics are managed by the `lidarpub` service and handles interfacing with a connected lidar to produce lidar point clouds, reflectivity maps, and depth maps.  The service can cluster the point cloud and remove the ground plane before clustering, and publishes the static transform from the `base_link` frame to the `lidar` frame on the `tf_static` topic.

- Robosense E1R
- Ouster OS1
- DBSCAN and voxel clustering
- IMU-guided ground plane filter

The lidar topics are published under the `lidar` namespace and offer the following sub-topics: `lidar/points`, `lidar/reflect`, `lidar/depth`, and `lidar/clusters`.  The sensor type, the density of the lidar points, the frequency of updates, the field of view, and the clustering are configurable through the `lidarpub` service, see the [LiDAR service configuration](../../platforms/configuration/lidar.md) documentation for details.  Topic names are relative to the device [hostname namespace](index.md#hostname-namespaces).

## lidar/points

The `/lidar/points` topic publishes information about the lidar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will have the fields `x`, `y`, `z`, and `reflect`.

| Field Name | Datatype | Units | Notes                               |
|------------|----------|-------|-------------------------------------|
| x          | float32  | m     | Represent XYZ location of the point |
| y          | float32  | m     | Represent XYZ location of the point |
| z          | float32  | m     | Represent XYZ location of the point |
| reflect    | uint8    |       | Intensity of reflected LiDAR beam   |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.  Note that the Ouster `lidar` frame is rotated 180 degrees from the `base_link` frame as its 0 degree point is at the rear connector, the transform published on `tf_static` accounts for the mounting.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | [LiDAR Page](../../platforms/quickstart/raivin/webui.md#the-lidar-page) |
| Foxglove | [PointCloud2 Example](https://docs.foxglove.dev/docs/visualization/panels/3d) |
| SDK | [LiDAR Points Example](../dev/examples/lidar.md#lidar-points) |

## lidar/reflect

The `/lidar/reflect` topic publishes the reflectivity map using the [Image](../api/sensor_msgs.md#image) schema. The encoding of the image is `mono8`. The value of a pixel is the reflectivity of that point. The image width depends on the number of columns configured on the lidar.  These images are published for the Ouster sensor.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | |
| Foxglove | [Image Example](https://docs.foxglove.dev/docs/visualization/panels/image) |
| SDK | [LiDAR Reflect Example](../dev/examples/lidar.md#lidar-reflect) |

## lidar/depth

The `/lidar/depth` topic publishes the depth map using the [Image](../api/sensor_msgs.md#image) schema. The encoding of the image is `mono16`. The value of a pixel is the distance from the lidar to the point in millimeters. The image width depends on the number of columns configured on the lidar.  These images are published for the Ouster sensor.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | |
| Foxglove | [Image Example](https://docs.foxglove.dev/docs/visualization/panels/image) |
| SDK | [LiDAR Depth Example](../dev/examples/lidar.md#lidar-depth) |

## lidar/clusters

The `/lidar/clusters` topic publishes the lidar clusters pointcloud using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will have the fields `x`, `y`, `z`, `cluster_id`, and `reflect`.

| Field Name | Datatype | Units | Notes                                                                |
|------------|----------|-------|----------------------------------------------------------------------|
| x          | float32  | m     | Represent XYZ location of the point                                  |
| y          | float32  | m     | Represent XYZ location of the point                                  |
| z          | float32  | m     | Represent XYZ location of the point                                  |
| cluster_id | uint16   |       | 0 means not clustered.  Otherwise same cluster id means same cluster |
| reflect    | uint8    |       | Intensity of reflected LiDAR beam                                    |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.  Note that the Ouster `lidar` frame is rotated 180 degrees from the `base_link` frame as its 0 degree point is at the rear connector, the transform published on `tf_static` accounts for the mounting.

This topic is only published if the lidarpub service is configured with a [clustering](../../platforms/configuration/lidar.md#clustering) algorithm.

| **Usage** | **Link** |
|:------------------:|:------------------:|
| Web UI | [LiDAR Page](../../platforms/quickstart/raivin/webui.md#the-lidar-page) |
| Foxglove | [PointCloud2 Example](https://docs.foxglove.dev/docs/visualization/panels/3d) |
| SDK | [LiDAR Clusters Example](../dev/examples/lidar.md#lidar-clusters) |
