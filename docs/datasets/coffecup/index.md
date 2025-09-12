# CoffeCup Dataset

Coffe Cup dataset is part of our [Data Capture Tutorial](../../datasets/tutorials/capture.md). The dataset has different types of coffe cups on different poses and surfaces with annotations for Object Detection and Semantic Segmentation.


## Object Detection Benchmark (50 epochs)


=== "ONNX"

    ## Object Detection and Segmentation Metrcis

    **COCO Metrics - RGB - (640x640) | ONNX**

    | Model             | mAP@0.5 | mAP@0.5..0.95 | seg-mAP@0.5 | seg-mAP@0.5..0.95 |  
    |-------------------|-----------|-----------|-------------|--------------|
    | modelpack-csp19-medium-640x640-rgb   | 0.995    |   0.978  |  0.899 | 0.863 |
    | ultralytics-yolov8n-640x640-rgb   | 0.993    |  0.991  | 0.993 | 0.981|

    !!! note
        Time information is not included in this validation because they can change dependening on the hardware quality

=== "i.MX 8M Plus"

    **COCO Metrics - RGB - (640x640) | TFLite | INT8**

    | Model             | mAP@0.5 | mAP@0.5..0.95 | seg-mAP@0.5 | seg-mAP@0.5..0.95 | Time (ms) |
    |-------------------|-----------|-----------|---------------|----------|-----------------|
    | modelpack-csp19-medium-640x640-rgb    | 0.995    | 0.911   | 0.884 | 0.856 | 45.53    |  
    | ultralytics-yolov8n-640x640-rgb    | 0.995    | 0.891  | 0.995 | 0.969 | 170.8    |  


    !!! note
        **i.MX 8M Plus** is running BSP 6.12


## Dataset Information

- **Groups**:
    - train: 916 images
    - val: 229 images

The dataset contains a total of 1399 images and a single class.

![Class Distribution](./assets/label_count.png){align=center}

## Dataset Gallery

![Dataset Gallery](./assets/gallery.png){align=center}


## License

