# Training Vision Models

This tutorial describes the steps to train **Vision** models in EdgeFirst Studio.  Recall that Vision models are models that perform object detection in camera frames or images.  EdgeFirst Studio is capable of training ModelPack and Ultralytics object detection models.  For a tutorial to train Fusion models, see [Training Fusion Models](fusion.md).

## View Dataset

First ensure that the dataset is ready to be used for training.  This means that the dataset meets all of the criteria listed below.

- [x] Complete Annotations (bounding boxes and/or segmentation masks/polygons)
- [x] Contains training and validation partitions
- [x] Contains a dataset tag/version

The section [View Dataset](../../datasets/tutorials/management.md#view-dataset) will show an example of a completed dataset.

## Specify Project Experiments

From the [Projects page](../../studio/projects.md), choose the project that contains the dataset you plan to use.  In this example, the project chosen is called "My First Project".  Next click the "Model Experiments" button as indicated in red.

{{ figure("../assets/training/model-experiments.jpg", "Model Experiments") }}

{% include-markdown "discrete/models/create_model_experiments.md" %}

## Create Training Session

In the experiment card, click the "Training Sessions" button as indicated in red below.

{{ figure("../assets/training/training-sessions.jpg", "Training Sessions") }}

You will be greeted to the "Training Sessions" page as shown below.  

{{ figure("../assets/training/training-sessions-page.jpg", "Training Sessions Page") }}

Start a training session by clicking on the "Actions" button on the top right corner of the page and then click "+ New" as indicated.

{{ figure("../assets/training/new-session-button.jpg", "New Session Button") }}

You will be greeted with a training session dialog.  In this dialog, specify the "Trainer Type" to either "ModelPack" or "Ultralytics" and provide a name and description of the training session as shown below.  Next specify the dataset to be used with training and validation partitions.  In this example, the dataset specified is the "Coffee Cup" dataset which was used as an example under the [Getting Started](../../getting_started/capture_data.md).  Next specify the training parameters.  By default, object detection (bounding boxes) model will be trained.  However, you can specify either "Segmentation" or both.  Additional information on these parameters are provided by hovering over the info button ![Info Button](../../assets/buttons/studio-info-button.jpg).

!!! tip "Input Resolution"
    We recommend changing the input resolution to 640x360 to maximize detection rates on small datasets.

!!! warning "Large Batch Size"
    For small datasets, a large batch size may produce poor results. Use a batch size of 4 or 8.

For more information on available "Data Augmentations" please see [Vision Augmentations](../augmentations.md).

{{ figure("../assets/training/vision-train-settings.jpg", "Training Session Fields") }}

1. **Model Name**: This field specifies the name of the training session and will be used to name the artifacts (e.g. `modelpack-coffecup-640x640-rgba-t-<session ID>.tflite` or `modelpack-coffecup-640x640-rgba-t-<session ID>.onnx`)
2. **Description**: This field is used to add some hints about the training session.  Commonly used to highlight some parameters
3. **Training Data**: In this section the user must select the dataset as well as train/val groups
4. **Input Resolution**: The user can pick predefined input resolutions.  Even when ModelPack accepts any resolution we keep this option as simple as possible.  In case you need a different resolution to be supported, please reach out and [email our support team](mailto:support@edgefirst.ai)
5. **Camera Adaptor**: ModelPack accepts six different input optimizations.  It could be either of RGB, BGR, RGBA, BGRA, Greyscale, or YUYV
6. **Model Parameters**: This section configures the model architecture
    1. **Model Backbone**: Model backbone exposes a CSPDarknet19 optimized for boosting inference time and a CSPDarknet53 optimized for accuracy
    2. **Model Size**: Similar to modern architectures, ModelPack also accepts dynamic scaling factors (`width in [0.25, 0.5, 0.75, 1.0]`, `depth in [0.33, 0.33, 0.66, 1.0]`)
    3. **Activation Function**: This parameter defines the main activation used in the model. Exposed values are ReLU, ReLU6 and SiLU.  The best tradeoff between speed and accuracy is produced by ReLU6 activation in most of the cases
    4. **Interpolation Method**: Model upsample layers are ruled by a resize operation.  This operation can run with two different algorithms: `Bilinear` or `Nearest`
    5. **Object Detection**: Enables object detection task (enabled by default)
    6. **Segmentation**: Enables Semantic Segmentation
    7. **Space to Depth**: This feature enables the Space to Depth Transformation to the input in order to reduce model complexity on higher resolutions
    8. **Split Decoder**: Remove the decoder from the model and use a very optimized one from EdgeFirst.  This feature is very useful when the location of the boxes has to be precise (0-offset)
7. **Training Parameters**: In this section the user is able to specify the number of epochs to train the model as well as the batch size.  Remember the larger the input resolution the smaller the batch size
    1. **Enable Training** *(Ultralytics only)*: When enabled, the model is trained using the selected weights. When disabled (default), no training is performed — weights are pushed directly to the session artifacts. See [Enable Training and Use Default Weights](#enable-training-and-use-default-weights) below.

        !!! note "No Training Charts"
            Training sessions with **Enable Training** disabled will not generate loss or metric charts, since the chart x-axis is epoch-based. This is expected behaviour.

    2. **Use Default Weights**: When enabled (default), training starts from pre-trained COCO weights. When disabled, starting weights are sourced from a prior training session you specify.

8. **Data Augmentation**: This section controls the probability of each augmentation technique.  This feature is crucial for training models and reduce overfitting, especially in small datasets
9. **Export Parameters**: Allow the user to set a portion of data for calibration when exporting the model for INT8 quantization
10. **Start Session**: This button will start the training session

### Enable Training and Use Default Weights

The **Enable Training** checkbox (Ultralytics only) and **Use Default Weights** checkbox combine to control how the session is initialized and whether active training is performed:

| Use Default Weights | Enable Training | Behaviour |
|---------------------|-----------------|----------|
| ✓ Enabled | ✓ Enabled | Train from pre-trained COCO weights. |
| ✗ Disabled | ✓ Enabled | Train starting from weights of a prior training session you specify. |
| ✓ Enabled | ✗ Disabled | **Default.** No training. Pre-trained COCO weights are copied directly to the session artifacts. Results will be poor on non-COCO datasets — Studio displays a warning. This default exists because full COCO training for Ultralytics is compute-intensive, and it lets you reproduce validation and profiling results from the [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models) using the published COCO checkpoints. |
| ✗ Disabled | ✗ Disabled | No training. Weights are copied from a specified prior training session — equivalent to cloning that session's artifacts. |

!!! warning "COCO pre-trained weights and dataset compatibility"
    The **Use Default Weights** option initializes from pre-trained COCO weights. These weights can technically be used as a starting point for any dataset, but **if your dataset labels have no overlap with COCO category names, validation accuracy will be very poor** — the model's class outputs will not correspond to your labels.

    For best transfer-learning results, ensure your label names match the relevant COCO categories, or supply a prior EdgeFirst training session as the starting weights.

!!! failure "InsufficientInstanceCapacity"

    {{ img("/studio/assets/models/insufficient-capacity-error.jpg", "InsufficientInstanceCapacity Error") }}

    If you see this error after starting your training session, retry creating the session. This can happen when AWS reports that no EC2 instances are currently available to launch; the current workaround is to retry.

## Session Progress

Once the training session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

{{ figure("../assets/training/vision-session-progress.jpg", "Training Session") }}

The training process begins with cloud instance initialization. Then the dataset is downloaded and cached.  Training starts afterwards.
At the end of the training process, the model is quantized and the model artifacts will be published on the training session available for download.

## Completed Session

The completed session will look as follows with the status set to "Complete".

{{ figure("../assets/training/vision-completed-session.jpg", "Completed Session") }}

The attributes of the training sessions in EdgeFirst Studio are labeled below.

{{ figure("../assets/training/training-session-attributes.jpg", "Training Session Attributes") }}

## Training Outcomes

Once the training session completes, you can view the training charts by clicking the "view training session charts" button on the top of the session card.

{{ figure("../assets/training/vision-charts.jpg", "Training Charts") }}

You can go back to the training session card by pressing the "Back" button as indicated in red below on the top left corner of the page.

{{ figure("../assets/training/back-button.jpg", "Back to the Session Card") }}

The trained model artifacts can be downloaded by clicking the session card.  This will open the session details and the models are listed under the "Artifacts" tab as shown below.  Click on the downward arrows to download the models to your PC.

{{ figure("../assets/training/vision-session-artifacts.jpg", "Training Session Artifacts") }}

It is also possible to compare the training metrics for multiple sessions.  See [Training Sessions](../../studio/models.md#training-sessions) in the Model Experiments Dashboard for further details.

!!! info "Netron"
    You can visualize the architecture of these models using [https://netron.app/](https://netron.app/).

## Next Steps

Now that you have trained your model, you can validate the performance of your model either [on target/device](../validation/vision/user_managed.md) or on the [cloud](../validation/vision/managed.md).
