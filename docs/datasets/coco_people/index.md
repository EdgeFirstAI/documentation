# COCO People dataset

This dataset is a subset of the original COCO dataset. All annotations were filtered to retain only those corresponding to the person class, effectively removing all other object categories. The complete set of images from the original dataset is preserved — including those that no longer have any associated annotations after filtering. Images without any person annotations are treated as negative samples, helping improve model robustness by providing background-only examples during training.

## Object Detection Benchmark (100 epochs)


=== "ONNX"

    **COCO Metrics - RGB - (640x640) | ONNX**

    | Model             | mAP@0.5 | mAP@0.5..0.95 |
    |-------------------|-----------|-----------|
    | modelpack-csp19-nano-640x640-rgb       | 0.48    |   0.223  | 
    | ultralytics-yolov8n-640x640-rgb | 0.620 | 0.41 |

    !!! note
        Time information is not included in this validation because they can change dependening on the hardware quality

=== "i.MX 8M Plus"

    **COCO Metrics - RGB - (640x640) | TFLite | INT8**

    | Model             | mAP@0.5 | mAP@0.5..0.95 | Time (ms) |
    |-------------------|-----------|-----------|---------------|
    | modelpack-csp19-nano-640x640-rgb       | 0.196   | 0.073    |  10.63    | 
    | ultralytics-yolov8n-640x640-rgb       | 0.583   | 0.374    |  137.43    | 

    !!! note
        **i.MX 8M Plus** is running BSP 6.12