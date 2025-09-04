# Playingcards Dataset

PlayingCards is an experimental object detection dataset developed at Au-Zone Technologies to evaluate embedded models in indoor scenarios. It contains 1,476 images, split into 1,327 for training and 148 for validation, covering 13 classes with various poses.

While bounding box prediction is relatively straightforward due to the uniform rectangular shape of all cards, classification presents a greater challenge. Models often overgeneralize card locations because of the consistent geometry, yet struggle to distinguish between visually similar classes such as jack, queen, and king.

## Dataset Labels

The labels on the dataset are the following:

```
ace, eight, five, four, jack, king, nine, queen, seven,
six, ten, three, two
```

and they have the following distribution across the dataset:

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
