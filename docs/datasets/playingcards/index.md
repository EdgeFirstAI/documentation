# Playingcards Dataset

PlayingCards is an experimental object detection dataset developed at Au-Zone Technologies to evaluate embedded models in indoor scenarios. 


## Dataset Information

- **Groups**:
    - train: 1327 Images
    - val: 148 images


It contains 1,476 images in total and 13 classes


![Class Distribution](./assets/label-count.png){align=center}


## Object Detection Benchmark (50 epochs)

**Table: COCO Metrics - RGB - (640x640)**

| Model             | mAP@0.5 | mAP@0.5..0.95 |
|-------------------|-----------|-----------|
| csp19-small       | 0.920     |   0.747    | 
| csp19-medium      | 0.946     |   0.754    | 
| csp19-large       | 0.944     |   0.769    | 
| csp53-nano        | 0.924     |   0.774    | 
| csp53-small       | 0.945     |   0.791    | 
| yolov8n           | 0.551     |   0.641    | 


## Image Gallery

![Gallery View from EdgeFirst Studio](./assets/gallery.png){align=center}


## License
