# Annotate Dataset

Now that you have a dataset in your project, you can start annotating the dataset.  This will briefly show the steps for annotating the dataset, but for an in depth tutorial on the annotation process, please see [Dataset Annotations](../../datasets/tutorials/annotations/index.md).  

To annotate a dataset, first create an annotation set on the dataset card.

{{ figure("/datasets/assets/annotations/add-annotation-set-button.jpg", "Annotation Set") }}

A new annotation set was created called "new-annotations".

{{ figure("/datasets/assets/annotations/new-annotation-set.jpg", "New Annotation Set") }}

Next, open the dataset gallery, by clicking on the gallery button ![Gallery Button](../../assets/buttons/studio-gallery-button.jpg) on the top left of the dataset card.  The dataset will contain sequences (video) ![Sequences Icon](../../assets/buttons/studio-sequence-icon.jpg) and images.  Click on any sequence card to start [annotating sequences](../../datasets/tutorials/annotations/automatic.md#semi-automatic-ground-truth-generation).

{{ figure("/datasets/assets/annotations/coffee-cup-gallery.jpg", "Coffee Cup Gallery") }}

On the top navbar, switch to the right annotation set.

{{ figure("/datasets/assets/annotations/switch-annotation-sets.jpg", "Switch Annotation Set") }}

[Start the AGTG server](../../datasets/tutorials/annotations/automatic.md#initialize-agtg-server) by clicking on the "AI Segment Tool" and follow the prompts as indicated.

{{ figure("/datasets/assets/annotations/automatic/agtg-segment-tool.jpg", "Auto Segment Mode") }}

Once the AGTG server has started, go ahead and [annotate the starting frame](../../datasets/tutorials/annotations/automatic.md#annotate-starting-frame).

{{ figure("/datasets/assets/annotations/automatic/agtg-prompts.jpg", "AGTG Initial Prompts") }}

Once the starting frame has been annotate, go ahead and [propagate the annotations](../../datasets/tutorials/annotations/automatic.md#propagate) throughout the rest of the frames.

{{ figure("/datasets/assets/annotations/automatic/propagation-process.jpg", "Propagation Process") }}

Once the propagation completes, click "Save Annotations" to save the propagated annotations.

{{ figure("/datasets/assets/annotations/automatic/propagation-completed.jpg", "Propagation Completed") }}

Repeat the steps for all the sequences in the dataset.  For the case of individual images, the same steps apply except there is no propagation step.  You can still use the AGTG feature to quickly annotate images as shown in [Add 2D annotations](../../datasets/tutorials/annotations/manual.md#add-2d-annotations).
