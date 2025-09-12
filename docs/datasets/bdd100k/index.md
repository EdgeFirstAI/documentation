# BDD100K: A Large-scale Diverse Driving Video Database


The BDD100K dataset is a large-scale driving video dataset containing 100,000 video clips with annotations for various computer vision tasks. It includes labels for object detection, lane marking, drivable areas, semantic segmentation, instance segmentation, tracking, and more. BDD100K supports research in autonomous driving and real-world scene understanding.

## Object Detection Benchmark (100 epochs)


=== "ONNX"

    **COCO Metrics - RGB - (640x640) | ONNX**

    | Model             | mAP@0.5 | mAP@0.5..0.95 |
    |-------------------|-----------|-----------|
    | modelpack-csp19-large-640x640-rgb       | 0.423     |   0.227    | 
    | modelpack-csp53-nano-640x640-rgb      | 0.466     |   262    |
    | ultralytics-yolov8n-640x640-rgb   | 0.325 | 0.173 |

    !!! note
        Time information is not included in this validation because they can change dependening on the hardware quality

=== "i.MX 8M Plus"

    **COCO Metrics - RGB - (640x640) | TFLite | INT8**

    | Model             | mAP@0.5 | mAP@0.5..0.95 | Time (ms)|
    |-------------------|-----------|-----------|---------|
    | modelpack-csp19-large-640x640-rgb       | 0.375     |   0.175    |  19.38 |
    | modelpack-csp53-nano-640x640-rgb      | 0.403     |   0.193    |  45.07|
    | ultralytics-yolov8n-640x640-rgb   | 0.272 | 0.138 | 137.39 |


    !!! note
        **i.MX 8M Plus** is running BSP 6.12


## Dataset Information

- **Groups**:
    - train: 70000 images
    - val: 10000 images
    - test: 20000 images

The dataset contains a total of 100000 images and 10 different classes

![Class Distribution](./assets/label_count.png){align=center}


## Dataset Gallery


![Dataset Gallery](./assets/gallery.png){align=center}

## License

[Dataset Home Page](https://bair.berkeley.edu/blog/2018/05/30/bdd/) and [Download Portal](http://bdd-data.berkeley.edu/)

## Reference

Yu, F., Chen, H., Wang, X., Xian, W., Chen, Y., Liu, F., ... & Darrell, T. (2020). Bdd100k: A diverse driving dataset for heterogeneous multitask learning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition (pp. 2636-2645).