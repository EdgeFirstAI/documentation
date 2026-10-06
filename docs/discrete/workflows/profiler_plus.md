## Create an Ultralytics Training Session

{% include-markdown "discrete/models/train_ultralytics.md" heading-offset=0 %}

## Validate on Target with the EdgeFirst Profiler

The Profiler+ workflow validates your model directly on your target hardware — not in the cloud. This gives you real inference latency, NPU utilization, and per-stage timing alongside accuracy metrics.

!!! info "Cloud validation not used here"
    Cloud validation only supports ONNX, Keras, and TFLite artifacts running on a cloud instance. On-target profiling with the EdgeFirst Profiler supports all converted formats (`.tflite`, `.hef`, `.dvm`, `.tensorrt.zip`) and measures real hardware performance.

### Install the profiler

=== "Python (pip)"

    ```sh
    pip install edgefirst-profiler
    ```

=== "Linux / macOS"

    ```sh
    curl -fsSL https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.sh | bash
    ```

!!! note "ONNX Runtime Library"
    Install the ONNX Runtime library `pip install onnxruntime` if it is missing
    from your system to profile ONNX models.

    {{ figure("/models/assets/validation/missing_onnxruntime.jpg", "Missing ONNXRuntime Library") }}

Confirm the install:

```sh
edgefirst-profiler --version
```

For per-platform guides including NPU delegate setup, see the [Profiler Installation](../../profiler/installation/index.md) section.

### Sign in to EdgeFirst Studio

```sh
edgefirst-profiler login
```

The interactive prompt asks for **server**, **username**, and **password**. Credentials are saved locally and refresh automatically.

### Run a validation session

Launch the profiler TUI:

```sh
edgefirst-profiler
```

Press **F2** to open the Studio screen, then navigate to your training session:

```text
Projects  →  Experiments  →  Training Sessions  →  Artifacts
```

Select the converted model artifact that matches your target hardware and choose **Validate**. The profiler creates a validation session in Studio, downloads the model and dataset to the device, and starts the run automatically.

The **F4 Profiler** dashboard streams iteration-level latency and per-stage timings live during the run. When complete, predictions and the timing trace upload to EdgeFirst Studio where mAP, precision-recall curves, and the trace viewer are generated.

In EdgeFirst Studio, you can see the validation session by navigating to the validation sessions under "Model Experiments".

{{ figure("/models/assets/validation/validation-sessions.jpg", "Validation Session") }}

The metrics of the validation session can be viewed by clicking on the "charts" button on the validation session card.

{{ figure("/models/assets/validation/profiler_completed_validation.jpg", "Validation Charts") }}

For the full walkthrough see [Profiler Quick Start](../../profiler/quickstart.md) and [Validation from the Profiler](../../profiler/studio/from_profiler.md).

## Compare Results to the Model Zoo

After validation, compare your results with the [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models) to see how close your model is to the published baselines.

{{ figure("/models/assets/validation/profiler_baselines.jpg", "EdgeFirst Profiler Baselines") }}

Focus on:

- **Task match**: Use the same task type (detection, segmentation, classification) as your training run.
- **Input modality**: Compare vision-only models against vision-only baselines, and fusion models against fusion baselines.
- **Metric alignment**: Match the primary metric (for example, mAP or F1) to ensure an apples-to-apples comparison.
- **Latency vs accuracy**: Look at accuracy and throughput together to understand the practical edge tradeoff.
