# Ultralytics Benchmarks

This page provides a summary of the benchmarks gathered for Ultralytics across various datasets.

=== "Playingcards"

    ## Playing Cards

    The Playing Cards dataset is a custom object detection dataset containing over 1,000 images annotated across 13 card classes (e.g., Ace to King).  It focuses on detecting cards in varied orientations and real-world settings.  We use this dataset to benchmark Ultralytics models for lightweight, task-specific detection performance. 

    **Table: Ultralytics on Playing Cards - RGB - (640x640) - ONNX - (50 epochs)**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 |
    |---------------------------------|---------|---------------|
    | ultralytics-yolov8n-640x640-rgb | 0.829   | 0.700         |

    **Table: Ultralytics on PlayingCards - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |---------------------------------|---------|---------------|-----------|
    | ultralytics-yolov8n-640x640-rgb | 0.809   | 0.671         | 138.13    | 
    
    Visit the full **Playingcards** dataset [Benchmark here](../../datasets/playingcards/index.md).

=== "Coffee Cup"

    ## Object Detection and Segmentation Metrics

    **Table: Ultralytics on CoffeeCup - RGB - (640x640) | ONNX**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 | seg-mAP@0.5 | seg-mAP@0.5..0.95 |  
    |---------------------------------|---------|---------------|-------------|-------------------|
    | ultralytics-yolov8n-640x640-rgb | 0.993   |  0.991        | 0.993       | 0.982             |

    
    **Table: Ultralytics on CoffeeCup - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 | seg-mAP@0.5   | seg-mAP@0.5..0.95 | Time (ms) |
    |---------------------------------|---------|---------------|---------------|-------------------|-----------|
    | ultralytics-yolov8n-640x640-rgb | 0.995   | 0.891         | 0.995         | 0.970             | 170.89    |  

    ## Segmentation Metrics

    Visit the full **Coffee Cup** dataset [Benchmark here](../../datasets/coffeecup/index.md).

=== "BDD100K"

    ## BDD100K

    BDD100K is a large-scale autonomous driving dataset with 100K images annotated for tasks like object detection, lane detection, and segmentation. It features diverse weather, lighting, and geographic conditions. We benchmark Ultralytics models on BDD100K to evaluate performance in real-world driving scenarios.

    **Table: Ultralytics on BDD100K - RGB - (640x640) - ONNX - (100 epochs)**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 |
    |---------------------------------|---------|---------------|
    | ultralytics-yolov8n-640x640-rgb | 0.325   | 0.173         |

    **Table: Ultralytics on BDD100K - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |---------------------------------|---------|---------------|-----------|
    | ultralytics-yolov8n-640x640-rgb | 0.272   | 0.138         | 137.66    |

    Visit the full **BDD100K** dataset [Benchmark here](../../datasets/bdd100k/index.md).

=== "COCO People"

    This dataset contains only annotations for person class from original dataset.  However, all the images are included during training as negative samples

    **Table: Ultralytics on COCO People - RGB - (640x640) - ONNX - (100 epochs)**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 |
    |---------------------------------|---------|---------------|
    | ultralytics-yolov8n-640x640-rgb | 0.620   | 0.410         |

    **Table: Ultralytics on COCO People - RGB - (640x640) - TFLite - i.MX 8M Plus**

    | Model                           | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |---------------------------------|---------|---------------|-----------|
    | ultralytics-yolov8n-640x640-rgb | 0.583   | 0.374         |  137.43   | 

    Visit the full **COCO People** dataset [Benchmark here](../../datasets/coco_people/index.md).

=== "COCO 2017"

    !!! note
        COCO benchmark is coming soon !!!

=== "ImageNet"

    !!! note
        To see Imagenet metrics visit Ultralytics: [Ultralytics ImageNet](https://docs.ultralytics.com/datasets/classify/imagenet/).

!!! note "BSP Version"
    **i.MX 8M Plus** is flashed with [NXP Yocto BSP](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX) 6.12.
