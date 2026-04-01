# ModelPack Overview

ModelPack is an advanced computer vision solution developed by Au-Zone Technologies as part of their EdgeFirst.AI middleware. It provides both object detection and semantic segmentation capabilities, enabling high-performance, low-latency AI inference on embedded devices, particularly those with AI accelerators (NPUs) in the 0.5 TOPS and up range.

| Detection                   | Segmentation                | Multitask                     |
|-----------------------------|-----------------------------|-------------------------------|
| ![Detection](../assets/detection-sample.png) | ![Segmentation](../assets/segmentation-sample.png) | ![Multitask](../assets/multitask-sample.png) |

ModelPack is optimized for real-time vision applications such as industrial automation, robotics, and autonomous systems. It combines object detection — locating multiple objects within an image using bounding boxes — with instance segmentation, which outlines each object’s exact shape at the pixel level. This unified approach enables detailed scene understanding at the edge and can contribute in a late fusion with the radar model.

## Getting Started

ModelPack can be trained now in EdgeFirst Studio using a Graphical User Interface by following four simple steps:

=== "Select Framework"

    <h2 id="select-framework" style="display: none;"></h2>

    1. Select **ModelPack** within the available training frameworks.

    {{ img("../assets/modelpack/modelpack-train-01.jpg", "Select ModelPack Training Framework") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [Next → 2. Name Session](#name-session){ .md-button .md-button--primary }
    </div>

=== "Name Session"

    <h2 id="name-session" style="display: none;"></h2>

    2. Set a **name** and **description** *(optional)* for the training session.

    {{ img("../assets/modelpack/modelpack-train-02.jpg", "Set Name and Description") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [1. Select Framework ← Back](#select-framework){ .md-button }
    [Next → 3. Select Dataset](#select-dataset){ .md-button .md-button--primary }
    </div>

=== "Select Dataset"

    <h2 id="select-dataset" style="display: none;"></h2>

    3. Choose your **dataset**.

    {{ img("../assets/modelpack/modelpack-train-03.jpg", "Select a Dataset") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [2. Name Session ← Back](#name-session){ .md-button }
    [Next → 4. Configure & Train](#train){ .md-button .md-button--primary }
    </div>

=== "Train"

    <h2 id="train" style="display: none;"></h2>

    4. **[Configure model parameters](#training-parameters)** (architecture, input size, epochs, etc.) and start **Training**.

    {{ img("../assets/modelpack/modelpack-train-04.jpg", "Configure and Train") }}{ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [3. Select Dataset ← Back](#select-dataset){ .md-button }
    [Next → 5. Validate](../validation/vision/managed.md){ .md-button  .md-button--primary }
    </div>

=== "Training Parameters"

    <h2 id="training-parameters" style="display: none;"></h2>

    1. **Model Name**: This field specifies the name of the training session and will be used to name the artifacts (e.g. `modelpack-coffecup-640x640-rgba-t-<session ID>.tflite` or `modelpack-coffecup-640x640-rgba-t-<session ID>.onnx`).
    2. **Description**: This field is used to add some hints about the training session.  Commonly used to highlight some parameters.
    3. **Training Data**: In this section the user must select the dataset as well as train/val groups.
    4. **Input Resolution**: The user can pick predefined input resulutions.  Even when ModelPack accepts any resolution we keep this option as simple as possible.  In case you need a different resolution to be supported, please reach out and [email our support team](mailto:support@edgefirst.ai).
    5. **Camera Adaptor**: ModelPack accepts three different input optimizations.  It could be either of RGB, RGBA, or YUYV.
    6. **Model Parameters**: This section configures the model architecture. 
        1. **Model Backbone**: Model backbone exposes a CSPDarknet19 optimized for boosting inference time and a CSPDarknet53 optimized for accuracy.
        2. **Model Size**: Similar to modern architectures, ModelPack also accepts dynamic scaling factors (`width in [0.25, 0.5, 0.75, 1.0]`, `depth in [0.33, 0.33, 0.66, 1.0]`).
        3. **Activation Function**: This parameter defines the main activation used in the model. Exposed values are ReLU, ReLU6 and SiLU.  The best tradeoff between speed and accuracy is produced by ReLU6 activation in most of the cases.
        4. **Interpolation Method**: Model upsample layers are ruled by a resize operation.  This operation can run with two different algorithms: `Bilinear` or `Nearest`.
        5. **Object Detection**: Enables object detection task (enabled by default).
        6. **Segmentation**: Enables Semantic Segmentation.
        7. **Space to Depth**: This feature enables the Space to Depth Transformation to the input in order to reduce model complexity on higher resolutions.
        8. **Split Decoder**: Remove the decoder from the model and use a very optimized one from EdgeFirst.  This feature is very useful when the location of the boxes has to be precise (0-offset).
    7. **Training Parameters**: In this section the user is able to specify the number of epochs to train the model as well as the batch size.  Remember the larger the input resolution the smaller the batch size. 
    8. **Data Augmentation**: This section controls the probablity of each augmentation technique.  This feature is crucial for training models and reduce overfitting, especially in small datasets.
    9. **Start Session**: This button will start the training session.

## ModelPack Architecture

ModelPack is a modern object detector and it adopts similar scaling strategies seen in the YOLO family models.
The model expands and contracts based on the width and height parameters.
Modelpack shares two main backbones: a Darknet53 backbone similar to [YOLOx](https://arxiv.org/pdf/2107.08430v2) which maximizes accuracy and a Darknet19 backbone for boosting inference time.
Different than YOLOx, ModelPack is NOT anchor free, which makes the model more accurate and stable after quantization.

{{ figure("../assets/darknet-53-backbone.png", "Darknet-53 Backbone") }}

Figure reproduced from: [Yang, L., Chen, G. & Ci, W. Multiclass objects detection](https://asp-eurasipjournals.springeropen.com/articles/10.1186/s13634-023-01045-8)

As mentioned above, ModelPack merges Semantic Segmentation and Object Detection on the same model and it is user responsibility depending on problem requirements.  Semantic Segmentation only uses two scales (Scale 1 and Scale 2). On the other hand, Object Detection task uses the three scales.

While solving both tasks in the same inference cycle, the three scales are used.

{{ figure("../assets/modelpack-arch.png", "ModelPack Architecture") }}

ModelPack outputs can be configured on Studio User Interface as explained in the [ModelPack training guide](../training/vision.md).
