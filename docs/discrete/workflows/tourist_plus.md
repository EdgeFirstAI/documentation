{% include-markdown "discrete/user/login.md" heading-offset=0 %}

## Browse Public Datasets

Once logged in, navigate to the **Sample Project** from the Home Page and click on the datasets.

{{ figure("/studio/assets/projects/sample-datasets-button.jpg", "Sample Project Datasets") }}

You will find [sample datasets](../../studio/datasets/index.md) which contains annotations of objects representing common household items from Coffee Cups to Playing Cards. These datasets are ready to be used for training models to detect these objects.

Click on any dataset card to view the dataset details, browse frames, and inspect annotations.  No copying is required to explore a public dataset.

{{ figure("/studio/assets/datasets/public-datasets.jpg", "Public Datasets") }}

## Browse Public Experiments

EdgeFirst Studio organizes model training and validation into [**experiments**](../../studio/models.md). Each experiment groups related training and validation sessions together so you can compare results, track improvements, and reproduce runs.

From the Home Page, navigate to the **Sample Project** and click **Model Experiments** to browse the available experiments.

{{ figure("/studio/assets/projects/sample-experiments-button.jpg", "Sample Project Model Experiments") }}

Inside an experiment you will find:

- **Training sessions** — each session records the model architecture, dataset used, training parameters, loss curves, and the resulting model artifacts (ONNX, TFLite, etc.)
- **Validation sessions** — each session measures the accuracy of a trained model against a dataset, producing precision-recall curves, mAP scores, and per-class metrics

{{ figure("/studio/assets/projects/sample-experiments.jpg", "Sample Experiments — training and validation sessions") }}

Exploring the sample experiments is a good way to understand what a completed MLOps run looks like before you start training your own models.

## Browse Public Models

Navigate to the **Models** section from any project to browse available models and their associated training and validation sessions.

Next deploy any model in EdgeFirst Studio by following this [guide](../../getting_started/running_pretrained_model.md).
