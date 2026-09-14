# Fusion Topics

The fusion topics are managed by the `fusion` service which combines the radar and LiDAR point clouds with the vision model output.  The service implements a late-fusion pipeline which projects each sensor point onto the camera image using the camera intrinsics from `camera/info` and the sensor transforms from `tf_static`, and annotates the point with the class and instance of the detection box or segmentation mask it falls in.  The classified points are clustered into 3D bounding boxes and an occupancy grid.  The service can also run a [RadarExp](../../models/fusion/index.md) radar fusion model on the radar cube and camera frames.

- Radar and LiDAR late fusion with the [model output](model.md#modeloutput)
- 3D bounding boxes from the clustered points
- Occupancy grid
- RadarExp fusion model on the radar cube (TFLite)
- ByteTrack tracking of the fused objects

The fusion topics are published under the `fusion` namespace and offer the following sub-topics: `fusion/radar`, `fusion/lidar`, `fusion/occupancy`, `fusion/boxes3d`, and `fusion/model_output`.  Fusion parameters are configurable through the `fusion` service.  See the [fusion service configuration](../../platforms/configuration/fusion.md) documentation for details.  Topic names are relative to the device [hostname namespace](index.md#hostname-namespaces).

## fusion/radar

The `fusion/radar` topic publishes the radar points annotated with the vision classes using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema.  The point cloud contains the same fields and data as the input point cloud, by default `radar/targets` on the Raivin, and additional fields: `vision_class` and `instance_id`, plus `track_id` when the model output carries tracks.  The `vision_class` is the class of the radar point as determined by projection of the radar point onto the camera detection boxes or segmentation masks, and `instance_id` identifies which detected object the point belongs to.  If the input data is clustered, points with the same non-zero cluster ID will have the same class.  Points which do not project onto a detected object are marked unclassified.

| Field Name   | Datatype | Units | Notes                                                               |
| ------------ | -------- | ----- | ------------------------------------------------------------------- |
| x            | float32  | m     | Represent XYZ location of the point                                 |
| y            | float32  | m     | Represent XYZ location of the point                                 |
| z            | float32  | m     | Represent XYZ location of the point                                 |
| speed        | float32  | m/s   | Only measures speed towards or away from the radar                  |
| power        | float32  |       |                                                                     |
| rcs          | float32  |       | Radar cross section                                                 |
| cluster_id   | float32  |       | Present when the input is `radar/clusters`, 0 means not clustered   |
| vision_class | uint16   |       | Class index from the vision model, points in the same instance share the class |
| instance_id  | uint16   |       | Identifies the detected object the point belongs to                 |
| track_id     | uint32   |       | Present when tracking is enabled on the model service               |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.  The point coordinates are preserved from the input sensor frame and the message keeps the sensor frame ID.

This topic is only published when the fusion service is configured with a radar input topic.

## fusion/lidar

The `fusion/lidar` topic publishes the LiDAR points annotated with the vision classes using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema.  The point cloud contains the same fields and data as the input point cloud, `lidar/clusters` or `lidar/points`, and the same additional `vision_class`, `instance_id`, and optional `track_id` fields as `fusion/radar`.

| Field Name   | Datatype | Units | Notes                                                               |
|--------------|----------|-------|---------------------------------------------------------------------|
| x            | float32  | m     | Represent XYZ location of the point                                 |
| y            | float32  | m     | Represent XYZ location of the point                                 |
| z            | float32  | m     | Represent XYZ location of the point                                 |
| reflect      | uint8    |       | Intensity of the reflected LiDAR beam                               |
| cluster_id   | uint16   |       | Present when the input is `lidar/clusters`, 0 means not clustered   |
| vision_class | uint16   |       | Class index from the vision model                                   |
| instance_id  | uint16   |       | Identifies the detected object the point belongs to                 |
| track_id     | uint32   |       | Present when tracking is enabled on the model service               |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

This topic is only published when the fusion service is configured with a LiDAR input topic.

## fusion/occupancy

The `fusion/occupancy` topic publishes information about the location of detected objects using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema.  The grid source is selected with the `GRID_SRC` setting, radar by default.

The point cloud will have the fields `x`, `y`, `z`, `cluster_id`, `vision_class`, and `instance_id`.  If the input data is clustered, there will only be one point for each cluster id, located at the centroid of the cluster.  If the input data is not clustered, the points will be located at the center of cells on a radial grid, as defined by the [range and angle bins](../../platforms/configuration/fusion.md#occupancy-settings) of the fusion service configuration.

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

## fusion/boxes3d

The `fusion/boxes3d` topic publishes 3D bounding boxes for the detected objects using the custom [Detect](../api/edgefirst_msgs.md#detect) schema.  The boxes are built from the clustered sensor points assigned to each detected object, the source sensor is selected with the `BBOX3D_SRC` setting, radar by default on the Raivin.  Each box carries the label and score of the vision detection along with the distance and radial speed measured by the sensor, and the tracking information when tracking is enabled.  The message frame ID is the source sensor frame.

This topic is only published when the fusion service is configured with a 3D box source and the corresponding sensor input topic.

## fusion/model_output

The `fusion/model_output` topic publishes the output grid of the RadarExp fusion model with the custom [Mask](../api/edgefirst_msgs.md#mask) schema.  This contains the fusion model bird's eye view occupancy prediction as a mask which can be used to confirm the model is working as expected.  The grid geometry is described by the range and angle bins of the fusion service configuration.

When tracking is enabled on the fusion service, the `fusion/model_output/tracked` topic publishes the same grid after tracking the occupied cells over time with the same [Mask](../api/edgefirst_msgs.md#mask) schema.

These topics are only published when the fusion service is configured with a [radar fusion model](../../platforms/configuration/fusion.md#radar-fusion-model), which also requires the radar cube to be enabled.
