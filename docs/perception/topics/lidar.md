# LiDAR Topics

The lidar topics are managed by the `lidarpub` service and handles interfacing with a connected lidar to produce lidar point clouds, reflectivity maps, and depth maps. 

- Ouster OS1

The lidar topics are published under the `/lidar` namespace and offers the following sub-topics: `/lidar/points`, `/lidar/reflect`, `/lidar/depth`, and `/lidar/clusters`. The density of the lidar points, the frequency of updates, and the field of view of the lidar are configurable through the `lidarpub` service. See lidarpub service configuration documentation for details.

## /lidar/points
The `/lidar/points` topic publishes information about the lidar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will have the fields `x`, `y`, `z`, and `reflect`, all with the Float32 datatype. 

**Usage** | **Link**
:------------------:|:------------------:
WebUI | []()
Foxglove | [PointCloud2 Example]()
SDK | [Lidar Points Example](../dev/examples/lidar.md#lidar-points)

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up. However, note that the `lidar` frame is rotated 180 degrees from the `base_link` frame, with forward facing the back of the camera.

## /lidar/reflect
The `/lidar/reflect` topic publishes the reflectivity map using the [Image](../api/sensor_msgs.md#image) schema. The encoding of the image is `mono8`. The value of a pixel is the reflectivity of that point. The width of a pixel depends on the number of columns configured on the lidar. 

**Usage** | **Link**
:------------------:|:------------------:
WebUI | []()
Foxglove | [Image Example]()
SDK | [Lidar Reflect Example](../dev/examples/lidar.md#lidar-reflect)

## /lidar/depth
The `/lidar/depth` topic publishes the depth map using the [Image](../api/sensor_msgs.md#image) schema. The encoding of the image is `mono16`. The value of a pixel is the distance from the lidar to the point in millimeters. The width of a pixel depends on the number of columns configured on the lidar. 

**Usage** | **Link**
:------------------:|:------------------:
WebUI | []()
Foxglove | [Image Example]()
SDK | [Lidar Depth Example](../dev/examples/lidar.md#lidar-depth)

## /lidar/clusters
The `/lidar/clusters` topic publishes the lidar clusters pointcloud using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema.

**Usage** | **Link**
:------------------:|:------------------:
WebUI | []()
Foxglove | [PointCloud2 Example]()
SDK | [Lidar Clusters Example](../dev/examples/lidar.md#lidar-clusters)