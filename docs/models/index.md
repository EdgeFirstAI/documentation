# EdgeFirst Studio Model Zoo

The EdgeFirst Studio Model Zoo provides training support for multiple models, including [ModelPack](modelpack/index.md), [EdgeFirst Fusion](fusion/index.md) and [Ultralytics](ultralytics/index.md). These frameworks are fully integrated and can be configured directly through the user interface.

=== "ModelPack"

    ModelPack is a single-sensor (single-input) architecture of a Vision model tasked with detecting objects in an image via bounding boxes, segmentation masks, or both.  A Vision model is a type of model that interprets images or videos to perform tasks such as object detection, image classification, and much more.  EdgeFirst Studio supports Vision models tasked with object detection.

    * [Quick Start Guide](modelpack/tutorials/index.md)
    * [Training ModelPack](modelpack/training.md)
    * Validating ModelPack
        - [Managed](modelpack/validation/managed.md)
        - [User-Managed](modelpack/validation/user_managed.md)
    * [Deploying ModelPack](tutorials/deployment.md#modelpack)

    <div class="wizard-actions" markdown>
    [Read More → ](modelpack/index.md){ .md-button }
    </div>

=== "EdgeFirst Fusion"

    A Sensor Fusion Model is a multi-sensor (multi-input) architecture that fuses Radar and Camera sensors designed for spatial perception tasks.  These models can make predictions of the object's position in world coordinates.  Fusion models takes the Radar cube and the Camera image as inputs to the model by default.  However, either the Camera or the Radar can be turned off to train specific camera-only and radar-only based Fusion models. 

    * [Training Fusion Models](fusion/training.md)
    * Validating Fusion Models
        - [Managed](fusion/validation.md)
        - User Managed (*Coming Soon*)
    * [Deploying Fusion Models ](tutorials/deployment.md#fusion)

    [Read More → ](fusion/index.md){ .md-button }

=== "Ultralytics"

    [Ultralytics](https://docs.ultralytics.com/) YOLO which is a popular implementation of the ubiquitous 
    YOLO architecture for one-shot detection models, and capable for being applied to various other tasks such as instance segmentation
    
    [Read More → ](ultralytics/index.md){ .md-button }



!!! tip
    If you need support for additional models, please do not hesitate and emal <a href="mailto:support@edgefirst.ai">support@edgefirst.ai</a>

## Related Articles

1. [Vision Augmentations](augmentations.md) - Describes available vision augmentations for training and validation.
2. Validation Metrics- Describes the validation metrics for both architectures in detail. 
    - [Detection](metrics/detection.md)
    - [Segmentation](metrics/segmentation.md)
    - [Fusion](metrics/fusion.md)
