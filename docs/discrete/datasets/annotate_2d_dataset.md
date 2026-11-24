Now that you have a dataset in your project, you can follow these steps to annotate your dataset from scratch. This annotation feature is available inside the [dataset gallery](../../studio/datasets/gallery.md); where the user has direct control over the annotation process with the ability to annotate any object with custom classes.  This feature will preload all frames of a *video* sequence in the dataset into [SAM2](https://ai.meta.com/research/sam2/) to generate segmentation masks and 2D bounding boxes for identified objects throughout the frames.

A complete description of this feature along with the functionalities of each buttons shown in this tutorial can be found under [Studio](../../studio/agtg.md#semi-automatic-ground-truth-generation).

This feature is a five-step process: *initialize AGTG server*, *annotate starting frame*, *propagate*, *save annotations*, *audit annotations*.

{{ video("/getting_started/assets/workflows/agtg-2d-tutorial.mp4", "AGTG Preview") }}

To annotate a dataset, first create an annotation set on the dataset card if it doesn't exist.

{{ figure("/datasets/assets/annotations/add-annotation-set-button.jpg", "Annotation Set") }}

Provide the name of the new annotation set and its description

{{ figure("/datasets/assets/annotations/new-annotation-set-options.jpg", "Annotation Set Specifiers") }}

A new annotation set is now created called "new-annotations".

{{ figure("/datasets/assets/annotations/new-annotation-set.jpg", "New Annotation Set") }}

Next, open the dataset gallery, by clicking on the image preview of the dataset card. Then click on any sequence to annotate.

{{ figure("/datasets/assets/annotations/automatic/click_2d_sequence.jpg", "Pick a Sequence") }}

Add labels to your dataset if it doesn't already have labels.

{{ figure("/datasets/assets/annotations/automatic/add_2d_labels.jpg", "Add 2D Labels") }}

On the top navbar, ensure the annotation set you have created is selected.

{{ figure("/datasets/assets/annotations/switch-annotation-sets.jpg", "Switch Annotation Set") }}

## Initialize AGTG Server

[Start the AGTG server](../../datasets/tutorials/annotations/automatic.md#initialize-agtg-server) by clicking on the "AI Segment Tool" and follow the prompts as indicated.

{{ figure("/datasets/assets/annotations/automatic/agtg-segment-tool.jpg", "Auto Segment Mode") }}

Go ahead and launch the AGTG server.  Please allow ~5mins for the server to initialize.

!!! warning "AGTG Server did not start"

    If the AGTG server has not started after 5 minutes, refresh your browser and click the **AI Segment Tool** button again.

{{ figure("/datasets/assets/annotations/manual/confirm-agtg-server-launch.jpg", "AGTG Server") }}

## Annotate Starting Frame

Once the AGTG server has started, go ahead and annotate the starting frame.

!!! warning "Active AGTG Server"
    This server is costing credits to run.  An inactivity of 15 minutes will auto-terminate this server.  Otherwise, once you have completed the annotations, please ensure to terminate the AGTG server by clicking !["Stop Task Button"](../../assets/buttons/studio_trash_button.jpg) to avoid spending more of your credits.

Each object must be annotated independently so the tracker can assign a unique ID. Start by drawing a bounding box for the first object by clicking and dragging.  For multiple objects in the frame, click "+" to add a new object as shown below.  The process for each object should be: *Add a new object* -> *Draw object prompt*.

By default, the prompts provided to SAM2 are bounding boxes (mouse click and drag) which should cover the object to be annotated in the frame.  However, points can also be provided (mouse clicks) by clicking areas that are part of the object.

{{ figure("/datasets/assets/annotations/automatic/agtg-prompts.jpg", "AGTG Initial Prompts") }}

## Propagate

Once the starting frame has been annotated, specify the "End Frame" which marks the frame where SAM2 stops propagating. By default this is the end of the sequence (last frame) if your sequence is less than 500 frames.  Otherwise the end frame is at the 500th frame.

!!! note "500 Frame Tracks"

    To avoid exceeding SAM's memory capacity, we limit the tracks to 500 frames.
    If your dataset contains more than 500 frames, repeat the steps shown for your next track of frames.

Go ahead and click "Propagate" to annotate the specified frames.

As the frames propagate, you should see the frames being auto-annotated.  To stop the propagation process click on "Stop Propagation".

{{ figure("/datasets/assets/annotations/automatic/propagation-process.jpg", "Propagation Process") }}

## Save Annotations

Once the propagation completes as it reached the end frame, click on "Save AIGT Annotations" to save the generated annotations.

{{ figure("/datasets/assets/annotations/automatic/propagation-completed.jpg", "Propagation Completed") }}

## Audit Annotations

Run the video playback to browse through the generated annotations and verify that the generated annotations are correct.

* If an annotation was missed, you can [add the annotation](../../datasets/tutorials/annotations/manual.md#add-2d-annotations) using the same process and click "Save AIGT Annotations" as shown.

    {{ figure("/datasets/assets/annotations/automatic/add-missed-annotation.jpg", "Add Missed Annotations") }}

* For objects that were improperly annotated, you can [remove annotations](../../datasets/tutorials/annotations/manual.md#delete-2d-annotations).  

* For annotations that require minor adjustments, EdgeFirst Studio has the features for [adjusting annotations](../../datasets/tutorials/annotations/manual.md#adjust-2d-annotations).  Please click on the links as provided for further instructions to these features.

Repeat the steps for all the sequences in the dataset.  You can go back to the dataset sequences by pressing the back button on the top left corner.

{{ figure("/datasets/assets/annotations/automatic/back-to-gallery.jpg", "Back to Dataset Gallery") }}

For the case of individual images, the same steps apply except there is no propagation step.  You can still use the AGTG feature to quickly annotate images as shown in [Add 2D annotations](../../datasets/tutorials/annotations/manual.md#add-2d-annotations).
