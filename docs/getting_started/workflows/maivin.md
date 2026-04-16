# Maivin Workflow

In this workflow, you will explore recording MCAPs from the Maivin which will be used to create and annotate datasets with 2D bounding boxes and segmentation masks.  Once the dataset has been annotated, you will start training and validating your Vision model using the dataset captured.  Finally, you will deploy the model back to the Maivin for inference.

{% include-markdown "discrete/workflows/maivin.md" %}

To deploy Vision models on a Maivin, please see these [instructions](../../platforms/quickstart/maivin/deploy.md).

{{ figure("../../models/assets/deployment/segmentation-sample-1.jpg", "Segmentation Sample") }}
