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

    4. **Configure model parameters** (architecture, input size, epochs, etc.) and start **Training**.

    {{ img("../assets/ultralytics/ultralytics-train-04.jpg", "Configure and Train") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [3. Select Dataset ← Back](#select-dataset){ .md-button }
    [Next → 5. Validate](../validation/vision/managed.md){ .md-button  .md-button--primary }
    </div>

=== "Training Parameters"

    <h2 id="training-parameters" style="display: none;"></h2>

    1. **Model Name**: This field specifies the name of the training session and will be used to name the artifacts (e.g. `yolov8n-coffecup-640x640-rgb-t-<session ID>.tflite` or `yolov8n-coffecup-640x640-rgb-t-<session ID>.onnx`).
    2. **Description**: This field is used to add some hints about the training session.  Commonly used to highlight some parameters
    3. **Training Data**: In this section the user must select the dataset as well as train/val groups
    4. **Input Resolution**: The user can pick predefined input resolutions.  In case you need a different resolution to be supported, please reach out and [email our support team](mailto:support@edgefirst.ai)
    5. **Camera Adaptor**: Ultralytics accepts six different input optimizations.  It could be either of RGB, BGR, RGBA, BGRA, Greyscale, or YUYV
    6. **Model Parameters**: This section configures the model architecture
        1. **Model Task**: This can be either "Detection" or "Segmentation". Note for Ultralytics segmentation refers to instance segmentation
        2. **Model Version**: The Ultralytics version to train from the choices (v5, v8, v11, v26)
        3. **Model Size**: The size of the model from the choices (Nano, Small, Medium, Large, XLarge)
    7. **Training Parameters**: In this section the user is able to specify the number of epochs to train the model as well as the batch size.  Remember the larger the input resolution the smaller the batch size 
    8. **Export Parameters**: Allow the user to set a portion of data for calibration when exporting the model for INT8 quantization. This section also allow the user to set the ONNX opset version
    9. **Export Pretrained Weights**: A checkbox to export the default pretrained weights from Ultralytics
    10. **Start Session**: This button will start the training session

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

The **Camera Adaptor** dropdown is available when configuring a training session, allowing you to select the target camera format for your deployment platform. This trains the model to accept native camera output (BGR, RGBA, YUYV, etc.) without runtime conversion.

See [Camera Adaptor](../cameraadaptor.md) for details on supported formats and platform guidance.

## Custom Models

If you have a custom float model, it is highly recommended to [export to a quantized model](../conversion/tflite.md) to deploy and maximize the model's performance using the target's NPU.

Deploying a quantized TFLite on the **i.MX 95 EVK** requires an extra step of [converting the model using NXP's eIQ neutron converter](../conversion/neutron.md).  This will allow the model to be deployed on the i.MX 95 using the Neutron delegate in the platform.

!!! warning "Specific BSP versions required"

    The latest BSP available for the Maivin lacks the `onnxruntime` library needed to run ONNX on the NPU.

    On the i.MX 8M Plus EVK, BSP v5.15 are used in the examples which was noted to have the providers needed for ONNX to run on the NPU `NnapiExecutionProvider`, `VsiNpuExecutionProvider`.  Later BSPs such as v6.12 did not have these providers.  This still needs confirmation from NXP as to why these providers were removed. 

## License

Ultralytics YOLO is covered by the GNU AGPL-3.0 license which allows for free use of this model within the constraints of the license.  Ultralytics offers [commercial licensing options](https://www.ultralytics.com/license).
