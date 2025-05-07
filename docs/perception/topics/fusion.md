# Fusion Topics

The fusion topics are managed by the `fusion` service and handles running radar only and radar fused with camera machine learning models. The service supports RTM and RTLite (formerly TFLite) models. The service can classify radar points based on model output.

- RTM models
- RTLite models
- Camera projection

The model topics are published under the `/fusion` namespace and offers the following sub-topics: `/fusion/targets`, `/fusion/occupancy`, `/fusion/model_output`. Fusion parameters are configurable through the `fusion` service. See fusion service configuration documentation for details.


## /fusion/targets

The `/fusion/targets` topic publishes information about the received radar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will contain the same fields and data as the input point cloud (by default, `/radar/targets`), and two additional fields: `fusion_class` and `vision_class`. The two additional fields are both Float32 datatype, but the values is always integer. The `fusion_class` is the class of the radar point as determined by the radar fusion model. The `vision_class` is the class of the radar point as determined by projection of the radar point onto the camera segmentation. If the input data is clustered, points with the same non-zero cluster ID will have the same fusion/vision class. 

The XYZ coordinate system follows the input data.

## /fusion/occupancy

The `/fusion/targets` topic publishes information about location of detected objects using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema.

If the input data is clustered, the point cloud will have the fields `x`, `y`, `z`, `speed`, `vision_class`, `fusion_class`, `count` and `cluster_id`, all with the Float32 datatype. There will only be one point for each cluster id, located at the centriod of the cluster. The count will contain the number of points in the cluster. The values of the `vision_class`, `fusion_class`, `count` and `cluster_id` will be integer. The XYZ coordinate system follows the input data.

If the input data is not clustered, the point cloud will have the fields `x`, `y`, `z`, `speed`, `vision_class`, `fusion_class`, `count`, all with the Float32 datatype. The points will be located at the center of cells on a radial grid, as defined in the fusion service configuration. The count will contain the number of points in the cell. The values of the `vision_class`, `fusion_class`, `count` and `cluster_id` will be integer. The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up.

## /fusion/model_output
The `/fusion/targets` topic publishes information about the output grid the fusion model the custom [Mask](../api/edgefirst_msgs.md#mask) schema. This contains the fusion model output as a mask. This can be used to confirm the model is working as expected.