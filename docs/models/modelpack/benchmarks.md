# Welcome to the ModelPack Benchmark Suite

This page presents comprehensive benchmark results for ModelPack, a versatile model collection featuring multiple backbone architectures and size variants (nano, small, medium, large). ModelPack is designed for flexibility and performance across a wide range of computer vision tasks. Here, we evaluate its performance on several key datasets, including ImageNet for classification, PlayingCards for object detection, and COCO for detection and segmentation . Each benchmark includes metrics such as accuracy, model size, and inference efficiency, helping developers and researchers choose the right configuration for their specific use case. Explore the tables below to compare performance across backbones and deployment scenarios.

## Imagenet

ImageNet is a large-scale dataset with over 14 million images, widely used for training and benchmarking computer vision models. It enables standardized evaluation using top-1 and top-5 accuracy metrics. Here, we benchmark CSPDarknet-based models on ImageNet to assess their accuracy and efficiency. ([Curious about Ultralytics on Imagenet... ?](https://docs.ultralytics.com/datasets/classify/imagenet/)).

**Table: CSPDarknet19 ImageNet Results - RGB - (224x224)**

| Model             | Top-1 Acc | Top-5 Acc | Top-10 Acc | Batch Size | Parameters |
|------------------|-----------|-----------|------------|------------|------------|
| csp19-nano   | 0.52      | 0.76      | 0.86       | 256        | 1.42M      |
| csp19-small  | 0.62      | 0.84      | 0.89       | 256        | 2.48M      |
| csp19-medium | 0.66      | 0.87      | 0.91       | 256        | 4.18M      |
| csp19-large  |  -        | -         | -          | -          | -          |

---

**Table: CSPDarknet53 ImageNet Results - RGB - (224x224)**


| Model             | Top-1 Acc | Top-5 Acc | Top-10 Acc | Batch Size | Parameters |
|------------------|-----------|-----------|------------|------------|------------|
| csp53-nano   | 0.72      | 0.91      | 0.94       | 256        | 2.70M      |
| csp53-small  | 0.83      | 0.95      | 0.98       | 128        | 7.40M      |
| csp53-medium | 0.91      | 0.99      | 0.99       | 128        | 22.8M      |
| csp53-large  | -         | -         | -          | 128        | 49.7M      |



## COCO 

COCO (Common Objects in Context) is a large-scale dataset with over 330K images and 80 object categories, widely used for object detection, segmentation, and keypoint estimation. It emphasizes understanding objects in complex, real-world scenes. Here, we benchmark ModelPack variants on COCO to evaluate detection accuracy and model scalability.

**Table: CSPDarknet53 ImageNet Results - RGB - (224x224)**


| Model             | mAP@0.5 | mAP@0.5..0.95 |
|-------------------|-----------|-----------|
| csp19-large       | 0.153      |   0.085 | 

Visit the full COCO dataset [Benchmark here](../../datasets/coco/index.md/#object-detection-benchmark-100-epochs)

## BDD100K

BDD100K is a large-scale autonomous driving dataset with 100K images annotated for tasks like object detection, lane detection, and segmentation. It features diverse weather, lighting, and geographic conditions. We benchmark ModelPack models on BDD100K to evaluate performance in real-world driving scenarios.



## Playing Cards

The Playing Cards dataset is a custom object detection dataset containing over 1,000 images annotated across 13 card classes (e.g., Ace to King). It focuses on detecting cards in varied orientations and real-world settings. We use this dataset to benchmark ModelPack models for lightweight, task-specific detection performance. 

**Table: ModelPack on PlayingCards - RGB - (640x640)**

| Model             | mAP@0.5 | mAP@0.5..0.95 |
|-------------------|-----------|-----------|
| csp19-small       | 0.920     |   0.747    | 
| csp19-medium      | 0.946     |   0.754    | 
| csp19-large       | 0.944     |   0.769    | 
| csp53-nano        | 0.924     |   0.774    | 
| csp19-small       | 0.945     |   0.791    | 

Visit the full COCO dataset [Benchmark here](../../datasets/playingcards/index.md/#object-detection-benchmark-100-epochs)