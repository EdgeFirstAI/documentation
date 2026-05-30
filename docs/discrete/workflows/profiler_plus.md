## Copy Dataset
{% include-markdown "discrete/datasets/copy_dataset.md" %}

## Tag Dataset
{% include-markdown "discrete/datasets/tag_dataset.md" %}
{% include-markdown "discrete/models/train_vision.md" %}
{% include-markdown "discrete/models/validate_vision.md" %}

## Compare Results to the Model Zoo

After validation, compare your results with the [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models) to see how close your model is to the published baselines.

Focus on:

- **Task match**: Use the same task type (detection, segmentation, classification) as your training run.
- **Input modality**: Compare vision-only models against vision-only baselines, and fusion models against fusion baselines.
- **Metric alignment**: Match the primary metric (for example, mAP or F1) to ensure an apples-to-apples comparison.
- **Latency vs accuracy**: Look at accuracy and throughput together to understand the practical edge tradeoff.

## Deploy Model on EdgeFirst Studio
{% include-markdown "discrete/models/deploy_studio_model.md" %}
