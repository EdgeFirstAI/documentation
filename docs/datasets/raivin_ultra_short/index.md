# Raivin Ultra Short Dataset

The Raivin Ultra Short dataset is a 3D dataset created by Au-Zone Technologies to evaluate [Fusion models](../../models/fusion/index.md) for people awareness in indoor and outdoor scenarios.  It was captured on a [Raivin platform](../../platforms/quickstart/raivin/index.md) and pairs synchronized camera frames with Radar and/or LiDAR point clouds (PCDs), enabling 3D tracking and spatial perception of people at close range (the "Ultra Short" 9&nbsp;m Radar range mode).

The dataset is publicly available in EdgeFirst Studio and can be explored in the [Raivin Ultra Short gallery](https://edgefirst.studio/public/datasets/ds-c1f/gallery).  Public datasets are read-only, so copy the project into your own workspace if you want to build on it.

## Fusion Benchmark (50 epochs)

=== "ONNX"

    **Fusion BEV Metrics - (480x270) | ONNX**

    | Model                       | Kernel Size | Precision | Recall | IoU   | F1    |
    |-----------------------------|-------------|-----------|--------|-------|-------|
    | fusion-ultra-short-480x270  | 1           | 0.757     | 0.739  | 0.597 | 0.748 |
    |                             | 3           | 0.851     | 0.831  | 0.725 | 0.841 |

=== "TFLite"

    **Fusion BEV Metrics - (480x270) | TFLite**

    | Model                       | Kernel Size | Precision | Recall | IoU   | F1    |
    |-----------------------------|-------------|-----------|--------|-------|-------|
    | fusion-ultra-short-480x270  | 1           | 0.757     | 0.738  | 0.597 | 0.748 |
    |                             | 3           | 0.851     | 0.830  | 0.725 | 0.841 |

## Dataset Information

**Groups**:

- train: 16854 Images
- val: 2133 images

It contains 24,746 images in total and a single class "person".

!!! info "Ungrouped Images"
    There are 5759 images in this dataset that are not associated to
    the train or val groups.

{{ figure("../assets/raivin_ultra_short/label_count.jpg", "Class Distribution") }}

### What's Included

Each sample pairs a synchronized camera frame with the Radar and/or LiDAR point cloud (PCD) captured by the Raivin's sensor module:

- **Camera frames** providing the 2D image context and the camera branch of the Fusion model input.
- **Radar and/or LiDAR PCDs** used to build the 3D bounding-box annotations and to train the spatial (Bird's-Eye-View) occupancy output.  LiDAR PCDs are denser and yield more accurate 3D boxes, while Radar PCDs are sparser but remain robust when the camera is degraded.
- **3D annotations** as 3D bounding boxes in world coordinates (meters) for the single `person` class, alongside the corresponding 2D annotations.

## Data Collection and Annotation

The dataset follows the standard EdgeFirst [dataset capture](../tutorials/capture.md) workflow on a Raivin platform:

1. **Record** — Camera, Radar, and LiDAR streams are recorded together as an MCAP on the device using the [MCAP Recording Service](../../perception/data_collection/recording.md).  Recording on-device keeps the camera frames and PCDs time-synchronized, which is essential for accurate fusion.
2. **Import** — The MCAP recording is uploaded into EdgeFirst Studio, which extracts the camera frames and the Radar/LiDAR PCDs into a dataset container.  See [Dataset Capture](../tutorials/capture.md#capture-with-an-edgefirst-platform) for uploading MCAPs, and [Dataset Import](../tutorials/import.md) for other dataset formats.
3. **Annotate** — Because the PCDs are present, 3D bounding boxes are generated automatically with the [Automatic Ground Truth Generation (AGTG)](../tutorials/annotations/automatic.md) pipeline and then refined manually.  See [3D Annotations](../../3D/annotation.md) and [Dataset Annotations](../tutorials/annotations/index.md) for the full annotation workflow.

## Fusion Model

The benchmark above was produced by an **EdgeFirst Fusion** model trained on this dataset.  The Fusion model performs early fusion of the camera frame with the Radar data and outputs a Bird's-Eye-View (BEV) occupancy grid that localizes people in world coordinates.  For background on the architecture and middleware, see the [Fusion Overview](../../models/fusion/index.md).

To train your own Fusion model on this dataset, follow [Training Fusion Models](../../models/training/fusion.md).  For an indoor, close-range setup like this dataset, set the **Radar Range Mode** to *Ultra Short (9 m)* and the **Object Detection Range** to 9 meters.

### Deploy and Test on the Raivin

After [validating the model](../../models/validation/fusion/managed.md), deploy it back onto the Raivin for live spatial inference by following [Deploying to the Raivin (Fusion)](../../models/deployment/3d_raivin.md).  Once deployed, the Raivin's [Web UI](../../platforms/quickstart/raivin/webui.md) shows the 2D inference (segmentation masks and bounding boxes) alongside the 3D occupancy grid highlighting detected people.  You can also capture an MCAP of the live inferences on the device and review it in Foxglove Studio.

## More 3D Workflows

This dataset is part of EdgeFirst Studio's [3D MLOps](../../3D/index.md) capabilities.  Refer to the 3D section for end-to-end guidance on working with 3D datasets and Fusion models:

- [3D Viewers](../../3D/viewers.md) — inspect camera frames, Radar/LiDAR PCDs, and 3D annotations together.
- [3D Annotations](../../3D/annotation.md) — create and refine 3D bounding boxes, including the AGTG pipeline.
- [Training 3D Perception (Fusion) Models](../../3D/training.md) — configure and run Fusion training sessions.
- [Validation](../../3D/validation.md) — review Fusion model metrics and BEV occupancy results.
- [Deployment](../../3D/deployment.md) — run the trained model on the Raivin platform.

## Image Gallery

{{ figure("../assets/raivin_ultra_short/gallery.jpg", "Raivin Ultra Short Dataset Gallery") }}

## License

{% include-markdown "discrete/datasets/au-zone_license.md" %}
