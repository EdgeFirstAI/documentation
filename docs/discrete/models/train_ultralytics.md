1. Click on "Model Experiments" of your created project

    {{ figure("/models/assets/training/model-experiments.jpg", "Model Experiments Page") }}

2. Create a new experiment

    {{ figure("/models/assets/training/create-experiment.jpg", "Model Experiments Page") }}

3. Navigate to the "Training Sessions"

    {{ figure("/models/assets/training/training-sessions.jpg", "Training Sessions") }}

4. Create a new training session by clicking the "Actions" dropdown menu on the top right of the page and then click the "+ New" button

    {{ figure("/models/assets/training/new-session-button.jpg", "New Session Button") }}

5. Start a YOLOv8n detection model by following these settings. Once the settings are set, click on "Start Session" at the bottom of the window

    {{ figure("/models/assets/training/training-session-attributes-ultralytics.jpg", "Ultralytics Training Settings") }}

    This will start a training session in progress.

    {{ figure("/models/assets/training/training-session-progress-ultralytics.jpg", "Ultralytics Training Progress") }}

    !!! failure "InsufficientInstanceCapacity"

        {{ img("/studio/assets/models/insufficient-capacity-error.jpg", "InsufficientInstanceCapacity Error") }}

        If you see this error after starting your training session, retry creating the session. This can happen when AWS reports that no EC2 instances are currently available to launch; the current workaround is to retry.

    !!! note "No Training Charts"

        {{ img("/models/assets/training/no-training-charts.jpg", "No Training Charts") }}

        Training sessions configured without epochs will not generate loss or metric charts, since the chart x-axis is epoch-based. This is expected behaviour.

    If you would like to know more about how to reproduce the benchmarks gathered in the [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models), please see [Training Configurations](../../profiler/concepts/configuration.md).

6. The completed training session should look like the following

    {{ figure("/models/assets/training/training-session-ultralytics-completed.jpg", "Ultralytics Training Completed") }}

7. We support model conversion and optimization workflows, enabling trained models to be deployed across a wide range of target platforms and hardware architectures.  Please follow the specific model conversion that matches your platform.  If you are using a Windows or macOS system, you can either follow the TFLite Converter workflow or proceed directly to the next section to validate the ONNX model, which is already provided as part of the training session outputs.

    | Converter | Supported Targets | Output Format | Docs |
    |-----------|------------------|---------------|------|
    | **TFLite Converter** | NXP i.MX 8M Plus (VIP8000), generic CPU/NPU TFLite delegates | `.tflite` flatbuffer | [TFLite Converter](../../models/conversion/tflite.md) |
    | **Neutron Converter** | NXP i.MX 95, i.MX 943/952, S32N79, MCX N54x/N94x, i.MX RT700, S32K5 | `.tflite` flatbuffer with Neutron microcode | [Neutron Converter](../../models/conversion/neutron.md) |
    | **TensorRT Converter** | NVIDIA Jetson (Orin Nano Super validated; broader lineup in progress) | `.tensorrt.zip` bundle (engine built on-device) | [TensorRT Converter](../../models/conversion/tensorrt.md) |
    | **Ara2 Converter** | NXP Ara240 DNPU | `.dvm` Dataflow Virtual Machine binary | [Ara2 Converter](../../models/conversion/ara2.md) |
    | **Hailo Converter** | Hailo-8 (26 TOPS), Hailo-8L (13 TOPS) | `.hef` Hailo Executable Format | [Hailo Converter](../../models/conversion/hailo.md) |

8. All converted models should appear under the model artifacts of the training session card.  Click on the training session card to expand for more details.

    {{ figure("/models/assets/conversion/yolov8n-det-model-artifacts.jpg", "YOLOv8n Detection Model Artifacts") }}

    Once you have converted your model, you can proceed towards profiling and validating the performance of your model next.
