# ModelPack Benchmarks

This section describes how ModelPack behaves across some datasets

## Imagenet

ImageNet is a large-scale, publicly available image dataset designed for visual object recognition research. Containing over 14 million images across more than 20,000 categories, it has become a cornerstone for training and evaluating deep learning models in computer vision. The ImageNet Large Scale Visual Recognition Challenge (ILSVRC), in particular, has driven significant advances in the field by serving as a standardized benchmark. Models are typically evaluated on their top-1 and top-5 classification accuracy using a fixed input resolution (commonly 224×224 RGB images). This benchmark provides a rigorous test of a model’s ability to generalize across diverse visual concepts, enabling direct comparisons of architecture performance, efficiency, and scalability. In this context, we evaluate a series of CSPDarknet-based models using standard ImageNet settings, reporting their accuracy and parameter efficiency to guide architecture selection for real-world applications.

### ImageNet Results: 

| Model             | Top-1 Acc | Top-5 Acc | Top-10 Acc | Batch Size | Parameters |
|------------------|-----------|-----------|------------|------------|------------|
| modelpack-nano   | 0.52      | 0.76      | 0.86       | 256        | 1.42M      |
| modelpack-small  | 0.62      | 0.84      | 0.89       | 256        | 2.48M      |
| modelpack-medium | 0.66      | 0.87      | 0.91       | 256        | 4.18M      |
| modelpack-large  |  -        | -         | -          | -          | -          |

**Table: CSPDarknet19 ImageNet Results - RGB - (224x224)**

---


| Model             | Top-1 Acc | Top-5 Acc | Top-10 Acc | Batch Size | Parameters |
|------------------|-----------|-----------|------------|------------|------------|
| modelpack-nano   | 0.72      | 0.91      | 0.94       | 256        | 2.70M      |
| modelpack-small  | 0.83      | 0.95      | 0.98       | 128        | 7.40M      |
| modelpack-medium | 0.91      | 0.99      | 0.99       | 128        | 22.8M      |
| modelpack-large  | -         | -         | -          | 128        | 49.7M      |

**Table: CSPDarknet53 ImageNet Results - RGB - (224x224)**
