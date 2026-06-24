# Annotate Dataset

Now that you have a dataset in your project, you can start annotating the dataset.  This will briefly show the steps for annotating the dataset, but for an in depth tutorial on the annotation process, please see [Dataset Annotations](../../datasets/tutorials/annotations/index.md).  

To annotate a dataset, first create an annotation set on the dataset card.

{{ figure("/datasets/assets/annotations/add-annotation-set-button.jpg", "Annotation Set") }}

Provide the name of the new annotation set and its description

{{ figure("/datasets/assets/annotations/new-annotation-set-options.jpg", "Annotation Set Specifiers") }}

A new annotation set is now created called "new-annotations".

{{ figure("/datasets/assets/annotations/new-annotation-set.jpg", "New Annotation Set") }}

Next, open the dataset gallery, by clicking on the image preview of the dataset card.

{{ figure("/datasets/assets/management/sample-dataset-sequences.jpg", "Coffee Cup Gallery") }}

The dataset will contain sequences (video) and images.  Click on any sequence card to start [annotating sequences](../../datasets/tutorials/annotations/automatic.md#semi-automatic-ground-truth-generation).

On the top navbar, switch to the annotation set you created.

{{ figure("/datasets/assets/annotations/switch-annotation-sets.jpg", "Switch Annotation Set") }}

[Start the AGTG server](../../datasets/tutorials/annotations/automatic.md#initialize-agtg-server) by clicking on the "AI Segment Tool" and follow the prompts as indicated.

{{ figure("/datasets/assets/annotations/automatic/agtg-segment-tool.jpg", "Auto Segment Mode") }}

Go ahead and launch the AGTG server.  Please allow ~5mins for the server to initialize. 

!!! warning "AGTG Server Did Not Start"

    If the AGTG server has not started after 5 minutes, refresh your browser and click the **AI Segment Tool** button again.

{{ figure("/datasets/assets/annotations/automatic/launch-agtg-server.jpg", "AGTG Server") }}

Once the AGTG server has started, go ahead and [annotate the starting frame](../../datasets/tutorials/annotations/automatic.md#annotate-starting-frame).  Once the starting frame has been annotated, go ahead and [propagate the annotations](../../datasets/tutorials/annotations/automatic.md#propagate) throughout the rest of the frames.

{{ video("/getting_started/assets/workflows/AGTG-tutorial.mp4", "AGTG Preview") }}

{{ figure("/datasets/assets/annotations/automatic/agtg-prompts.jpg", "AGTG Initial Prompts") }}

Once the propagation completes, click "Save Annotations" to save the propagated annotations.

{{ figure("/datasets/assets/annotations/automatic/propagation-completed.jpg", "Propagation Completed") }}

!!! note "Audit Annotations"

    Run the video playback to browse through the generated annotations and verify that the generated annotations are correct.

    If an annotation was missed, you can quickly [add the annotation](../../datasets/tutorials/annotations/manual.md#add-2d-annotations) using the same process and click "Save AIGT Annotations" as shown.

    {{ img("/datasets/assets/annotations/automatic/add-missed-annotation.jpg", "Add Missed Annotations") }}

    For objects that were improperly annotated, you can [remove annotations](../../datasets/tutorials/annotations/manual.md#delete-2d-annotations).  For annotations that require minor adjustments, EdgeFirst Studio has the features for [adjusting annotations](../../datasets/tutorials/annotations/manual.md#adjust-2d-annotations).  Please click on the links as provided for further instructions on each of these features.

Repeat the steps for all the sequences in the dataset.  You can go back to the dataset sequences by pressing the back button on the top left corner.

{{ figure("/datasets/assets/annotations/automatic/back-to-gallery.jpg", "AGTG Server") }}

For the case of individual images, the same steps apply except there is no propagation step.  You can still use the AGTG feature to quickly annotate images as shown in [Add 2D annotations](../../datasets/tutorials/annotations/manual.md#add-2d-annotations).
