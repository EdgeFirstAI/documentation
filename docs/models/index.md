# EdgeFirst Studio Model Zoo

The EdgeFirst Studio Model Zoo provides training support for multiple models, including [ModelPack](modelpack/index.md), [EdgeFirst Fusion](fusion/index.md), and [Ultralytics](ultralytics/index.md). These frameworks are fully integrated and can be configured directly through the user interface.

=== "ModelPack"

    ModelPack is a single-sensor (single-input) architecture of a Vision model tasked with detecting objects in an image via bounding boxes, segmentation masks, or both.  A Vision model is a type of model that interprets images or videos to perform tasks such as object detection, image classification, and much more.  EdgeFirst Studio supports Vision models tasked with object detection.

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](modelpack/index.md){ .md-button }
    </div>

=== "EdgeFirst Fusion"

    A Sensor Fusion Model is a multi-sensor (multi-input) architecture that fuses Radar and Camera sensors designed for spatial perception tasks.  These models can make predictions of the object's position in world coordinates.  Fusion models takes the Radar cube and the Camera image as inputs to the model by default.  However, either the Camera or the Radar can be turned off to train specific camera-only and radar-only based Fusion models. 

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](fusion/index.md){ .md-button }
    </div>

=== "Ultralytics"

    [Ultralytics](https://docs.ultralytics.com/) YOLO which is a popular implementation of the ubiquitous 
    YOLO architecture for one-shot detection models, and capable for being applied to various other tasks such as instance segmentation.
    
    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](ultralytics/index.md){ .md-button }
    </div>

!!! tip "Build Your Own Model (BYOM)"
    📬 If you need support for additional models,
    please do not hesitate and [email our support team](mailto:support@edgefirst.ai) — we’re here to help!

## Related Articles

1. [Vision Augmentations](augmentations.md) - Describes available vision augmentations for training and validation.
2. [Model Metadata](metadata.md) - Documents the metadata schema embedded in EdgeFirst models for MLOps traceability.
3. Validation Metrics - Describes the validation metrics for both architectures in detail.
    - [Detection](validation/metrics/detection.md)
    - [Segmentation](validation/metrics/segmentation.md)
    - [Fusion](validation/metrics/fusion.md)
