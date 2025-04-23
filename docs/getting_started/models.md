# Model Training, Validation, and Deployment

EdgeFirst Studio supports *Vision Models* trained using **ModelPack** and *Spatial Perception Models* also known as **Fusion** models.

## ModelPack Tutorials

ModelPack is a single-sensor (single-input) architecture of a Vision model tasked with detecting objects in an image via bounding boxes, segmentation masks, or both. A Vision model is a type of model that interprets images or videos to perform tasks such as object recognition, image classification, and much more. EdgeFirst Studio supports Vision models tasked with object recognition.

* [Training ModelPack](../models/modelpack/training.md)
* [Validating ModelPack](../models/modelpack/validation.md)
* [Deploying ModelPack](../models/modelpack/deployment.md)

## Sensor Fusion Tutorials

A Sensor Fusion Model is a multi-sensor (multi-input) architecture that fuses Radar and Camera sensors designed for spatial perception tasks. These models can make predictions of the object's position in world coordinates. Fusion models takes the Radar cube and the Camera image as inputs to the model by default. However, either the Camera or the Radar can be turned off to train specific camera-only and radar-only based Fusion models. 

* [Training Fusion Models](../models/fusion/training.md)

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Q8uiYJb1HJ4" title="EdgeFirst Training" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

* [Validating Fusion Models](../models/fusion/validation.md)

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/oKh4k0CCLmU?si=PPmbJ1-8dZPLhGh2" title="EdgeFirst Validation" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

* [Deploying Fusion Models](../models/fusion/deployment.md)
