# Annotate Dataset

Now that you have imported videos or images into EdgeFirst Studio, let's take a look at how to annotate the dataset using the [Automatic Ground Truth Generation (AGTG)](../../../studio/agtg.md) features in EdgeFirst Studio.

1. On the [dataset gallery](../../../studio/datasets/gallery.md), click on any sequence to annotate.

    {{ figure("../../../datasets/assets/import/imported_videos.png", "Imported Videos") }}

2. Add the list of labels you plan to annotate for your dataset. In this example, the labels will be classified as "screw,washer,nuts,misc".

    {{ figure("../../../datasets/assets/annotations/automatic/add_labels.jpg", "Add Labels") }}

3. Once the labels have been added, start the "AI Segment Tool" and click on "Launch AGTG Server" as shown.

    {{ figure("../../../datasets/assets/annotations/automatic/launch_agtg_server_phytec.jpg", "Start AGTG Server") }}

    Allow ~5 mins. for the AGTG server to start. If more than 5 mins. has exceeded, please refresh the page and try again.

    {{ figure("../../../datasets/assets/annotations/automatic/agtg_initializing.jpg", "AGTG Initialization") }}

4. Start by adding bounding box prompts to each object in the frame as shown. Once the prompts have been added, click on propagate to start the annotations for the forward frames.

    {{ figure("../../../datasets/assets/annotations/automatic/agtg_prompts_phytec.jpg", "AGTG Prompts") }}

    You should see the annotations propagate throughout the frames.

    {{ figure("../../../datasets/assets/annotations/automatic/agtg_propagation_phytec.jpg", "AGTG Propagation") }}

5. Once the propagation completes, click on "Save AIGT Annotations" at the top.

    {{ figure("../../../datasets/assets/annotations/automatic/save_aigt_annotations_phytec.jpg", "Save AGTG Annotations") }}

6. If you find that all the objects appear in the last frame, you can annotate the last frame instead and select "Reverse Propagation" to propagate backwards.

    {{ figure("../../../datasets/assets/annotations/automatic/reverse_propagation_phytec.jpg", "Reverse Propagation") }}

7. Once you have annotated the selected sequence, click "Back" to go back to the list of sequences and select a new sequence to annotate. Then proceed with the same steps above to annotate the dataset.

    {{ figure("../../../datasets/assets/annotations/automatic/back_to_gallery_phytec.jpg", "Back to Gallery") }}

!!! note "Annotation Tutorial"
    For an in-depth tutorial on annotating datasets, please see our [Dataset Tutorials](../../../datasets/tutorials/annotations/automatic.md#semi-automatic-ground-truth-generation).

## Split Dataset

Now that you have annotated your dataset, let's split the dataset into train and validation groups which will be needed for model training.

{% include-markdown "discrete/datasets/split_dataset.md" %}

## Tag Dataset

Let's give a your dataset a tag to finalize the changes to your dataset and start using it for training.

{% include-markdown "discrete/datasets/tag_dataset.md" %}

## Next Steps

Now that you have annotated your dataset, let's look at how you can [train a detection model](train.md) using this dataset.
