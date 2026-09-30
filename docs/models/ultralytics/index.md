# Ultralytics

The EdgeFirst Studio Model Zoo includes the [Ultralytics](https://docs.ultralytics.com/) YOLO which is a popular implementation of the ubiquitous YOLO architecture for one-shot detection models, and capable of being applied to various other tasks such as instance segmentation.  This document describes the integration into EdgeFirst Studio, supported features, and optimized deployment strategies.  For further details of the Ultralytics implementation of the YOLO architecture, please refer to their documentation.

!!! info
    EdgeFirst Studio uses the EdgeFirst fork of Ultralytics available at [github.com/EdgeFirstAI/ultralytics](https://github.com/EdgeFirstAI/ultralytics) (branch: `edgefirst`), which includes [Camera Adaptor](../cameraadaptor.md) integration for native camera format support during training.

Our Model Zoo ecosystem provides a collection of models to be re-trained through EdgeFirst Studio and deployed to a wide range of devices using a consistent workflow to achieve the best performance and latency at the edge.

## Getting Started

YOLOv5, YOLOv8, YOLO11, and YOLO26 can be trained in EdgeFirst Studio using a Graphical User Interface by following four simple steps:

=== "Select Framework"

    <h2 id="select-framework" style="display: none;"></h2>

    1. Select **Ultralytics** within the available training frameworks.

    {{ img("../assets/ultralytics/ultralytics-train-01.jpg", "Select Ultralytics Training Framework") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [Next → 2. Name Session](#name-session){ .md-button .md-button--primary }
    </div>

=== "Name Session"

    <h2 id="name-session" style="display: none;"></h2>

    2. Set a **name** and **description** *(optional)* for the training session.

    {{ img("../assets/ultralytics/ultralytics-train-02.jpg", "Set Name and Description") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [1. Select Framework ← Back](#select-framework){ .md-button }
    [Next → 3. Select Dataset](#select-dataset){ .md-button .md-button--primary }
    </div>

=== "Select Dataset"

    <h2 id="select-dataset" style="display: none;"></h2>

    3. Choose your **dataset**.

    {{ img("../assets/ultralytics/ultralytics-train-03.jpg", "Select a Dataset") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [2. Name Session ← Back](#name-session){ .md-button }
    [Next → 4. Configure & Train](#train){ .md-button .md-button--primary }
    </div>

=== "Train"

    <h2 id="train" style="display: none;"></h2>

    4. **[Configure the launch form](#training-parameters)** (input resolution, model, weights, training and export) and start the session.

    {{ img("../assets/ultralytics/ultralytics-train-04.jpg", "Configure and Train") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [3. Select Dataset ← Back](#select-dataset){ .md-button }
    [Next → 5. Validate](../validation/vision/managed.md){ .md-button  .md-button--primary }
    </div>

=== "Training Parameters"

    <h2 id="training-parameters" style="display: none;"></h2>

    The Ultralytics launch form groups its fields as follows.

    1. **Training Session**
        1. **Name**: The name of the training session, also used to name the artifacts (e.g. `yolov8n-coffecup-640x640-rgb-t-<session ID>.onnx`)
        2. **Description**: An optional description of the training session, commonly used to highlight some parameters
    2. **Source Dataset**: The dataset the session trains, validates and calibrates on, with its annotation set and tag
    3. **Destination Experiment**: The experiment the training session is created in.  Artifacts and charts are published there when the session finishes
    4. **Input Resolution**: The network input resolution (width x height), 640x640 by default.  Every option is divisible by 32 to match the YOLO backbone stride, and the list covers 1:1, 4:3 and 16:9 resolutions from 320x320 up to 3840x2176 (4K).  A dataset whose aspect ratio differs from the Input Resolution is letterboxed.  Detection accuracy is typically best near 640, the resolution the COCO weights are pretrained at.  With [Input Tiling](#input-tiling) the larger side of the Input Resolution is the tile size.  In case you need a different resolution to be supported, please reach out and [email our support team](mailto:support@edgefirst.ai)
    5. **Task Selection**: Defines the model architecture.  These fields are ignored when the **Weights** are a previous training session
        1. **Model Task**: Either "Detection" (default) or "Segmentation". Note for Ultralytics segmentation refers to instance segmentation
        2. **Model Version**: The Ultralytics version from the choices v5, v8 (default), v11 and v26
        3. **Model Size**: The size of the model from the choices Nano (default), Small, Medium, Large and XLarge
    6. **Training**
        1. **Weights**: The weights the session starts from, either **Pretrained (COCO)** (default) or a previous Ultralytics training session.  See [Weights Source](#weights-source)
        2. **Enable Training**: Off by default, so the session exports the selected weights without training.  Turn it on to fine-tune the weights on the selected dataset, for example when your dataset classes differ from the 80 COCO classes, when you need a non-RGB camera format, or to improve accuracy beyond the COCO baseline.  See [Weights Source](#weights-source) for what each combination does.  The following fields appear when **Enable Training** is on
            1. **Epochs**: The number of epochs to train the model, 50 by default (1 to 500)
            2. **Batch Size**: The number of samples processed in a single training step, 16 by default (1 to 64).  Remember the larger the input resolution the smaller the batch size
            3. **Camera Adaptor**: The target camera format of the model input, one of RGB (default), BGR, RGBA, BGRA, Greyscale or YUYV.  See [Camera Adaptor](#camera-adaptor)
            4. **Input Tiling**: Trains detection models on native-resolution tiles.  See [Input Tiling](#input-tiling)

            !!! note "Charts Without Training"
                A session with **Enable Training** off runs no epochs, so its loss and learning-rate charts stay empty.  Its mAP, precision and recall charts hold a single point, the validation of the exported model.  See [Weights Source](#weights-source).

    7. **Export Parameters**
        1. **Calibration Samples**: The number of training images in the INT8 quantization calibration snapshot, 500 by default (100 to 2000).  Very low counts can reduce quantized accuracy, while higher counts increase export time with diminishing returns.  Snapshots are reused across compatible sessions
        2. **ONNX Opset Version**: The ONNX opset version of the exported model, 11, 12 or 13 (default)
        3. **End-to-End (NMS-free)**: YOLO26 only, off by default.  Builds and trains the one-to-one head so the exported model outputs final detections without NMS.  Leave it off for the best INT8 accuracy, because training the one-to-one head reduces the weight of the one-to-many head used with NMS.  A session with another Model Version fails at launch when it is enabled
        4. **Deployment**: **Tiled** (default) or **Whole frame**, for export-only sessions whose **Weights** were trained with Input Tiling.  See [Deploying Tile-Trained Weights](#deploying-tile-trained-weights)
    8. **Start Session**: This button starts the training session

!!! note "Important"
    Datasets and default weights are handled internally by EdgeFirst Studio.  There's no need to migrate or store data locally.

## Supported Versions

EdgeFirst Studio supports the following Ultralytics YOLO versions:

| Version | Architecture | Key Features |
|---------|--------------|--------------|
| YOLOv5  | C3 backbone  | Classic anchor-based detection |
| YOLOv8  | C2f backbone | Anchor-free detection with DFL |
| YOLO11  | C3k2, C2PSA  | Efficient architecture with depthwise convolutions |
| YOLO26  | C3k2, A2C2f  | Latest architecture with area-attention |

All versions share the same anchor-free `Detect` head and use the same decoder at inference time. See [Model Metadata](../metadata.md) for details on how the decoder works across versions.

## Camera Adaptor

The **Camera Adaptor** dropdown under **Enable Training** selects the target camera format for your deployment platform. This trains the model to accept native camera output (BGR, RGBA, YUYV, etc.) without runtime conversion.  RGB matches the pretrained baseline; the other formats train the first convolution layer to adapt to the new input layout.  When the **Weights** are a previous training session, the camera adaptor comes from those weights and the dropdown is ignored.

See [Camera Adaptor](../cameraadaptor.md) for details on supported formats and platform guidance.

## Weights Source

The **Weights** field in the Training group selects the weights a session starts from.

- **Pretrained (COCO)** (default) uses the Ultralytics COCO weights for the Model Task, Model Version and Model Size selected on the form.
- **A previous training session** uses the `.pt` weights published by an Ultralytics training session together with that session's model definition. The task, version, size, camera adaptor and end-to-end head come from the weights (weights that name no camera adaptor are RGB, like the pretrained weights), so the Task Selection values (**Model Task**, **Model Version** and **Model Size**), the **Camera Adaptor** and the **End-to-End** value on the form are ignored.

The **Enable Training** setting then decides what the session does with the weights.

| Enable Training | Session behavior |
|-----------------|-------------------|
| On | Training starts from the selected weights and fine-tunes them on the selected dataset. |
| Off | The session re-exports the selected weights without retraining, at the Input Resolution and Deployment chosen on the form. |

A session with trained or sourced weights publishes them as `<session name>-<session ID>.pt` with the model metadata embedded, so it can be selected as the weights source of a later session.  An export-only session with **Pretrained (COCO)** weights publishes no `.pt`.

A session with **Enable Training** off validates the exported model on the dataset's validation split and reports the results as the session's final validation metrics, the same metrics a training session reports for its final checkpoint.  The mAP, precision and recall charts hold that single final-validation point; the loss and learning-rate charts stay empty because no epochs run.  Tile-trained weights are validated at the deployed geometry; other models are validated at the Input Resolution.  Validation is skipped when the dataset has no validation split or its classes differ from the model's, for example **Pretrained (COCO)** weights on a dataset that is not COCO.

## Input Tiling

Small objects in high-resolution frames lose most of their pixels when the frame is downscaled to the model's input size.  **Input Tiling**, available when **Enable Training** is on, trains on native-resolution tiles cut from each frame instead, so small objects keep their native pixel scale.

When Input Tiling is enabled, the larger side of the **Input Resolution** is the tile size.  The following settings control how tiles are sampled and validated.

| Setting | Default | Description |
|---------|---------|-------------|
| **Windows per Frame** | 4 (1 to 8) | Number of tiles cut from each decoded frame.  Extra tiles feed mosaic. |
| **Object Windows** | 0.75 | Share of tiles placed around a labeled object. |
| **Background Windows** | 0.15 | Share of tiles that contain no labeled object. |
| **Full-Frame Windows** | 0.10 | Share of tiles that are the whole frame, downscaled to the tile size. |
| **Validation** | Whole frame | **Whole frame** scores full native-resolution frames, **Tiled** scores the deployment tile grid with the detections merged across tiles, and **Both** reports both, with the tiled metrics under a `tiled/` prefix. |

Input Tiling supports detection with the **RGB** or **BGR** camera adaptor.

A tiling training session exports a tiled model at its tile size, with a calibration snapshot cut from the deployment tile grid.

## Deploying Tile-Trained Weights

A model is exported for one input geometry, and a tiled model is exported tiled at its tile size.  The same tile-trained weights can be deployed at another geometry without retraining by starting an export-only session.

The **Deployment** setting in the Export Parameters applies to export-only sessions whose **Weights** were trained with Input Tiling, and is ignored for other sessions.

| Deployment | Input Resolution is | Runtime behavior |
|------------|---------------------|-------------------|
| **Tiled** (default) | The tile size. | The runtime cuts each frame into tiles of this size.  A frame smaller than the tile is letterboxed, centred, into it. |
| **Whole frame** | The model input. | The runtime letterboxes each frame into the model input once, with the padding centred. |

### Train Tiled, Deploy Whole Frame

1. Train a detection model with **Input Tiling** enabled.
2. Start a new Ultralytics session on the same dataset with **Enable Training** off.
3. Set **Weights** to the tiled training session.
4. Set **Deployment** to **Whole frame**.
5. Set **Input Resolution** to the size the model receives, for example `3840x2176` for 4K frames.  A 1080p frame maps to `1920x1088` and a 4K frame to `3840x2176`.

The session exports and calibrates at the new geometry without training.

### Tiled Re-Export at Another Tile Size

To deploy the weights tiled at a different tile size, follow the same steps with **Deployment** set to **Tiled** and choose the tile size as the **Input Resolution**.  Any **Input Resolution** option is available, including `1920x1088` and `3840x2176`.

### Metadata

The model metadata records how the model was trained and exported in `tiling.training` and `tiling.export`.  See [Tiling](../metadata.md#tiling) for the schema and [Tiled Models](../conversion/calibration.md#tiled-models) for the calibration of tiled models.

## Custom Models

If you have a custom float model, it is highly recommended to [export to a quantized model](../conversion/tflite.md) to deploy and maximize the model's performance using the target's NPU.

Deploying a quantized TFLite on the **i.MX 95 EVK** requires an extra step of [converting the model using NXP's eIQ neutron converter](../conversion/neutron.md).  This will allow the model to be deployed on the i.MX 95 using the Neutron delegate in the platform.

!!! warning "Specific BSP versions required"

    The latest BSP available for the Maivin lacks the `onnxruntime` library needed to run ONNX on the NPU.

    On the i.MX 8M Plus EVK, BSP v5.15 are used in the examples which was noted to have the providers needed for ONNX to run on the NPU `NnapiExecutionProvider`, `VsiNpuExecutionProvider`.  Later BSPs such as v6.12 did not have these providers.  This still needs confirmation from NXP as to why these providers were removed. 

## License

Ultralytics YOLO is covered by the GNU AGPL-3.0 license which allows for free use of this model within the constraints of the license.  Ultralytics offers [commercial licensing options](https://www.ultralytics.com/license).
