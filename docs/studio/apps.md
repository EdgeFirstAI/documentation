# Studio Apps Dashboard

The Studio Apps page lists all available EdgeFirst apps that can be run directly from
EdgeFirst Studio.  Apps extend the platform with custom processing pipelines such as data import, model training, conversion, validation, and profiling.

To access this page, click the **Apps** waffle icon in the top navigation bar and select
**Apps** from the menu.

{{ figure("assets/apps-page.png", "Studio Apps Marketplace") }}

## App Cards

Each app is displayed as a card with the following information:

- **Name** — The display name of the app.
- **Description** — A brief summary of what the app does.
- **Package ID** (package field) — The internal package identifier used by the platform.
- **Version** — The currently published version of the app.
- **Author** — The organization or individual that published the app.
- **Help** — A link to the app's full documentation page.
- **Runs** — The total number of executions recorded for this app across the organization.
- **Pricing** — The per-hour compute cost, or **Free** if there is no charge.

Click the **Run** button on an app card to launch the app.  A configuration dialog will
appear to set the app's input parameters before execution begins.  Once started, the
app run is tracked in the [Tasks panel](navigation.md#tasks).

## Available Apps

The following apps are available by default in EdgeFirst Studio:

| App | Description | Pricing |
|---|---|---|
| **Roboflow Importer** | Import datasets from Roboflow into EdgeFirst Studio. | Free |
| **EdgeFirst Profiler** | Profile model inference pipelines and produce Perfetto traces. | Free |
| **EdgeFirst Validator** | Post-process predictions and Perfetto traces to compute COCO/LVIS accuracy metrics and timing charts, then publish results to the validation session. | Free |
| **TensorRT Converter** | Convert ONNX models to TensorRT `.engine` plans cross-compiled for NVIDIA Jetson. | $1/hour |
| **TFLite Converter** | Convert a SavedModel to TFLite with optional INT8 quantization, per-channel calibration, and configurable split support. | $1/hour |

!!! info "App Marketplace"
    The available apps may change as new apps are published.  Contact
    [support@edgefirst.ai](mailto:support@edgefirst.ai) for information on publishing
    your own apps to the marketplace.

## Next Steps

For details on running model conversion apps, see [Model Conversion](../models/conversion/tflite.md).
For the TensorRT converter, see [TensorRT Conversion](../models/conversion/tensorrt.md).
