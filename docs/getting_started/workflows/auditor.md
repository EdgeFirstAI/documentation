# Auditor Workflow

In this workflow, you will learn how to annotate your own dataset, train a model, validate it, and deploy it on the browser — all in the cloud without requiring target hardware.

First copy a dataset from the "Sample Project" as shown below.

{{ figure("../..//studio/assets/projects/sample-datasets-button.jpg", "Sample Datasets Button") }}

Inside "Sample Project", you will find a sample dataset called "Coffee Cup".  The examples shown will copy this dataset to train a model that detects coffee cups on images.

## Copy Dataset

{% include-markdown "discrete/datasets/copy_dataset.md" %}
{% include-markdown "discrete/datasets/annotate_2d_dataset.md" %}

## Tag Dataset

{% include-markdown "discrete/datasets/tag_dataset.md" %}

{% include-markdown "discrete/models/train_vision.md" %}
{% include-markdown "discrete/models/convert_vision.md" %}
{% include-markdown "discrete/models/validate_vision.md" %}

## Deploy Model

{% include-markdown "discrete/models/deploy_studio_model.md" %}

## Next Steps

Want to bring your own dataset? Check out the [Web Persona Workflow](web.md).
