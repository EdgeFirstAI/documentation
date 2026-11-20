The 3D annotations are formulated from either Radar or LiDAR PCDs whichever is available upon [import from a Raivin Platform](../../platforms/quickstart/raivin/upload.md). You can auto-annotate a dataset with 3D annotations from the [dataset gallery in EdgeFirst Studio](../../studio/datasets/gallery.md).

This annotation process allows you to annotate any object with 2D and 3D annotations. 2D annotations exists on the frame as 2D bounding boxes and segmentation masks in pixel coordinates. 3D annotations are 3D bounding boxes in meters that describe the physical dimension of the annotated object and visualized in the 3D panel.

This feature is a five-step process: intialize AGTG Server, Annotate Starting Frame, Propagate, Save Annotations, Audit Annotations.

{{ video("/getting_started/assets/workflows/agtg-3d-tutorial.mp4", "AGTG Preview") }}

From the dataset gallery, click on any sequence to annotate.

{{ figure("/3D/assets/click_3d_sequence.jpg", "Pick a Sequence") }}

Add labels to your dataset if it doesn't already have labels.

{{ figure("/3D/assets/add_3d_labels.jpg", "Add 3D Labels") }}

Enable the LiDAR or Radar Point Clouds.

{{ figure("/3D/assets/pcd_visibility.jpg", "Enable PCD Visibility") }}

## Initialize AGTG Server

Launch the AGTG server by clicking on the "AI Segment Tool".

{{ figure("/3D/assets/launch_agtg_server.jpg", "Launch AGTG Server") }}

## Annotate Starting Frame

Annotate the starting frame by drawing a box around the object (click and drag). This will point SAM to the object in the frame that you would like to track. If a second object also needs to be annotated, click on the "+" button as shown to add a new object. Do this for each new object in your frame.

{{ figure("/3D/assets/annotate_starting_frame.jpg", "Annotate Frame") }}

## Propagate

Click propagate to start tracking the annotated object and creates 2D and 3D annotations
throughout the frames.

{{ figure("/3D/assets/propagate_starting_frame.jpg", "Propagate") }}

{{ figure("/3D/assets/agtg_progress.jpg", "AGTG Progress") }}

!!! note "500 Frame Tracks"

    To avoid exceeding SAM's memory capacity, we limit the tracks to 500 frames.
    If your dataset contains more than 500 frames, repeat the steps shown for your next track of frames.

## Save Annotations

Once propagation completes, click "Save AIGT Annotations". This will save the generated annotations.

{{ figure("/3D/assets/save_aigt_annotations.jpg", "Save Annotations") }}

## Audit Annotations

The generated annotations may not have been perfect. Remember, the AGTG feature merely aids the annotation process and reduces the time it takes to annotate a dataset, but it currently does not entirely replace the human effort needed to obtain a correctly annotated dataset.

Review the generated annotations by moving back to the starting frame in the video playback and identify cases where:

1. An object was not annotated:

    a. The frame did not have 2D annotations (bounding boxes and masks). *You can fix this error by following the steps for [adding 2D annotations](../../3D/annotations/2d_annotations.md#add-2d-annotations).*

    b. The object did not have a 3D bounding box. *You can fix this error by following the steps to [add a 3D bounding box via the Clustering Mode](../../3D/annotations/3d_annotations.md#cluster-3d-annotation).*

2. An annotation was wrong:

    a. The annotation should not exist. *You can [delete annotations](../../3D/annotations/3d_annotations.md#delete-3d-annotation) of objects that should not exist.*

    b. The annotation needs to be adjusted. *It may be faster to [delete the annotation](../../3D/annotations/3d_annotations.md#delete-3d-annotation) and re-[add the annotation](../../3D/annotations/2d_annotations.md#add-2d-annotations) if SAM needs to be tried again. However, Studio provides tools to adjust [2D](../../3D/annotations/2d_annotations.md#adjust-2d-annotations) and [3D](../../3D/annotations/3d_annotations.md) annotations.*

!!! info "Limitation: 3D bounding box sometimes do not generate during propagation"

    We are facing a limitation to the AGTG tooling where a 3D bounding box was not generated during propagation. The 3D bounding boxes are based on the LiDAR PCDs that intersect the mask on the frame. If the PCDs do not intersect or minimally intersects the mask, then there would be no PCD clusters that is synchronized with the object in the frame to create a 3D bounding box.

    Shown below is an example:

    {{ img("/3D/assets/project_lidar_pcd.jpg", "Project PCDs the the Frame") }}

    However, we provide a ["Clustering Mode"](../../3D/annotations/3d_annotations.md#cluster-3d-annotation) which requires the user to select a set of clustered PCDs to automatically draw a 3D bounding box for the object.

For the keyboard shortcuts available while annotating, see [3D Keyboard Hotkeys](../../3D/annotations/hotkeys.md).
