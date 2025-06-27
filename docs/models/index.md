# EdgeFirst Models

EdgeFirst Studio supports two model architectures: **ModelPack** and **Fusion**.

1. [ModelPack](modelpack/index.md)

    ModelPack is a single-sensor (single-input) architecture of a Vision model tasked with detecting objects in an image via bounding boxes, segmentation masks, or both.  A Vision model is a type of model that interprets images or videos to perform tasks such as object detection, image classification, and much more.  EdgeFirst Studio supports Vision models tasked with object detection.

    * [Quick Start Guide](modelpack/tutorials/index.md)
    * [Training ModelPack](modelpack/training.md)
    * Validating ModelPack
        - [Managed](modelpack/validation/managed.md)
        - [User-Managed](modelpack/validation/user_managed.md)
    * [Deploying ModelPack](tutorials/deployment.md#modelpack)

2. [Fusion](fusion/index.md)

    A Sensor Fusion Model is a multi-sensor (multi-input) architecture that fuses Radar and Camera sensors designed for spatial perception tasks.  These models can make predictions of the object's position in world coordinates.  Fusion models takes the Radar cube and the Camera image as inputs to the model by default.  However, either the Camera or the Radar can be turned off to train specific camera-only and radar-only based Fusion models. 

    * [Training Fusion Models](fusion/training.md)
    * Validating Fusion Models
        - [Managed](fusion/validation.md)
        - User Managed (*Coming Soon*)
    * [Deploying Fusion Models ](tutorials/deployment.md#fusion)

!!! note
    Click on the links for more information on each architecture and the relevant workflows.

Related articles are provided below:

1. [Vision Augmentations](augmentations.md) - Describes available vision augmentations for training and validation.
2. Validation Metrics- Describes the validation metrics for both architectures in detail. 
    - [Detection](metrics/detection.md)
    - [Segmentation](metrics/segmentation.md)
    - [Fusion](metrics/fusion.md)
