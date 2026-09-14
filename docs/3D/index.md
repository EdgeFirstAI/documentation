# 3D MLOps

EdgeFirst Studio offers 3D Machine Learning Operations using a [Raivin platform](../platforms/quickstart/raivin/index.md) that support dataset annotations using world coordinates and model training to detect the position of objects for practical applications such as object awareness or perception.

The following is a sample 3D annotation (right) in EdgeFirst Studio represented as 3D bounding boxes around the objects of interest.  The 2D image (left) are shown beside with the 2D annotations represented as segmentation masks and 2D bounding boxes covering the objects of interest in the image.

!!! infor "3D Point Clouds"
    3D bounding boxes are created from LiDAR or Radar point clouds.  LiDAR points clouds are more dense allowing more accurate 3D bounding boxes.  Radar point clouds are more sparse providing only general clusters of the object, unlike LiDAR which forms the overall shape of the object.

    Au-Zone Technologies provides Raivin platforms with either the Radar or LiDAR module for enhanced 3D perception. 

{{ figure("../datasets/assets/annotations/sample-studio-annotations.jpg", "EdgeFirst Studio Annotations") }}

The Raivin platform can visualize the model inference using the [Web UI](../platforms/quickstart/raivin/webui.md) service which provide the 2D inference (segmentation masks and bounding boxes) and the 3D inference using a polar grid highlighting the clusters of Radar points indicating the position of the objects in world coordinates.

{{ figure("../models/assets/deployment/occupancy-sample-1.png", "Model Inference on the Raivin") }}

In this section, you will explore the 3D MLOps in EdgeFirst Studio.  Start by learning more about the [3D viewers](viewers.md) in EdgeFirst Studio.

Next explore the 3D workflows from [3D annotations](annotation.md) to [training 3D perception (Fusion) models](training.md), [validation of Fusion models](validation.md), and [model deployment in the Raivin](deployment.md).
