# Web Workflow

In this workflow, you will explore recording a video or capturing images using a mobile device and then upload the captured data into EdgeFirst Studio for annotation and model training, validation, and deployment using the PC. This workflow requires the user to have {{ studio_link("signed up", "signup") }} and {{ studio_link("logged in", "login") }} to EdgeFirst Studio and followed the initial steps described in the [Getting Started with EdgeFirst Studio](../../index.md).

## Capture with a Phone

This guide is based on recording and capturing images of coffee cups using a phone.  However, you can choose any type of objects for your dataset and the same steps will apply.

{% include-markdown "discrete/datasets/recording_on_phone.md" heading-offset=2 %}
{% include-markdown "discrete/datasets/create_dataset_container.md" %}
{% include-markdown "discrete/datasets/uploading_video_to_studio.md" %}
{% include-markdown "discrete/datasets/uploading_images_to_studio.md" %}

Next [view the gallery of the dataset](../../datasets/tutorials/management.md#view-dataset) to confirm all the captured data has been uploaded.  You should see the imported video file and images in the gallery.  Note that videos appear as sequences with a play button overlay on the preview thumbnail.

{{ figure("/getting_started/assets/workflows/pc-dataset-gallery.jpg", "Coffee Cup Gallery") }}

Now that you have imported captured images or videos into EdgeFirst Studio you can now start annotating your data as shown in the next section below.

{% include-markdown "discrete/datasets/annotate_2d_dataset.md" %}

## Split Dataset

{% include-markdown "discrete/datasets/split_dataset.md" %}

## Tag Dataset

{% include-markdown "discrete/datasets/tag_dataset.md" %}
{% include-markdown "discrete/models/train_vision.md" %}
{% include-markdown "discrete/models/convert_vision.md" %}
{% include-markdown "discrete/models/validate_vision.md" %}
{% include-markdown "discrete/models/deploy_model.md" %}

## Next Steps

Have a target device?  Check out the [Hardware Persona Workflows](hardware.md) to run through the MLOps process on your device.
