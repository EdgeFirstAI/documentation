# Apps Dashboard

The Studio Apps page is a catalog that lists all available EdgeFirst apps. Apps extend
the platform with custom processing pipelines such as data import, model training,
conversion, validation, and profiling.

To access this page, click the **Apps** waffle icon in the top navigation bar and select
**Apps** from the menu.

{{ figure("assets/apps-page.png", "Studio Apps Marketplace") }}

## Search And Filter

The top of the Apps page provides filters to help narrow the catalog:

- **Name**: Search by the app package or internal app name.
- **Title**: Search by the user-facing app title.
- **Author**: Filter apps by publisher.
- **Type**: Filter by app category such as AIGT, Converter, Exporter, Importer,
  Profiler, Trainer, or Validator.

When a type filter is active, a **Clear Filter** button appears so you can return to the
full catalog.

## App Categories

When no type filter is selected, the Apps page first shows category cards rather than
individual app cards. Each category card summarizes one app type and includes:

- **Category name** such as Converter or Importer.
- **Description** of what that class of apps is used for.
- **Apps** count showing how many apps are available in that category.
- **Free** count showing how many apps in the category have no hourly cost.
- **Author** dropdown for narrowing that category by publisher.

Clicking a category card, or choosing a specific value in the **Type** filter, opens the
list of individual apps for that category.

## App Cards

After selecting a category, each app is displayed as a detailed card with the following
information:

- **Title** — The display name of the app.
- **Type** — The app category, such as `converter`.
- **Preview image** — A visual identifier for the app.
- **Description** — A brief summary of what the app does.
- **Package ID and Version** — The internal package identifier and published version,
  shown together, for example `edgefirst-studio-neutron : 1.4.1`.
- **Runs** — The total number of executions recorded for the app.
- **Author** — The organization or individual that published the app.
- **Help** — A link to the app's full documentation page.
- **Pricing** — The per-hour compute cost, or **Free** if there is no charge.

!!! note "Apps are launched from their workflow"
    The Apps page is a catalog only. Apps are not launched directly from this page.
    Each app is started from the relevant point in its workflow. For example,
    Converter Apps are launched from a completed training session's *Artifacts* tab.
    Once started, the app run is tracked in the [Tasks page](tasks.md).

## Available Apps

EdgeFirst Studio ships with the apps described below. Each app is documented in more
detail on its own help page, linked from its card and from the sections that follow.

### App Types

The Apps page groups apps into the following categories:

- **Converter**: Converts a trained model into a deployment-ready artifact for a target
  runtime or accelerator.
- **Exporter**: Packages datasets, annotations, or model outputs into an external format
  for download or use outside Studio.
- **Importer**: Brings external data such as images, videos, MCAPs, or local datasets
  archives into Studio.
- **Profiler**: Runs on-target measurement and produces timing traces, predictions, and
  performance artifacts for validation.
- **Trainer**: Launches model training jobs for either ModelPack or Ultralytics and produces training sessions, checkpoints,
  and deployment artifacts.
- **Validator**: Evaluates trained or profiled models and produces quality metrics,
  charts, and reports.

### Importer Apps

Importer Apps are used to bring external data into EdgeFirst Studio and convert it into a
Dataset that can be labeled, grouped, trained, and validated. These workflows are typically
launched from the dataset context menu and accept files from a local machine or an external
recording workflow.

The available importer workflows include:

- **Images** — Import image folders or collections into a dataset. See [Import Images](../datasets/tutorials/import.md#import-images).
- **Videos** — Import video files and convert them into dataset frames for annotation and training. See [Import Videos](../datasets/tutorials/import.md#import-videos).
- **Darknet Dataset** — Import YOLO/Darknet-style image and label directories, including split or unsplit layouts. See [Import Darknet Datasets](../datasets/tutorials/import.md#import-darknet-datasets).
- **EdgeFirst Dataset** — Import a packaged EdgeFirst dataset archive containing the dataset and annotation files. See [Import EdgeFirst Datasets](../datasets/tutorials/import.md#import-edgefirst-datasets).
- **MCAP / Recording Upload** — Upload MCAP recordings captured from an EdgeFirst platform and restore them into a dataset. See [Upload MCAP](../datasets/tutorials/capture.md#upload-mcap) and [MCAP Publishing](../perception/data_collection/publishing.md).

Together, these importer apps cover the common onboarding paths for raw media, annotated data,
third-party dataset formats, and platform recordings.

### Exporter Apps

Exporter Apps package Studio assets into portable files that can be downloaded, archived,
shared externally, or used in downstream tools. Unlike Importer Apps, which bring data
into Studio, Exporter Apps take data already created inside EdgeFirst Studio and convert it
into an external artifact.

The most common export workflows are:

- **Dataset export** — Export a dataset, annotations, or image links for local storage or
  downstream processing. See [Export Dataset](datasets/index.md#export-dataset).
- **Snapshot export** — Save a frozen dataset version as a reusable artifact. See
  [Snapshots](snapshots.md).
- **Model artifact export (work in progress)** — Package trained or converted model outputs for deployment,
  benchmarking, or external tooling. See [Model Conversion](../models/conversion/index.md)
  and [ModelPack](../models/modelpack/index.md).
- **Validation or profiling results (work in progress)** — Download derived metrics, traces, and reports from a
  completed session for analysis outside Studio.

In practice, an exporter app is the step that turns an in-platform result into a file you can
store locally, move between systems, or hand off to another workflow.

### Trainer Apps

Trainer Apps produce vision models for a dataset and publish the model, its [metadata](../models/metadata.md) and an INT8 calibration snapshot to a training session. A Training App is launched from an experiment's *Training Sessions* page, where its launch form collects the dataset, the destination experiment and the training parameters. The session runs on a cloud GPU instance.  See [Training Vision Models](../models/training/vision.md).

#### ModelPack

Trains ModelPack object detection, semantic segmentation and multitask models, with optional Input Tiling (SAHI) for small objects in high-resolution images.  See [ModelPack](../models/modelpack/index.md).

#### Ultralytics

Trains or exports Ultralytics YOLO detection and instance segmentation models, starting from COCO pretrained weights or a previous session's weights, with optional Input Tiling for detection.  See [Ultralytics](../models/ultralytics/index.md).

### Converter Apps

Converter Apps turn a completed training session's framework-native artifact (a
TensorFlow SavedModel or an ONNX graph) into a deployment-ready binary for a specific
target, embedding the [EdgeFirst model metadata](../models/metadata.md) so the runtime can
decode the model's outputs with no per-target glue code. A Converter App is launched from
a training session's *Artifacts* tab. Most converters apply the **EdgeFirst Smart
Quantizer** to recover INT8 accuracy without retraining. For the full conversion
workflow, the Smart Quantization mechanism, per-converter behavior, and calibration, see
[Model Conversion](../models/conversion/index.md).

#### TFLite Converter

Converts a SavedModel into a quantized `.tflite` flatbuffer for NXP i.MX 8M Plus and
generic CPU/NPU TFLite delegates, applying per-scale Smart Quantization. See
[TFLite Conversion](../models/conversion/tflite.md).

#### Neutron Converter

Re-encodes a TFLite model with Neutron microcode for NXP i.MX 95 and other NXP eIQ
Neutron silicon. See [Neutron Conversion](../models/conversion/neutron.md).

#### TensorRT Converter

Bundles an ONNX graph into a `.tensorrt.zip` for an on-device TensorRT engine build on
NVIDIA Jetson (FP16 path). See [TensorRT Conversion](../models/conversion/tensorrt.md).

#### Ara2 Converter

Converts a model into a `.dvm` Dataflow Virtual Machine binary for the NXP Ara240 DNPU,
with per-scale split and optional INT16 DFL promotion. See
[Ara2 Conversion](../models/conversion/ara2.md).

#### Hailo Converter

Compiles a model into a `.hef` Hailo Executable Format binary for Hailo-8 and Hailo-8L
NPUs, with structurally-required per-scale Smart Quantization. See
[Hailo Conversion](../models/conversion/hailo.md).

!!! info "App Marketplace"
    The available apps may change as new apps are published. Per-app pricing is shown on
    each app card and reflected in your [billing](user/billing.md). Contact
    [support@edgefirst.ai](mailto:support@edgefirst.ai) for information on publishing
    your own apps to the marketplace.

### EdgeFirst Profiler

The on-target measurement engine. The Profiler runs the complete vision pipeline —
decode, preprocess, inference, postprocess, and NMS — on the target hardware your model
will deploy to, then publishes per-image predictions and a detailed timing trace back to
EdgeFirst Studio. Studio uses those artifacts to generate the accuracy metrics, timing
charts, and trace visualizations for the validation session. See
[Profiler](../profiler/index.md).

### EdgeFirst Validator

The Studio-side companion to the Profiler. The Validator post-processes the predictions
and timing traces produced by a profiling run to compute COCO/LVIS accuracy metrics
(such as mAP and mIoU) and timing charts, then publishes the results to the validation
session. See [Validation Metrics](../models/validation/metrics/index.md).

## Next Steps

- [Model Conversion](../models/conversion/index.md) — the conversion workflow, Smart
  Quantization, and per-converter launch options.
- [Profiler](../profiler/index.md) — on-target profiling and validation runs.
- [Validation Metrics](../models/validation/metrics/index.md) — how accuracy and timing
  results are computed and presented.
