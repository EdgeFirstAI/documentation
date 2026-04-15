# Capture with a Phone

The examples below will show recording of a five second video and image captures of coffee cups using a phone for training a Vision model that detects coffee cups. However, you can choose any type of objects in your dataset.

{% include-markdown "discrete/datasets/recording_on_phone.md" heading-offset=2 %}
{% include-markdown "discrete/datasets/create_dataset_container.md" heading-offset=0 %}
{% include-markdown "discrete/datasets/uploading_video_to_studio.md" heading-offset=0 %}
{% include-markdown "discrete/datasets/uploading_images_to_studio.md" heading-offset=0 %}

Next [view the gallery of the dataset](../../datasets/tutorials/management.md#view-dataset) to confirm all the captured data has been uploaded.  You should see the imported video file and images in the gallery.  Note that videos appear as sequences with a play button overlay on the preview thumbnail.

{{ figure("/getting_started/assets/workflows/pc-dataset-gallery.jpg", "Coffee Cup Gallery") }}

Once all the captured data has been uploaded to the dataset container, you will now assign groups to the data to split the data into training and validation sets.  Follow the [tutorial for creating groups](../../datasets/tutorials/management.md#split-dataset) with an 80% partition to training and 20% partition to validation.  The final outcome for the groups should look as follows.

{{ figure("/getting_started/assets/workflows/dataset-groups.jpg", "Dataset Groups") }}

Now that you have imported captured images or videos into EdgeFirst Studio and have split the captured data into training and validation partitions, you can now start annotating your data as shown in the next section below.

{% include-markdown "discrete/datasets/annotate_2d_dataset.md" heading-offset=0 %}
{% include-markdown "discrete/datasets/audit_2d_dataset.md" heading-offset=0 %}
{% include-markdown "discrete/datasets/split_dataset.md" heading-offset=0 %}
{% include-markdown "discrete/models/train_vision.md" heading-offset=0 %}
{% include-markdown "discrete/models/validate_vision.md" heading-offset=0 %}
{% include-markdown "discrete/models/deploy_model.md" heading-offset=0 %}
