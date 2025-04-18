# Modelpack Overview

ModelPack (MPK) is an advanced computer vision solution developed by Au-Zone Technologies as part of their EdgeFirst.AI middleware. It provides both object detection and instance segmentation capabilities, enabling high-performance, low-latency AI inference on embedded devices—particularly those leveraging NXP’s processors and hardware accelerators.

| Detection                   | Segmentation                | Multitask                     |
|-----------------------------|-----------------------------|-------------------------------|
| ![Detection](../assets/detection-sample.png) | ![Segmentation](../assets/segmentation-sample.png) | ![Multitask](../assets/multitask-sample.png) |



MPK is optimized for real-time vision applications such as industrial automation, robotics, and autonomous systems. It combines object detection—locating multiple objects within an image using bounding boxes—with instance segmentation, which outlines each object’s exact shape at the pixel level. This unified approach enables detailed scene understanding at the edge and can contribute in a late fusion with the radar model.


The architecture is higly configurable form the API via width and height parameters. These hyperparameters expand the model in both directions, width and depth. There are 4 predifined versions of ModelPack which are mainluy focused for embedded deployments: nano, tiny, small and medium. 


|   Variant           | Parameters | Width | Height | COCO mAP |
|---------------------|------------|-------|--------|----------|
| **modelpack-nano**  |    2.5M    | 0.25  | 0.33   |     -    |
| **modelpack-tiny**  |    5.5M    | 0.35  | 0.33   |     -    |
| **modelpack-small** |    9.7M    | 0.5   | 0.33   |     -    |
| **modelpack-medium**|    31M     | 0.75  | 0.67   |     -    |



## Quick Start Guide

This section includes several tutorials useful to understand how to operate ModelPack from EdgeFirst Studio. At this point the user should know how to [Record/Capture Datasets](../../datasets/tutorials.md) from either Maivin or Raivin.


### Musicbox Detector

This tutorial shows the whole ModelPack live cicle, from data collection to model deployment. At the end of this tutorial, the user will be able to go outside and record data to play with ModelPack at any scale. For more information go to [MusicBox Tutorial](tutorials/musicbox.md)

![MusicBox](./tutorials/assets/musicbox-tutorial-header.png)


### Golf Ball Detector


### Earpods Detector




ModelPack exposes two different outputs that can be combined depending on the problem. The first one is a regression output for object detection that decode bounding boxes and classes. The second output is a classification output that assign a class to each pixel. Segmentation output is aproximatelly half of the input size. 

Modelpack is a single-sensor (single-input) architecture of a Vision model tasked with detecting objects in an image via bounding boxes, segmentation masks, or both. A Vision model is a type of model that interprets images or videos to perform tasks such as object recognition, image classification, and much more. There are three types of Vision models that are supported in EdgeFirst Studio. 

1. Detection: Models that output bounding boxes and scores that provide 4-point coordinates on the image marking the locations of the object.
2. Segmentation: Models that output segmentation masks with the same shape as the input image to distinguish pixels belonging to the object or its background. 
3. Multitask: A combination of object detection and segmentation. These models outputs bounding boxes, scores, and segmentation masks.




## Tutorials