# Model Tutorials

EdgeFirst Studio supports *Vision Models* trained using **ModelPack** and *Spatial Perception Models* also known as **Fusion** models.

## ModelPack

[ModelPack](../../models/modelpack/index.md) is a single-sensor (single-input) architecture of a Vision model tasked with detecting objects in an image via bounding boxes, segmentation masks, or both.  A Vision model is a type of model that interprets images or videos to perform tasks such as object recognition, image classification, and much more.  EdgeFirst Studio supports Vision models tasked with object recognition.

# Fusion

A [Sensor Fusion Model](../../models/fusion/index.md) is a multi-sensor (multi-input) architecture that fuses Radar and Camera sensors designed for spatial perception tasks.  These models can make predictions of the object's position in world coordinates.  Fusion models takes the Radar cube and the Camera image as inputs to the model by default.  However, either the Camera or the Radar can be turned off to train specific camera-only and radar-only based Fusion models. 