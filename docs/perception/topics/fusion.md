# Fusion Topics

The fusion topics are managed by the `fusion` service and handles running radar only and radar fused with camera machine learning models. The service supports RTM and RTLite (formerly TFLite) models. The service can classify radar points based on model output.

- RTM models
- RTLite models
- Camera projection

The model topics are published under the `/fusion` namespace and offers the following sub-topics: `/fusion/targets`, `/fusion/occupancy`, `/fusion/model_output`. Fusion parameters are configurable through the `fusion` service. See fusion service configuration documentation for details.


## /fusion/radar

The `/fusion/radar` topic publishes information about the received radar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will contain the same fields and data as the input point cloud (by default, `/radar/clusters`), and two additional fields: `fusion_class` and `vision_class`. The two additional fields are both Float32 datatype, but the values is always integer. The `fusion_class` is the class of the radar point as determined by the radar fusion model. The `vision_class` is the class of the radar point as determined by projection of the radar point onto the camera segmentation. If the input data is clustered, points with the same non-zero cluster ID will have the same fusion/vision class. 

| Field Name   | Datatype | Units | Notes                                                               |
| ------------ | -------- | ----- | ------------------------------------------------------------------- |
| x            | float32  | m     | Represent XYZ location of the point                                 |
| y            | float32  | m     | Represent XYZ location of the point                                 |
| z            | float32  | m     | Represent XYZ location of the point                                 |
| speed        | float32  | m/s   | Only measures speed towards or away from the radar                  |
| power        | float32  |       |                                                                     |
| rcs          | float32  |       | Radar cross section                                                 |
| cluster_id   | uint16   |       | 0 means not clustered. Otherwise same cluster id means same cluster |
| fusion_class | uint8    |       | Points in the same cluster will have the same class                 |
| vision_class | uint8    |       | Points in the same cluster will have the same class                 |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up. 

## /fusion/lidar

The `/fusion/lidar` topic publishes information about the received lidar points using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema. The point cloud will contain the same fields and data as the input point cloud (by default, `/lidar/clusters`), and two additional fields: `fusion_class` and `vision_class`. The `fusion_class` is the class of the radar point as determined by the radar fusion model. The `vision_class` is the class of the radar point as determined by projection of the radar point onto the camera segmentation. If the input data is clustered, points with the same non-zero cluster ID will have the same fusion/vision class. 

| Field Name   | Datatype | Units | Notes                                                               |
|--------------|----------|-------|---------------------------------------------------------------------|
| x            | float32  | m     | Represent XYZ location of the point                                 |
| y            | float32  | m     | Represent XYZ location of the point                                 |
| z            | float32  | m     | Represent XYZ location of the point                                 |
| reflect      | uint8    |       | Only measures speed towards or away from the radar                  |
| cluster_id   | uint16   |       | 0 means not clustered. Otherwise same cluster id means same cluster |
| fusion_class | uint8    |       | Points in the same cluster will have the same class                 |
| vision_class | uint8    |       | Points in the same cluster will have the same class                 |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up. 

## /fusion/occupancy

The `/fusion/occupancy` topic publishes information about location of detected objects using the [PointCloud2](../api/sensor_msgs.md#pointcloud2) schema.

The point cloud will have the fields `x`, `y`, `z`, `cluster_id`, `vision_class`, `fusion_class`. If the input data is clustered, there will only be one point for each cluster id, located at the centroid of the cluster. If the input data is not clustered, the points will be located at the center of cells on a radial grid, as defined in the fusion service configuration.

| Field Name   | Datatype | Units | Notes                                                               |
|--------------|----------|-------|---------------------------------------------------------------------|
| x            | float32  | m     | Represent XYZ location of the point                                 |
| y            | float32  | m     | Represent XYZ location of the point                                 |
| z            | float32  | m     | Represent XYZ location of the point                                 |
| cluster_id   | uint16   |       | 0 means not clustered. Otherwise same cluster id means same cluster |
| fusion_class | uint8    |       | Points in the same cluster will have the same class                 |
| vision_class | uint8    |       | Points in the same cluster will have the same class                 |

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) of x forward, y left, z up. 

## /fusion/boxes3d
The `/model/boxes3d` topic publishes information about the detected objects using the custom [Detect](../api/edgefirst_msgs.md#detect) schema. Each detect message contains information about the model timing, and a list of objects detected. Each object detected has the normalized bounding box coordinates, label, score, distance, speed, and tracking information included. The distance and speed are 0 when the values cannot be determined. When tracking is enabled, the track ID is a UUID string, and the lifetime represents how many times this track was seen. 

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) for `_optical` frames of z forward, x right, y down. 

This topic is only published if the model service is configured with a model that outputs object detection and when those detections contain depth from a model that is using either radar or lidar.

## /fusion/model_output
The `/fusion/model_output` topic publishes information about the output grid the fusion model with the custom [Mask](../api/edgefirst_msgs.md#mask) schema. This contains the fusion model output as a mask. This can be used to confirm the model is working as expected.

## /fusion/model_output/tracked
The `/fusion/model_output/tracked` topic publishes information about the output grid the fusion model with the custom [Mask](../api/edgefirst_msgs.md#mask) schema. This contains the fusion model output as a mask. This can be used to confirm the model is working as expected. In addition, this topic will also attempt to track objects as they traverse the output grid.
