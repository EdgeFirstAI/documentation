# 3D MLOps

Teach your model to see the world in three dimensions.  With 3D MLOps in EdgeFirst Studio, you can annotate objects in real-world coordinates, train models that learn where those objects are, and deploy them on a [Raivin platform](../platforms/quickstart/raivin/index.md).  It is the foundation for applications such as object awareness and perception, where knowing that something is there is not enough and you also need to know where.

{{ figure("../datasets/assets/annotations/sample-studio-annotations.jpg", "EdgeFirst Studio Annotations") }}

The example above shows 3D annotations (right) next to the camera frame (left).  The 3D bounding boxes describes the physical dimensions of each object in meters, while the frame shows the picture of the same objects surrounded by 2D bounding boxes and segmentation masks.

!!! info "3D Point Clouds"
    3D bounding boxes are created from LiDAR or Radar point clouds.  LiDAR points clouds are more dense allowing more accurate 3D bounding boxes.  Radar point clouds are more sparse providing only general clusters of the object, unlike LiDAR which forms the overall shape of the object.

    Au-Zone Technologies provides Raivin platforms with either the Radar or LiDAR module for enhanced 3D perception. 

Once a model is deployed, the Raivin can show you what it sees live.  The [Web UI](../platforms/quickstart/raivin/webui.md) displays the 2D inference (segmentation masks and bounding boxes) alongside a 3D polar grid that highlights the Radar point clusters marking where objects are in world coordinates.

{{ figure("../models/assets/deployment/occupancy-sample-1.png", "Model Inference on the Raivin") }}

## Where to Start

New to 3D MLOPs?  Start with the [3D viewers](viewers.md) to see how point clouds and 3D boxes appear in Studio.

Then follow the workflow from data to deployment:

1. [Annotate](annotations/index.md) your data with 3D bounding boxes.
2. [Train](training.md) a 3D perception (Fusion) model.
3. [Validate](validation.md) the model's performance.
4. [Deploy](deployment.md) it to the Raivin.

As you annotate, [objects and annotation cases](annotations/cases.md) explains how to work with multiple annotations on the same object, and the [keyboard hotkeys](annotations/hotkeys.md) will speed up your editing.
