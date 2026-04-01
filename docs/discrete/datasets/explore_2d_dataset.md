{{ figure("/studio/assets/datasets/dataset-attributes.jpg", "Dataset Card UI Breakdown") }}

In this dataset, you can see that it has a total of 1399 images and single label "coffeecup".  This dataset also has two partitions; one for training and another for validation.  There is a total of 915 images for the training group and 229 images for the validation group.  Finally, the dataset has a single annotation set which shows that 1385 images have annotations and there is a total of 3020 annotations (3020 distinct objects in the dataset).

Click on the ![Dataset Gallery button](../../assets/buttons/studio-gallery-button.jpg) button on top of the dataset card to navigate to the dataset gallery.  The dataset gallery will look like the following below.

{{ figure("/datasets/assets/management/sample-dataset-image.jpg", "Sequences and Images") }}

This dataset will contain both [sequences](../../datasets/format/structure.md#1-sequence-based-datasets) (videos) ![Sequences](../../assets/buttons/studio-sequence-icon.jpg) and images.  Clicking on the sequences will provide video playback.  Otherwise, clicking on images will expand the image view.

This dataset will have a complete set of 2D annotations (masks and bounding boxes) of coffee cups.  This dataset was quickly annotated using the [Automatic Ground Truth Generatation (AGTG) feature in EdgeFirst Studio](../../studio/agtg.md).
