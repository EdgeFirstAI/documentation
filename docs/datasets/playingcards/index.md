# Playingcards Dataset

The Playing Cards dataset is a custom object detection dataset containing over 1,000 images annotated across 13 card classes (e.g., Ace to King). It focuses on detecting cards in varied orientations and real-world settings. We use this dataset to benchmark ModelPack models for lightweight, task-specific detection performance. 


## Object Detection Benchmark (100 epochs)

**Table: COCO Metrics - RGB - (640x640)**

| Model             | mAP@0.5 | mAP@0.5..0.95 |
|-------------------|-----------|-----------|
| csp19-small       | 0.920     |   0.747    | 
| csp19-medium      | 0.946     |   0.754    | 
| csp19-large       | 0.944     |   0.769    | 
| csp53-nano        | 0.924     |   0.774    | 
| csp19-small       | 0.945     |   0.791    | 
| yolov8n           | 0.551     |   0.641    | 
