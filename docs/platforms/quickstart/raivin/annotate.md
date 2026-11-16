# Annotate Dataset

A fusion model learns from 2D and 3D bounding boxes, so every object you want the model to detect needs both in every frame.  If you chose an auto-generated annotation source when you [restored the MCAP](restore.md), EdgeFirst Studio's [Automatic Ground Truth Generation (AGTG)](../../../studio/agtg.md) has already annotated the dataset.  In this step you check those annotations, add any that are missing, and fix any that are wrong.

## Check the Annotations

From the dataset card, open the dataset gallery and click on the sequence.  Make sure the Radar or LiDAR point clouds and the 3D bounding boxes are toggled visible.

{{ figure("../../../datasets/assets/annotations/manual/visible-3d-annotations.jpg", "Visible 3D Annotations") }}

Step through the frames and check that:

- Every object has a 2D box on the image and a 3D box around its points.
- Each object keeps the same label from frame to frame.
- No boxes are drawn around background or empty space.

If the dataset has no annotations, because it was restored without an annotation source, or if objects are missing, add them with the AGTG tool as shown below.  If the boxes are there but in the wrong place or the wrong size, go to [Fix Annotations](#fix-annotations).

## Add Missing Annotations

The AGTG tool tracks the objects you mark in one frame through the rest of the sequence, and creates their 2D boxes, segmentation masks and 3D boxes from the point clouds.

1. Inside the dataset gallery, click on the "AI Segment Tool".

    {{ figure("../../../datasets/assets/annotations/automatic/agtg-segment-tool.jpg", "AI Segment Tool") }}

2. If no AGTG server is running, click on "Launch AGTG Server".  The server takes about 5 minutes to start.  If it hasn't started after 5 minutes, refresh the page and click on the "AI Segment Tool" again.

    {{ figure("../../../datasets/assets/annotations/manual/confirm-agtg-server-launch.jpg", "Launch AGTG Server") }}

3. In the first frame that shows the objects, draw a box around the first object.  For each additional object, click "+" to add a new object, then draw its box.  Each object needs its own entry so the tracker can give it a unique ID.

    {{ figure("../../../datasets/assets/annotations/automatic/agtg-prompts.jpg", "AGTG Prompts") }}

4. Set the "End Frame" and click on "Propagate".  The annotations are added frame by frame as the objects are tracked.

    {{ figure("../../../datasets/assets/annotations/automatic/propagation-process.jpg", "Propagation") }}

    !!! Bug "Long Tracks"
        Keep each propagation under 500 frames.  The tool becomes unreliable on tracks of about 1500 frames or more.

5. When propagation reaches the end frame, click on "Save AIGT Annotations".

    {{ figure("../../../datasets/assets/annotations/automatic/propagation-completed.jpg", "Save Annotations") }}

6. Repeat these steps for each sequence in the dataset.

!!! warning "Shut Down the AGTG Server"
    The AGTG server uses credits while it runs.  When you have finished annotating, click on "Shutdown AGTG Server".  The server also shuts down after 15 minutes of inactivity.

For more detail on each option, see the [AGTG tutorial](../../../datasets/tutorials/annotations/automatic.md#semi-automatic-ground-truth-generation).

## Fix Annotations

To move, resize or delete a 2D or 3D box, or to change its label, follow the [Manual Annotations](../../../datasets/tutorials/annotations/manual.md) tutorial.

When every sequence is annotated and the boxes are correct, continue to the next step: [Split and Tag Dataset](split.md).

## More Information

- [Automatic Ground Truth Generation (AGTG)](../../../studio/agtg.md): how the AGTG pipeline works and what each control in the tool does.
- [AGTG Tutorial](../../../datasets/tutorials/annotations/automatic.md): fully automatic annotation during restore, and semi-automatic annotation in the gallery, with video tutorials.
- [Manual Annotations](../../../datasets/tutorials/annotations/manual.md): adjusting 2D and 3D boxes by hand.
- [3D Annotations](../../../3D/annotation.md): what the 3D boxes represent and how they are built from Radar or LiDAR point clouds.
- [Dataset Annotations](../../../datasets/tutorials/annotations/index.md): adding, editing and removing labels.

## Next Steps

Once every sequence is annotated, the next step in the Raivin Quick Start guide is to prepare the dataset for training by [splitting and tagging the dataset](split.md).
