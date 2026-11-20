# 3D Annotations

The 3D annotations are a set of 3D bounding boxes in meters that represent the physical dimensions of the object in the frame.  Proceed to this link for more information regarding the [format of the 3D bounding boxes](../../datasets/format/box_format.md#box3d).

{{ figure("../assets/3d_bounding_box_plus_lidar.jpg", "LiDAR PCDs") }}

## Annotations on the Same Object

A 2D box, a segmentation mask, and a 3D box can all belong to the same object.  See [Objects and Annotation Cases](cases.md) for how objects are organised, how to join annotations that ended up on separate objects, and how to resolve common cases.

## Automatic Ground Truth Generation

{% include-markdown "discrete/datasets/annotate_3d_dataset.md" %}

{% include-markdown "discrete/datasets/key_frames.md" %}
