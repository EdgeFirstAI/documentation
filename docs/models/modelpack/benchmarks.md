# ModelPack Benchmark Suite

This page presents comprehensive benchmark results for ModelPack, a versatile model collection featuring multiple backbone architectures and size variants (nano, small, medium, large). ModelPack is designed for flexibility and performance across a wide range of computer vision tasks. Here, we evaluate its performance on several key datasets, including ImageNet for classification, PlayingCards for object detection, and COCO for detection and segmentation . Each benchmark includes metrics such as accuracy, model size, and inference efficiency, helping developers and researchers choose the right configuration for their specific use case. Explore the tables below to compare performance across backbones and deployment scenarios.

=== "Playingcards"

    ## Playing Cards

    The Playing Cards dataset is a custom object detection dataset containing over 1,000 images annotated across 13 card classes (e.g., Ace to King). It focuses on detecting cards in varied orientations and real-world settings. We use this dataset to benchmark ModelPack models for lightweight, task-specific detection performance. 

    **Table: ModelPack on PlayingCards - RGB - (640x640) - ONNX - (50 epochs)**

    | Model                              | mAP@0.5 | mAP@0.5..0.95 |
    |------------------------------------|---------|---------------|
    | modelpack-csp19-small-640x640-rgb  | 0.874   | 0.687         | 
    | modelpack-csp19-medium-640x640-rgb | 0.909   | 0.683         | 
    | modelpack-csp19-large-640x640-rgb  | 0.926   | 0.731         | 
    | modelpack-csp53-nano-640x640-rgb   | 0.876   | 0.706         | 
    | modelpack-csp53-small-640x640-rgb  | 0.931   | 0.755         | 

    **Table: ModelPack on PlayingCards - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                              | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |------------------------------------|---------|---------------|-----------|
    | modelpack-csp19-small-640x640-rgb  | 0.867   | 0.642         | 15.99     |  
    | modelpack-csp19-medium-640x640-rgb | 0.901   | 0.643         | 20.60     |  
    | modelpack-csp19-large-640x640-rgb  | 0.909   | 0.658         | 24.46     |  
    | modelpack-csp53-nano-640x640-rgb   | 0.862   | 0.642         | 44.08     |  
    | modelpack-csp53-small-640x640-rgb  | 0.928   | 0.692         | 79.29     |  

    Visit the full **Playingcards** dataset [Benchmark here](../../datasets/playingcards/index.md).

=== "Coffee Cup"

    ## Object Detection and Segmentation Metrcis
    
    **Table: ModelPack on CoffeeCup - RGB - (640x640) | ONNX**

    | Model                              | mAP@0.5 | mAP@0.5..0.95 | seg-mAP@0.5 | seg-mAP@0.5..0.95 |  
    |------------------------------------|---------|---------------|-------------|-------------------|
    | modelpack-csp19-medium-640x640-rgb | 0.995   | 0.978         | 0.891       | 0.863             |

    **Table: ModelPack on CoffeeCup - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                              | mAP@0.5 | mAP@0.5..0.95 | seg-mAP@0.5 | seg-mAP@0.5..0.95 | Time (ms) |
    |------------------------------------|---------|---------------|-------------|-------------------|-----------|
    | modelpack-csp19-medium-640x640-rgb | 0.995   | 0.911         | 0.884       | 0.856             | 45.53     |  
     
    Visit the full **Coffee Cup** dataset [Benchmark here](../../datasets/coffeecup/index.md).

=== "BDD100K"

    ## BDD100K

    BDD100K is a large-scale autonomous driving dataset with 100K images annotated for tasks like object detection, lane detection, and segmentation. It features diverse weather, lighting, and geographic conditions. We benchmark ModelPack models on BDD100K to evaluate performance in real-world driving scenarios.

    **Table: ModelPack on BDD100K - RGB - (640x640) - ONNX - (100 epochs)**

    | Model                             | mAP@0.5 | mAP@0.5..0.95 |
    |-----------------------------------|---------|---------------|
    | modelpack-csp19-large-640x640-rgb | 0.423   | 0.227         | 
    | modelpack-csp53-nano-640x640-rgb  | 0.466   | 262           |


    **Table: ModelPack on BDD100K - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                             | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |-----------------------------------|---------|---------------|-----------|
    | modelpack-csp19-large-640x640-rgb | 0.375   | 0.175         |  19.28    |
    | modelpack-csp53-nano-640x640-rgb  | 0.403   | 0.194         |  45.15    |

    Visit the full **BDD100K** dataset [Benchmark here](../../datasets/bdd100k/index.md).

=== "COCO People"

    This dataset contains only annotations for person class from original dataset. However, all the images are included during training as negative samples

    **Table: ModelPack on COCO People - RGB - (640x640) - ONNX - (100 epochs)**

    | Model                            | mAP@0.5 | mAP@0.5..0.95 |
    |----------------------------------|---------|---------------|
    | modelpack-csp19-nano-640x640-rgb | 0.48    | 0.223         | 
    
    **Table: ModelPack on COCO People - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                            | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |----------------------------------|---------|---------------|-----------|
    | modelpack-csp19-nano-640x640-rgb | 0.196   | 0.073         |  10.63    | 
    
    Visit the full **COCO People** dataset [Benchmark here](../../datasets/coco_people/index.md).

=== "COCO 2017"

    !!! note
        COCO benchmark is coming soon !!!

=== "ImageNet"

    ## Imagenet

    ImageNet is a large-scale dataset with over 14 million images, widely used for training and benchmarking computer vision models. It enables standardized evaluation using top-1 and top-5 accuracy metrics. Here, we benchmark CSPDarknet-based models on ImageNet to assess their accuracy and efficiency. ([Curious about Ultralytics on Imagenet... ?](https://docs.ultralytics.com/datasets/classify/imagenet/)).

    **Table: CSPDarknet19 ImageNet Results - RGB - (224x224)**

    | Model        | Top-1 Acc | Top-5 Acc | Top-10 Acc | Batch Size | Parameters |
    |--------------|-----------|-----------|------------|------------|------------|
    | csp19-nano   | 0.52      | 0.76      | 0.86       | 256        | 1.42M      |
    | csp19-small  | 0.62      | 0.84      | 0.89       | 256        | 2.48M      |
    | csp19-medium | 0.66      | 0.87      | 0.91       | 256        | 4.18M      |
    | csp19-large  |  -        | -         | -          | -          | -          |

    ---

    **Table: CSPDarknet53 ImageNet Results - RGB - (224x224)**

    | Model        | Top-1 Acc | Top-5 Acc | Top-10 Acc | Batch Size | Parameters |
    |--------------|-----------|-----------|------------|------------|------------|
    | csp53-nano   | 0.72      | 0.91      | 0.94       | 256        | 2.70M      |
    | csp53-small  | 0.83      | 0.95      | 0.98       | 128        | 7.40M      |
    | csp53-medium | 0.91      | 0.99      | 0.99       | 128        | 22.8M      |
    | csp53-large  | -         | -         | -          | 128        | 49.7M      |

    !!! note
        All modelpack backbones are pretrained on Imagenet.  If you want to reproduce the experiments or metrics on this dataset, please contact <a href="mailto:support@edgefirst.ai">support@edgefirst.ai</a>.

!!! note "BSP Version"
    **i.MX 8M Plus** is flashed with [NXP Yocto BSP](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX) 6.12.
