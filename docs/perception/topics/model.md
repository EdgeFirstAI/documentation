# Model Topics

The model topics are managed by the `model` service and handles running vision only machine learning models.  The service supports object detection and segmentation tasks.

- RTM models
    - Object Detection
    - Segmentation
- ByteTrack tracking

The model topics are published under the `/model` namespace and offers the following sub-topics: `/model/boxes2d`, `/model/mask`, `/model/mask_compressed`, `/model/info`, `/model/visualization`. Tracking parameters are configurable through the `model` service. See model service configuration documentation for details.

## /model/boxes2d
The `/model/boxes2d` topic publishes information about the detected objects using the custom [Detect](../api/edgefirst_msgs.md#detect) schema. Each detect message contains information about the model timing, and a list of objects detected. Each object detected has the normalized bounding box coordinates, label, score, distance, speed, and tracking information included. The distance and speed are 0 when the values cannot be determined. When tracking is enabled, the track ID is a UUID string, and the lifetime represents how many times this track was seen. 

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) for `_optical` frames of z forward, x right, y down. 

This topic is only published if the model service is configured with a model that outputs object detection.

## /model/mask
The `/model/mask` topic publishes information about segmentation masks using the custom [Mask](../api/edgefirst_msgs.md#Mask) schema. Each mask message has the width, height, and length of the mask message. The messages on `/model/mask` are uncompressed and the encoding is an empty string. This topic is recommended to be consumed by other services on the device to save compression and decompression time.

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) for `_optical` frames of z forward, x right, y down. 

This topic is only published if the model service is configured with a model that outputs segmentation.

## /model/mask_compressed
The `/model/mask_compressed` topic publishes information about segmentation masks using the custom [Mask](../api/edgefirst_msgs.md#Mask) schema. Each mask message has the width, height, and length of the mask message. The messages on `/model/mask_compressed` are compressed and the encoding is `zstd`. This topic is recommended to be consumed by services that are operating over the network to reduce network bandwidth requirements.

The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) for `_optical` frames of z forward, x right, y down. 

This topic is only published if the model service is configured to enable compression and configured with a model that outputs segmentation.

## /model/info
The `/model/info` topic publishes information about the current model configuration. It describes shape and type of the input and output tensors, the labels of the model, the tasks the model supports, the format of the model, and the name of the model.