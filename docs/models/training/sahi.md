# Training for Small Objects (SAHI)

Small objects disappear when a high-resolution frame is squeezed into a fixed model input.  **Input Tiling**, the EdgeFirst implementation of SAHI (Slicing Aided Hyper Inference), trains the model on native-resolution tiles of each frame, so small objects keep their pixels.  The trained weights can then be deployed in one of two ways: **tiled**, where the runtime cuts each frame into tiles and merges the detections, or **whole frame**, where an export-only session re-exports the same weights at the camera's native resolution for a single inference per frame.

This page explains when tiling helps, how EdgeFirst Studio trains with tiles, and how to deploy and validate the result with either trainer.

{{ figure("../assets/training/sahi/sahi-train-export-runtime.png", "One set of tile-trained weights, two deployments: tiled with a per-tile NMS and IoS merge, or whole frame in one pass.  Results for YOLO26s on VisDrone, RTX 3090.") }}

## Why Small Objects Disappear

A detector sees an object through the cells of its feature maps; the finest detection head has one cell for every 8 input pixels.  An object needs a few cells to be localized and classified.  When a frame is letterboxed into a smaller model input, every object shrinks by the same factor.

The [VisDrone](https://github.com/VisDrone/VisDrone-Dataset) aerial dataset shows the effect.  Most of its frames are 1360x765, with about 71 objects per frame, and the median object is about 23 pixels on a side.  Letterboxed into a 640x640 input, that object shrinks to about 11 pixels, roughly one stride-8 cell, and most of its detail is gone.  On a native-resolution 640x640 tile, or in a whole-frame 1344x768 input, it keeps its 23 pixels.

{{ figure("../assets/training/sahi/sahi-small-object-scale.png", "The median VisDrone object against the stride-8 grid at each input.  Downscaling to 640 leaves it about one cell wide; a native tile or a native-resolution input keeps it at about three.") }}

Raising the input resolution keeps the pixels, but training a whole-frame model at high resolution needs smaller batches, takes longer and tends to overfit early.  Tiling decouples training from the frame size: the model trains on fixed-size tiles at the same batch size whatever the frame size.

## When to Tile

Tiling is two independent choices: whether to **train** on tiles, and whether to **infer** on tiles.

- **Train on tiles** when the objects that matter are small relative to the frame, and the frames are larger than the input you can afford to train at.  The tile size, usually 640x640, and the batch size stay the same at every frame size.
- **Infer on tiles** only when the whole frame does not fit the target accelerator, by memory or by operator limits, or when INT8 quantization at the large input loses too much accuracy on that target.  Otherwise, deploy the tile-trained weights whole frame: one inference per frame is usually faster and, on most targets, more accurate.

{{ figure("../assets/training/sahi/sahi-when-to-tile.png", "Training on 640 tiles keeps the same tile and batch at every frame size.  At inference a frame needs more tiles as it grows (640 tiles with at least 10% overlap), while a whole-frame pass eventually exceeds what the board can run.  Where the crossover lies depends on the model and the board.") }}

The number of tiles grows quickly with the frame size.  With 640x640 tiles and the minimum 10% overlap, a 1360x765 frame needs 6 tiles, a 1280x1280 frame 9, a 4K frame 28 and an 8K frame 112, and every tile is a full inference.

## How Studio Trains with Tiles

Turn on **Input Tiling (SAHI)** in ModelPack or **Input Tiling** in Ultralytics.  The **Input Resolution** becomes the tile size; use 640x640.  Input Tiling supports object detection with the RGB or BGR camera adaptor.

Every epoch visits every training frame once.  Each training batch is drawn from **Frames per Batch** frames, each contributing about Batch Size ÷ Frames per Batch tiles.  The tiles are cut at native resolution, and each is one of three kinds of window:

| Window | Default share | Description |
|--------|---------------|-------------|
| **Object** | 75% | Placed around a labeled object, choosing the best of four candidate placements, the one that holds the most other objects.  Part of them are snapped to the deployment tile grid, so the model learns the tile seams it meets at inference. |
| **Background** | 15% | Contains no labeled object, so the model learns what to ignore.  Frames without labels supply these first. |
| **Full frame** | 10% | The whole frame letterboxed into the tile, keeping large objects and scene context. |

{{ figure("../assets/training/sahi/sahi-training-windows.jpg", "The three kinds of training window on a VisDrone frame, cut for a 640x640 deployment grid.") }}

An object cut by a tile edge is kept as a training target only when enough of it is visible inside the tile.  The final epochs train on native-scale tiles only, with the tile mosaic off, so the model finishes on tiles as it meets them at deployment.

The two trainers expose different controls over the sampler:

| Trainer | Sampler settings |
|---------|------------------|
| ModelPack | Frames per Batch, Background Tiles, Full-Image Tiles, Grid-Aligned Tiles, Native-Scale Tiles, Tile Zoom Range, Minimum Visible Fraction, Final Native Epochs, Class-Balanced Tiles.  See [ModelPack Input Tiling](../modelpack/index.md#input-tiling-sahi). |
| Ultralytics | Frames per Batch, Object Windows, Background Windows, Full-Frame Windows.  Tiles are always cut at native scale, with the random scale augmentation limited to ±25%, and the last 10 epochs run without mosaic or random scale.  See [Ultralytics Input Tiling](../ultralytics/index.md#input-tiling). |

!!! tip "Full-frame windows are not whole-frame training"
    A full-frame window is a training tile that shows the whole frame downscaled.  It is unrelated to whole-frame **deployment**, which runs the full-resolution frame through the model.

## Validating a Tile-Trained Model

A tile-trained model is scored on whole validation frames, not on individual tiles, in one of two ways:

- **Tile grid**: each frame is cut into the deployment tile grid, each tile is detected separately, and the detections are merged.  This measures a tiled deployment.
- **Whole frame**: each frame runs through the model in one pass at native resolution.  This measures a whole-frame deployment of the same weights.

| Trainer | Validation during training |
|---------|----------------------------|
| ModelPack | **Tiled Validation** selects **Whole Image** (default), **Tile Grid** or **Both**.  See [Tiled Validation](../modelpack/index.md#tiled-validation). |
| Ultralytics | Always the tile grid.  These metrics choose the best checkpoint.  To measure whole-frame accuracy, run an export-only **Whole frame** session. |

An export-only session validates the model it exports, at its deployed geometry, and reports the result as its final validation metrics.  Validation is skipped when the dataset has no validation split or its classes differ from the model's.

## Deploying a Tile-Trained Model

The edge runtimes compile a static input shape, so the deployment geometry is fixed when the model is exported.  The [model metadata](../metadata.md#tiling) records it in a `tiling` section that the converters copy unchanged and the runtime reads.

| | Online tiling | Whole-frame re-export |
|-|---------------|-----------------------|
| Produced by | The training session itself | An export-only session with the tile-trained session as its **Weights** |
| Model input | The tile, e.g. 640x640 | The camera frame rounded to multiples of 32, e.g. 1344x768 or 3840x2176 |
| `tiling.mode` | `tiled` | `whole_frame` |
| Inferences per frame | One per tile, plus a per-tile NMS and a merge | One |
| Calibration snapshot | Deployment-grid tiles at native scale | Letterboxed whole frames |
| Choose it when | The whole frame does not fit the accelerator, or large-input INT8 loses too much accuracy | The board can run the whole frame, usually the faster and more accurate choice |

### Online Tiling

A training session with Input Tiling exports a tiled model at its tile size.  At runtime each frame is cut into an evenly distributed grid of tiles with at least 10% overlap, so an object on a seam lands whole inside at least one tile.  Each tile runs through the model, its detections are filtered with class-aware NMS and lifted into frame coordinates, and the detections of adjacent tiles are merged.

The merge compares boxes by **IoS**, the intersection over the smaller box, rather than IoU.  A fragment of an object cut by a seam overlaps the whole box only partly by IoU, so an IoU test would keep both, while its IoS is close to 1.  The merge keeps the highest-scoring box of each group.

{{ figure("../assets/training/sahi/sahi-seams-merge.png", "An object on a tile seam is detected whole in one tile and as a fragment in the adjacent tile.  IoU would keep both boxes; IoS matches the fragment to the whole box and the merge keeps the best one.") }}

The cost is one inference per tile: the 6-tile grid of a 1360x765 frame covers about 2.4 times the frame's pixels.  See [Grid](../metadata.md#grid) and [Merge](../metadata.md#merge) for the exact algorithms.

### Whole-Frame Re-Export

The detectors are fully convolutional and the tiles were cut at native scale, so the same weights run on the full-resolution frame without retraining.  An export-only session exports them at the camera's resolution adjusted to multiples of 32, with the frame letterboxed into it: 1080p becomes 1920x1088 and 4K becomes 3840x2176, and 1360x765 frames suit a custom 1344x768 in Ultralytics.  ModelPack rounds its Input Resolution up to multiples of 32; Ultralytics requires its Input Resolution or Custom Resolution to be multiples of 32 already.  The runtime letterboxes each frame into the model input and runs it once.

### Tiled Re-Export at Another Tile Size

An export-only session can also re-export tile-trained weights tiled at another tile size, for example a larger tile on an accelerator that fits it, to cut the number of tiles per frame.  Objects are still seen at native scale, so the runtime tile does not need to match the training tile.

### Choosing a Deployment

The EdgeFirst Model Zoo publishes VisDrone results for each strategy.  For YOLO26s on an RTX 3090 (ONNX FP32), the same tile-trained weights deployed whole frame at 1344x768 were both the most accurate and about three times faster than tiled deployment:

| Training | Deployment | mAP50-95 | AP small | FPS |
|----------|------------|----------|----------|-----|
| Whole frame at 640 | 640x640 | 22.4 | 14.0 | 239 |
| Whole frame at 1280 | 1280x1280 | 33.0 | 24.6 | 102 |
| 640 tiles | Tiled, about 5 tiles per frame | 32.9 | 24.3 | 46 |
| 640 tiles | Whole frame at 1344x768 | **35.2** | **26.5** | 138 |

{{ figure("../assets/training/sahi/sahi-deployment-lanes.png", "The four VisDrone strategies to scale, with their YOLO26s results on an RTX 3090.") }}

The ranking depends on the target.  On embedded accelerators the same weights showed the same pattern on most targets, for example on the NVIDIA Jetson Orin Nano (TensorRT FP16: 34.97 whole frame at 89 ms against 32.82 tiled at 176 ms) and the NXP i.MX 95 (Neutron INT8: 32.12 at 321 ms against 30.45 at 425 ms).  On the NXP Ara240, INT8 quantization of the large whole-frame input lost more accuracy than tiling did, and tiled deployment scored higher (26.62 against 23.06).  Some targets cannot run the whole frame at all: the Hailo-8L cannot fit some models at 1344x768 or 1280x1280 in its on-chip memory.  See the [VisDrone models on the EdgeFirst Model Zoo](https://huggingface.co/EdgeFirst/visdrone-yolo26-det) for every model, size and platform.

Validate both deployments on your own target with the [EdgeFirst Profiler](../../profiler/index.md) before choosing.

## Step by Step

The steps below train with tiles, then produce both deployments from the same weights.

=== "Ultralytics"

    1. **Train with tiles.**  Start an Ultralytics training session with **Model Task** Detection, **Input Resolution** `640x640`, **Enable Training** on, a camera adaptor of RGB or BGR, and **Input Tiling** on.  Keep the tiling defaults.  The session exports a tiled model at 640x640 and validates on the tile grid.
    2. **Re-export whole frame.**  Start another Ultralytics session on the same dataset with **Enable Training** off and **Weights** set to the training session.  Keep **Deployment** at **Whole frame**, the default.  Set **Input Resolution** or **Custom Resolution** to the camera frame rounded to multiples of 32, for example `1920x1088` for 1080p, `3840x2176` for 4K or a custom `1344x768` for 1360x765 frames.  Consider lowering **Calibration Samples** for 4K, because whole-frame snapshots hold full frames.
    3. **Compare.**  Both sessions report final validation metrics for their deployment.  Convert and profile both on the target to compare accuracy and latency.

    See [Deploying Tile-Trained Weights](../ultralytics/index.md#deploying-tile-trained-weights).

=== "ModelPack"

    1. **Train with tiles.**  Start a ModelPack training session with **Object Detection** only, **Input Resolution** `640x640`, a camera adaptor of RGB or BGR, **Input Tiling (SAHI)** on and, for small objects, **Fine Detection Head** on.  Keep the tiling defaults.  Set **Tiled Validation** to **Both** to see the tile grid and whole-image metrics side by side.  The session exports a tiled model at 640x640.
    2. **Re-export whole frame.**  Start another ModelPack session on the same dataset with **Weights** set to the training session's `.keras` weights and **Enable Training** off.  Set **Deployment** to **Whole frame**; the ModelPack default is **Tiled**.  Set **Input Resolution** to the option matching the camera frame, for example `1920x1088` for 1080p or `3840x2176` for 4K.  The session rounds the resolution up to multiples of 32.
    3. **Compare.**  Both sessions report final validation metrics for their deployment.  Convert and profile both on the target to compare accuracy and latency.

    See [Deploying Tile-Trained Models](../modelpack/index.md#deploying-tile-trained-models).

!!! warning "Deployment defaults differ between the trainers"
    The **Deployment** default is **Whole frame** in Ultralytics and **Tiled** in ModelPack.  **Deployment** applies only to export-only sessions whose **Weights** were trained with Input Tiling.  A training session with Input Tiling always exports tiled, whatever **Deployment** says.

## Converting and Calibrating

Convert either model with the [converter apps](../conversion/index.md) as usual.  The converters copy the `tiling` section into the compiled model unchanged, and each export's INT8 calibration snapshot matches its deployment: deployment-grid tiles for a tiled model, letterboxed whole frames for a whole-frame model.  A whole-frame snapshot at 4K is large: 500 samples take about 12.5 GB, against about 0.6 GB for 500 tiles.  See [Tiled Models](../conversion/calibration.md#tiled-models).

## Running Tiled Models

The [EdgeFirst Profiler](../../profiler/index.md) reads the `tiling` section of the model.  A model with `tiling.mode: tiled` is tiled automatically, whether the run is launched from Studio or on the target; a `whole_frame` model runs one inference per frame.  The profiler can also tile a model that was not trained with tiles, with `--sahi`.  See [Tiled Inference (SAHI)](../../profiler/concepts/sahi.md).

Applications tile with the [EdgeFirst HAL](https://github.com/EdgeFirstAI/hal), which provides the tile grid preprocessing and the IoS merge of per-tile detections for Rust, Python and C.  Read the grid overlap and merge settings from the model's `tiling` section so the application matches the deployment the model was validated for.

## Related Articles

- [ModelPack](../modelpack/index.md) and [Ultralytics](../ultralytics/index.md) launch form references
- [Model Metadata: Tiling](../metadata.md#tiling), the `tiling` section schema, grid and merge
- [Calibration Snapshot: Tiled Models](../conversion/calibration.md#tiled-models)
- [Tiled Inference (SAHI)](../../profiler/concepts/sahi.md) in the EdgeFirst Profiler
