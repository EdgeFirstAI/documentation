# BDD100K: A Large-scale Diverse Driving Video Database

The BDD100K dataset is a large-scale driving video dataset containing 100,000 video clips with annotations for various computer vision tasks.  It includes labels for object detection, lane marking, driveable areas, semantic segmentation, instance segmentation, tracking, and more.  BDD100K supports research in autonomous driving and real-world scene understanding.

## Object Detection Benchmark (100 epochs)

=== "ONNX"

    **COCO Metrics - RGB - (640x640) | ONNX**

    | Model                             | mAP@0.5   | mAP@0.5..0.95 |
    |-----------------------------------|-----------|---------------|
    | modelpack-csp19-medium-640x640-rgb | 0.466   | 0.259         | 
    | modelpack-csp19-large-640x640-rgb | 0.479   | 0.273         | 
    | **modelpack-csp53-nano-640x640-rgb**  | **0.525**   | **0.31**           |
    | yolov5n-det-640x64-rgb            | 0.443   | 0.241           |
    | yolov8n-det-640x640-rgb           | 0.436   | 0.25           |
    | yolo11-det-640x640-rgb           | 0.449   | 0.249           |

    !!! note "Timing Benchmark"
        Time information is not included in this validation because they can change depending on the hardware quality of the cloud servers in EdgeFirst Studio. The timing benchmarks are provided when the models are run on specific platforms such as the [i.MX 8M Plus](#imx-8m-plus).

=== "i.MX 8M Plus"

    <h2 id="imx-8m-plus" style="display: none;"></h2>

    **COCO Metrics - RGB - (640x640) | TFLite | INT8**

    | Model                             | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |-----------------------------------|---------|---------------|-----------|
    | modelpack-csp19-medium-640x640-rgb | 0.418   | 0.201         |  22.2    |
    | modelpack-csp19-large-640x640-rgb | 0.408   | 0.199         |  25.02    |
    | modelpack-csp53-nano-640x640-rgb  | 0.466   | 0.239         |  47.8    |
    | yolov5n-det-640x640-rgb           | -   | -         |  62.9    |
    | yolov8n-det-640x640-rgb           | -   | -         |  66.7    |
    | yolo11n-det-640x640-rgb           | -   | -         |  93.4    |

    !!! note "BSP Version"
        **i.MX 8M Plus** is flashed with [NXP Yocto BSP](https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software/embedded-linux-for-i-mx-applications-processors:IMXLINUX) 6.12.

## Dataset Information

- **Groups**:
    - train: 70000 images
    - val: 10000 images
    - test: 20000 images

The dataset contains a total of 100,000 images and 10 different classes.

<figure markdown="span">
![Class Distribution](../assets/bdd100k/label_count.png){ align=center }
</figure>

## Dataset Gallery

<figure markdown="span">
![BDD100K Dataset Gallery](../assets/bdd100k/gallery.png){ align=center }
</figure>

## License

[Dataset Home Page](https://bair.berkeley.edu/blog/2018/05/30/bdd/) and [Download Portal](http://bdd-data.berkeley.edu/)

## Reference

Yu, F., Chen, H., Wang, X., Xian, W., Chen, Y., Liu, F., ... & Darrell, T. (2020). Bdd100k: A diverse driving dataset for heterogeneous multitask learning. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition (pp. 2636-2645).
