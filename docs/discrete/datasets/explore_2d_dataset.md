{{ figure("/studio/assets/datasets/dataset-attributes.jpg", "Dataset Card UI Breakdown") }}

This dataset has a total of 1399 images and single label "coffeecup".  It has two partitions; "train" and "val".  There is a total of 1119 images for the training group ("train") and 280 images for the validation group ("val").

Click the image preview to view the dataset gallery.  The dataset gallery will look like the following below.

{{ figure("/datasets/assets/management/sample-dataset-sequences.jpg", "Dataset Sequences") }}

{{ figure("/datasets/assets/management/sample-dataset-images.jpg", "Dataset Images") }}

This dataset will contain [both sequences (videos) and images](../../datasets/format/structure.md#3-mixed-datasets).  Clicking on the sequences will provide video playback of the sequence.  Otherwise, clicking on images will expand the image view and allow playback of all images in the dataset.

This dataset has a complete set of 2D annotations (masks and bounding boxes) of coffee cups.  Additional features are also available to the user by expanding the image previews of the dataset such as [annotation features and visualization](../../datasets/tutorials/annotations/index.md), and image information.

{{ figure("/datasets/assets/management/sample-dataset-image-preview.jpg", "Dataset Image Preview") }}

!!! tip "Fast Annotations"
    This dataset was quickly annotated using the [Automatic Ground Truth Generation (AGTG) feature of EdgeFirst Studio](../../studio/agtg.md).
