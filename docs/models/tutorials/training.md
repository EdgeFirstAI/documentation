# Training

EdgeFirst Studio supports training of *Vision* models using ModelPack tasked for image object detection and the training of "Fusion" models tasked for predicting the object's position in the field.  During training, the datasets with 2D annotations (segmentation masks and 2D bounding boxes) are used for training ModelPack and 3D annotations (3D bounding boxes) are used for training Fusion. 

[Vision augmentation techniques](../augmentations.md) are also applied during training to enhance the model's performance in a variety of conditions and to increase the number of training samples. 

## ModelPack

[ModelPack](../modelpack/index.md) is a single-sensor (single-input) architecture of Vision models tasked with detecting objects in an image via bounding boxes, segmentation masks, or both.  A Vision model is a type of model that interprets images or videos to perform tasks such as object detection, image classification, and much more.  EdgeFirst Studio supports Vision models tasked with object detection.

For training *Vision* models tasked with detecting objects in an image, follow tutorials for [Training ModelPack](../modelpack/training.md) in EdgeFirst Studio.  

## Fusion

A [Sensor Fusion Model](../fusion/index.md) is a multi-sensor (multi-input) architecture that fuses Radar and Camera sensors designed for spatial perception tasks.  These models can make predictions of the object's position in world coordinates.  Fusion models takes the Radar cube and the Camera image as inputs to the model by default.  However, the Camera or the Radar can be turned off to train specific camera-only and radar-only based Fusion models. 

For training *Spatial Perception Models* tasked with detecting the position of the object in the field, follow tutorials for [Training Fusion Models](../fusion/training.md) in EdgeFirst Studio. 

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Q8uiYJb1HJ4" title="EdgeFirst Training" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
