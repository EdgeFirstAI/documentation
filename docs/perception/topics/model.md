# Model Topics

The model topics are managed by the `model` service and handles running vision machine learning models on the camera frames.  The service supports object detection and segmentation tasks.

- TensorFlow Lite models on the NPU through a delegate, or on the CPU
    - Object Detection
    - Instance and Semantic Segmentation
- ModelPack, Ultralytics YOLO, and EdgeFirst Model Zoo models with the embedded EdgeFirst configuration
- ByteTrack tracking

The model service subscribes to the [camera frames](camera.md#cameraframe) and publishes its results under the `model` namespace on the following sub-topics: `model/output`, `model/info`, and optionally `model/visualization`.  The legacy `model/boxes2d` and `model/mask` topics can be re-enabled through configuration.  Detection, tracking, and topic parameters are configurable through the `model` service.  See the [model service configuration](../../platforms/configuration/model.md) documentation for details.  Topic names are relative to the device [hostname namespace](index.md#hostname-namespaces).

## model/output

The `model/output` topic publishes the complete result of each inference using the custom [Model](../api/edgefirst_msgs.md#model) schema.  Each message contains the model timing and the detected objects.

- The `input_time`, `model_time`, `output_time`, and `decode_time` durations break down the time spent loading the camera frame into the model input, running the model, reading the outputs, and decoding the outputs including NMS and tracking.
- The `boxes` array holds one [Box](../api/edgefirst_msgs.md#box) per detected object with the normalized center point, width, and height of the bounding box, the label, the score, the distance and speed which are `0` when unknown, and the [Track](../api/edgefirst_msgs.md#track) information.  When tracking is enabled the track ID is a UUID string and the lifetime represents how many frames this track was seen, otherwise the track ID is empty.
- The `masks` array holds the segmentation [Mask](../api/edgefirst_msgs.md#mask) messages.  A semantic segmentation model publishes a single mask with `boxed` false where each pixel holds the class index.  An instance segmentation model publishes one mask per detected box with `boxed` true, in the same order as the `boxes` array, cropped to the box.  Masks are published uncompressed with an empty encoding.

The box coordinates are normalized to the camera frame, the service back-projects the detections through its aspect-preserving letterbox so the coordinates align with the original camera image.  The XYZ coordinate system follows the [standard ROS convention](https://www.ros.org/reps/rep-0103.html#coordinate-frame-conventions) for `_optical` frames of z forward, x right, y down.

The `boxes` array is empty for segmentation-only models and the `masks` array is empty for detection-only models.  The message header timestamp matches the camera frame the inference was run on, which lets consumers such as the Web UI align the overlay with the decoded video frame.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | [Camera Page](../../platforms/quickstart/maivin/webui.md#the-camera-page) segmentation overlay
Foxglove | [EdgeFirst Plug-in](../data_collection/foxglove.md#installing-edgefirst-plugin)
SDK | [Model Example](../dev/examples/model.md)

## model/info

The `model/info` topic publishes information about the current model configuration using the custom [ModelInfo](../api/edgefirst_msgs.md#modelinfo) schema.  It describes the shape and type of the input and output tensors, the labels of the model, the tasks the model supports, the format of the model, and the name of the model.  Consumers such as the fusion service and the EdgeFirst Publisher use the labels to map the class indices found in the masks and boxes to label names.

## model/visualization

The `model/visualization` topic publishes information about the detected objects using the [ImageAnnotations](../api/foxglove_msgs.md#imageannotations) schema.  This message contains text and line annotations which will draw boxes and labels in Foxglove.  This message is intended only for help visualizing the detection results in Foxglove without needing the EdgeFirst plug-in.

This topic is only published if the model service is configured to enable [visualization](../../platforms/configuration/model.md#visualization) and configured with a model that outputs object detection.

## Legacy Topics

Earlier releases of the model service published the detection boxes and the segmentation masks on separate topics.  These topics are disabled by default and can be re-enabled with the `DETECT_TOPIC` and `MASK_TOPIC` settings of the [model service configuration](../../platforms/configuration/model.md#topics) for applications which have not migrated to `model/output`.

### model/boxes2d

The `model/boxes2d` topic publishes the detected objects using the custom [Detect](../api/edgefirst_msgs.md#detect) schema with the same [Box](../api/edgefirst_msgs.md#box) entries as `model/output`.

### model/mask

The `model/mask` topic publishes the segmentation masks using the custom [Mask](../api/edgefirst_msgs.md#mask) schema.  The masks are uncompressed, the previous `model/mask_compressed` topic with zstd compressed masks is no longer provided as compression is handled by the Web UI transport.
