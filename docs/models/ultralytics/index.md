# Ultralytics

The EdgeFirst Studio Model Zoo includes the [Ultralytics](https://docs.ultralytics.com/) YOLO which is a popular implementation of the ubiquitous YOLO architecture for one-shot detection models, and capable of being applied to various other tasks such as instance segmentation.  This document describes the integration into EdgeFirst Studio, supported features, and optimized deployment strategies.  For further details of the Ultralytics implementation of the YOLO architecture, please refer to their documentation.

!!! info
    EdgeFirst Studio uses the EdgeFirst fork of Ultralytics available at [github.com/EdgeFirstAI/ultralytics](https://github.com/EdgeFirstAI/ultralytics) (branch: `edgefirst`), which includes [Camera Adaptor](../cameraadaptor.md) integration for native camera format support during training.

Our Model Zoo ecosystem provides a collection of models to be re-trained through EdgeFirst Studio and deployed to a wide range of devices using a consistent workflow to achieve the best performance and latency at the edge.

## Getting Started

YOLOv5, YOLOv8, YOLO11, and YOLO26 can be trained in {{ studio_link("EdgeFirst Studio") }} by following four simple steps:

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
        1. **Name**: The name of the training session, also used to name the artifacts (e.g. `yolov8n-coffeecup-640x640-rgb-t-<session ID>.fp32.onnx`)
        2. **Description**: An optional description of the training session, commonly used to highlight some parameters
    2. **Source Dataset**: The dataset the session trains, validates and calibrates on, with its annotation set and tag.  The dataset can belong to a different project than the experiment
    3. **Destination Experiment**: The experiment the training session is created in.  Its artifacts and charts are published there when the session finishes
    4. **Input**
        1. **Input Resolution**: The network input resolution (width x height), 640x640 by default.  The options are 640x640 and 1280x1280 (1:1), 640x480 VGA (4:3), and 960x544 qHD, 1920x1088 FHD and 3840x2176 4K (16:9).  The 16:9 options are rounded to the 32-pixel backbone stride.  A dataset whose aspect ratio differs from the Input Resolution is letterboxed.  Detection accuracy is typically best near 640, the resolution the COCO weights are pretrained at.  The large options suit [whole-frame deployment of tile-trained weights](#deploying-tile-trained-weights).  With [Input Tiling](#input-tiling) the larger side of the Input Resolution is the tile size
        2. **Custom Resolution**: Optional.  A network input resolution as `WIDTHxHEIGHT`, for example `1344x768`, used instead of **Input Resolution**.  Both sides must be multiples of 32, otherwise the session fails before it downloads the dataset.  A width that is not a multiple of 64 works but logs a warning, because Mali GPU preprocessing needs 64-byte aligned RGB rows.  Leave it empty to use **Input Resolution**
    5. **Task Selection**: Defines the model architecture.  These fields are ignored when the **Weights** are a previous training session
        1. **Model Task**: Either "Detection" (default) or "Segmentation". Note for Ultralytics segmentation refers to instance segmentation
        2. **Model Version**: The Ultralytics version from the choices v5, v8 (default), v11 and v26
        3. **Model Size**: The size of the model from the choices Nano (default), Small, Medium, Large and XLarge
    6. **Training**
        1. **Weights**: The weights the session starts from, either **Pretrained (COCO)** (default) or a previous Ultralytics training session.  See [Weights Source](#weights-source)
        2. **Enable Training**: Off by default, so the session exports the selected weights without training.  Turn it on to fine-tune the weights on the selected dataset, for example when your dataset classes differ from the 80 COCO classes, when you need a non-RGB camera format, or to improve accuracy beyond the COCO baseline.  See [Weights Source](#weights-source) for what each combination does.  The following fields appear when **Enable Training** is on

            1. **Epochs**: The number of epochs to train the model, 50 by default (1 to 500)
            2. **Batch Size**: The number of samples (tiles, with Input Tiling) processed in a single training step, 16 by default (1 to 64).  The larger the input resolution, the smaller the batch that fits in GPU memory
            3. **Optimizer**: **Auto** (default), SGD, MuSGD, AdamW or Adam.  See [Optimizer](#optimizer)
            4. **Learning Rate**: The initial learning rate of an explicitly chosen optimizer, 0.01 by default (0.0005 to 0.02).  0.01 suits SGD and MuSGD; 0.001 to 0.002 suits AdamW and Adam.  Ignored with **Auto**
            5. **Final Learning Rate Factor**: The learning rate at the last epoch, as a fraction of the initial learning rate, 0.01 by default (0.01 to 1)
            6. **Cosine Schedule**: Off by default.  Decays the learning rate along a cosine curve instead of linearly
            7. **Momentum**: SGD momentum, or Adam beta1, of an explicitly chosen optimizer, 0.937 by default (0.6 to 0.99).  Ignored with **Auto**
            8. **Weight Decay**: L2 weight decay applied to convolution and linear weights, 0.0005 by default (0 to 0.05)
            9. **Warmup Epochs**: Epochs over which the learning rate and momentum ramp up from their warmup values, 3 by default (0 to 10)
            10. **Camera Adaptor**: The target camera format of the model input, one of RGB (default), BGR, RGBA, BGRA, Greyscale or YUYV.  See [Camera Adaptor](#camera-adaptor)
            11. **Input Tiling**: Trains detection models on native-resolution tiles.  Its settings appear when it is on.  See [Input Tiling](#input-tiling)

            !!! note "Charts Without Training"
                A session with **Enable Training** off runs no epochs, so its loss and learning-rate charts stay empty.  Its mAP, precision and recall charts hold a single point, the validation of the exported model.  See [Weights Source](#weights-source).

    7. **Augmentation**: Random changes applied to training images, used only when **Enable Training** is on.  The defaults are Ultralytics' own.  See [Augmentation](#augmentation)
    8. **Export Parameters**
        1. **Calibration Samples**: The number of training images (tiles, for a tiled model) in the INT8 quantization calibration snapshot, 500 by default (100 to 2000).  Very low counts can reduce quantized accuracy, while higher counts increase export time with diminishing returns.  Snapshots are reused across compatible sessions
        2. **ONNX Opset Version**: The ONNX opset version of the exported model, 11, 12 or 13 (default)
        3. **End-to-End (NMS-free)**: YOLO26 only, off by default.  Builds and trains the one-to-one head so the exported model outputs final detections without NMS.  Leave it off for the best INT8 accuracy, because training the one-to-one head reduces the weight of the one-to-many head used with NMS.  A session with another Model Version fails at launch when it is enabled
        4. **Deployment**: **Whole frame** (default) or **Tiled**.  Applies only to export-only sessions whose **Weights** were trained with Input Tiling, and is ignored for every other session.  See [Deploying Tile-Trained Weights](#deploying-tile-trained-weights)
    9. **Start App**: This button starts the training session

    The session publishes `labels.txt`, FP32 and FP16 ONNX models (`.fp32.onnx` and `.fp16.onnx`), a TensorFlow SavedModel (`_saved_model.zip`) and, when it trained or sourced weights, the `.pt` weights.  The INT8 calibration snapshot is stored in the Studio snapshot store, where the [converter apps](../conversion/index.md) find it.

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

The **Camera Adaptor** dropdown under **Enable Training** selects the target camera format for your deployment platform. This trains the model to accept native camera output (BGR, RGBA, YUYV, etc.) without runtime conversion.  RGB matches the pretrained baseline; the other formats train the first convolution layer to adapt to the new input layout.  When the **Weights** are a previous training session, the camera adaptor comes from those weights and the dropdown is ignored.  An export-only session with **Pretrained (COCO)** weights always exports an RGB model.

See [Camera Adaptor](../cameraadaptor.md) for details on supported formats and platform guidance.

## Optimizer

**Optimizer** set to **Auto** lets Ultralytics choose from the length of the run.  When the run exceeds 10,000 training steps (⌈images ÷ max(Batch Size, 64)⌉ × Epochs) it uses MuSGD with learning rate 0.01 and momentum 0.9; otherwise it uses AdamW with a learning rate fitted to the number of classes and momentum 0.9.  **Auto** ignores the **Learning Rate** and **Momentum** fields.

Choose an optimizer explicitly to compare sessions of different lengths, batch sizes or tiling settings on the same optimizer, because **Auto** can pick a different optimizer for each of them.  **Final Learning Rate Factor**, **Cosine Schedule**, **Weight Decay** and **Warmup Epochs** apply with every optimizer.

## Augmentation

The Augmentation group sets the random changes applied to training images.  It is used only when **Enable Training** is on.

| Setting | Default | Description |
|---------|---------|-------------|
| **Horizontal Flip** | 0.5 (0 to 1) | Probability of mirroring an image left to right.  Set it to 0 when a mirrored object would belong to a different class or look wrong, such as text, signs, arrows or left and right hands. |
| **Vertical Flip** | 0 (0 to 1) | Probability of mirroring an image top to bottom.  Leave it at 0 for side-on cameras, where up stays up; overhead and aerial views suit 0.5. |
| **Rotation** | 0 (0 to 180) | Largest random rotation, in degrees either way.  Boxes grow to enclose the rotated object, so keep it small for side-on cameras; overhead and aerial views suit up to 180. |
| **Hue** | 0.015 (0 to 0.1) | Largest random hue shift, as a fraction of the color wheel.  Set it to 0 when color tells classes apart. |
| **Saturation** | 0.7 (0 to 1) | Largest random change in color saturation, as a fraction. |
| **Brightness** | 0.4 (0 to 1) | Largest random change in brightness, as a fraction.  Lower it for fixed indoor lighting and raise it for outdoor scenes. |
| **Mosaic** | 1 (0 to 1) | Probability of combining four training images into one.  Mosaic shows objects at more scales and positions, but it can hurt small datasets and datasets whose objects fill most of the frame. |
| **Final Epochs Without Mosaic** | 10 (0 to 100) | Number of final epochs trained with mosaic off, so the model finishes on whole images.  0 keeps mosaic on to the end. |

**Hue**, **Saturation** and **Brightness** have no effect with the Greyscale camera adaptor.  With [Input Tiling](#input-tiling) the tiling trainer sets **Final Epochs Without Mosaic** to its final phase of 10 epochs and limits the random scale, so the form values for those are ignored and the session log records it.

## Weights Source

The **Weights** field in the Training group selects the weights a session starts from.

- **Pretrained (COCO)** (default) uses the Ultralytics COCO weights for the Model Task, Model Version and Model Size selected on the form.
- **A previous training session** uses the `.pt` weights published by an Ultralytics training session together with that session's model definition. The task, version, size, camera adaptor and end-to-end head come from the weights (weights that name no camera adaptor are RGB, like the pretrained weights), so the Task Selection values (**Model Task**, **Model Version** and **Model Size**), the **Camera Adaptor** and the **End-to-End** value on the form are ignored.  The weights must carry the EdgeFirst model metadata, which sessions from trainer version 1.15.0 onward embed; otherwise the session fails at launch.

The **Enable Training** setting then decides what the session does with the weights.

| Enable Training | Session behavior |
|-----------------|-------------------|
| On | Training starts from the selected weights and fine-tunes them on the selected dataset. |
| Off | The session re-exports the selected weights without retraining, at the Input Resolution and, for tile-trained weights, the Deployment chosen on the form. |

A session with trained or sourced weights publishes them as `<session name>-<session ID>.pt` with the model metadata embedded, so it can be selected as the weights source of a later session.  An export-only session with **Pretrained (COCO)** weights publishes no `.pt`.  YOLOv5 segmentation has no pretrained export: a **Pretrained (COCO)** v5 segmentation session needs **Enable Training** on.

A session with **Enable Training** off validates the exported model on the dataset's validation split and reports the results as the session's final validation metrics, the same metrics a training session reports for its final checkpoint.  The mAP, precision and recall charts hold that single final-validation point; the loss and learning-rate charts stay empty because no epochs run.  Tile-trained weights are validated at the deployed geometry; other models are validated at the Input Resolution.  Validation is skipped when the dataset has no validation split or its classes differ from the model's, for example **Pretrained (COCO)** weights on a dataset that is not COCO.

Validation matches the Ultralytics validator and the [EdgeFirst Profiler](../../profiler/index.md): multi-label candidates, class-aware NMS at IoU 0.7 on whole frames (0.5 per tile on the tile grid) and at most 300 detections per frame.

## Input Tiling

Small objects in high-resolution frames lose most of their pixels when the frame is downscaled to the model's input size.  **Input Tiling**, available when **Enable Training** is on, trains on native-resolution tiles cut from each frame instead, so small objects keep their native pixel scale.  See [Training for Small Objects (SAHI)](../training/sahi.md) for when to use it and how to deploy the result.

When Input Tiling is enabled, the tile is a square whose side is the larger side of the **Input Resolution** (or **Custom Resolution**): 640x640 trains on 640x640 tiles, and 1920x1088 on 1920x1920 tiles.  Choose a square resolution for tiled training.  The following settings control how tiles are sampled.

| Setting | Default | Description |
|---------|---------|-------------|
| **Frames per Batch** | 4 (1 to 64) | Frames each training batch is drawn from.  Each frame contributes about Batch Size ÷ Frames per Batch tiles, and every frame is visited once per epoch, so an epoch has Batch Size ÷ Frames per Batch times the training steps of an untiled epoch.  Set it to the Batch Size (one tile per frame per epoch) to give a tiled epoch the same number of steps as an untiled one, so that Epochs, warmup and the learning-rate schedule compare directly with untiled sessions.  Values above the Batch Size use the Batch Size. |
| **Object Windows** | 0.75 (0 to 1) | Target share of an epoch's tiles that contain a labeled object. |
| **Background Windows** | 0.15 (0 to 1) | Target share of an epoch's tiles that contain no labeled object.  Frames without labels supply these first. |
| **Full-Frame Windows** | 0.10 (0 to 1) | Target share of an epoch's tiles that are a whole labeled frame, downscaled to the tile size. |

Object windows prefer placements that hold several labeled objects.  The last 10 epochs train with mosaic off, and the full-frame share moves to object windows, so the model finishes on tiles as it meets them at deployment.  Tiled training runs on a single GPU.

Input Tiling supports detection with the **RGB** or **BGR** camera adaptor; other combinations fail at launch.

Every epoch, validation scores every validation frame on the deployment tile grid: each tile is detected separately with class-aware NMS at IoU 0.5, and the detections are merged across tiles.  These metrics choose the best checkpoint.  Besides the usual metrics, a tiled session charts per-epoch `tiling/*` statistics of the sampler, such as the realized object and background shares and the mean tiles per frame.  To measure the same weights at whole frame, start an export-only session with **Deployment** set to **Whole frame**; see [Deploying Tile-Trained Weights](#deploying-tile-trained-weights).

A tiling training session exports a tiled model at its tile size, with a calibration snapshot cut from the deployment tile grid.

## Deploying Tile-Trained Weights

A model is exported for one input geometry, and a tiling training session always exports a tiled model at its tile size.  The same tile-trained weights can be deployed at another geometry without retraining by starting an export-only session.

The **Deployment** setting in the Export Parameters applies to export-only sessions whose **Weights** were trained with Input Tiling, and is ignored for other sessions.

| Deployment | Input Resolution is | Runtime behavior |
|------------|---------------------|-------------------|
| **Whole frame** (default) | The model input. | The runtime letterboxes each frame into the model input once, with the padding centered. |
| **Tiled** | The tile size. | The runtime cuts each frame into tiles of this size.  A frame smaller than the tile is letterboxed, centered, into it. |

!!! warning "ModelPack and Ultralytics default to different Deployment modes"
    The **Deployment** default is **Whole frame** in Ultralytics and **Tiled** in ModelPack.

### Train Tiled, Deploy Whole Frame

1. Train a detection model with **Input Tiling** enabled.
2. Start a new Ultralytics session on the same dataset with **Enable Training** off.
3. Set **Weights** to the tiled training session.
4. Keep **Deployment** at **Whole frame**.
5. Set **Input Resolution**, or **Custom Resolution**, to the size the model receives: the camera frame rounded to multiples of 32.  A 1080p frame maps to `1920x1088`, a 4K frame to `3840x2176`, and a 1360x765 frame to a custom `1344x768`.
6. Consider lowering **Calibration Samples** for large resolutions.  A whole-frame snapshot holds full frames, so 500 samples at 4K take about 12.5 GB, and the trainer warns when a snapshot exceeds 4 GiB.

The session exports, calibrates and validates at the new geometry without training.

### Tiled Re-Export at Another Tile Size

To deploy the weights tiled at a different tile size, follow the same steps with **Deployment** set to **Tiled** and choose the tile size as the **Input Resolution** or **Custom Resolution**.  The re-exported tile does not need to be square; for example `1920x1088` tiles cover a 4K frame in a 3x3 grid, against 28 tiles of 640x640.

See [Training for Small Objects (SAHI)](../training/sahi.md#choosing-a-deployment) for how to choose between the two.

### Metadata

The model metadata records how the model was trained and exported in `tiling.training` and `tiling.export`.  See [Tiling](../metadata.md#tiling) for the schema and [Tiled Models](../conversion/calibration.md#tiled-models) for the calibration of tiled models.

## Custom Models

If you have a custom float model, it is highly recommended to [export to a quantized model](../conversion/tflite.md) to deploy and maximize the model's performance using the target's NPU.

Deploying a quantized TFLite on the **i.MX 95 EVK** requires an extra step of [converting the model using NXP's eIQ neutron converter](../conversion/neutron.md).  This will allow the model to be deployed on the i.MX 95 using the Neutron delegate in the platform.

## License

Ultralytics YOLO is covered by the GNU AGPL-3.0 license which allows for free use of this model within the constraints of the license.  Ultralytics offers [commercial licensing options](https://www.ultralytics.com/license).
