# EdgeFirst Studio Dataset Zoo

The EdgeFirst Studio Dataset Zoo offers two types of datasets:

- **EdgeFirst Datasets**: Commercially clean datasets you can license from Au-Zone Technologies
- **Third-party Datasets**: Datasets for evaluation and research only (see their licensing restrictions)

=== "Coffee Cup"

    The Coffee Cup dataset was created by Au-Zone Technologies using mobile devices at various orientations to capture image samples of coffee cups.  The dataset contains a single label "coffeecup" with image bounding box and instance segmentation annotations.  This is a simple dataset typically used for user onboarding to explore the features of dataset annotations, model training and validation in EdgeFirst Studio.  A Vision model can be trained in EdgeFirst Studio using this dataset in under 1 hour.  The trained models can also be deployed in the PC, NXP's i.MX 8M Plus EVK, or a field-ready [EdgeFirst Platform](../platforms/index.md) such as a Maivin or a Raivin to detect coffee cups in the frame.

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](coffeecup/index.md){ .md-button }
    </div>

=== "Playing Cards"

    The Playing Cards dataset was created by Au-Zone Technologies using various recording devices such as the Maivin 1 under different illumination conditions, orientations, and backgrounds to capture image samples of Playing Cards.  The dataset contains 13 labels of the numbers from a typical deck of cards.  However, suits are currently not annotated.  This dataset only has image bounding box annotations.  This dataset is typically used for testing Object Detection algorithms at the edge.  All the objects in this dataset have the same rectangular shapes, but only the color and the texture is different among the classes, and the camera target distance is relatively small.  An Object Detection model can be trained in EdgeFirst Studio using this dataset in under 1 hour.  The trained models can also be deployed in the PC, NXP's i.MX 8M Plus EVK, or a field-ready [EdgeFirst Platform](../platforms/index.md) such as a Maivin or a Raivin.

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](playingcards/index.md){ .md-button }
    </div>

=== "BDD100K"

    The BDD100K dataset was created by [UC Berkeley](https://bair.berkeley.edu/blog/2018/05/30/bdd/) which is a large-scale driving video dataset seeking to improve autonomous driving and real-world scene understanding solutions.  The dataset consists of 100,000 videos; each video about 40 seconds long at 720p and 30 FPS recorded by cell-phones.  The dataset contains 10 labels focusing on traffic entities and includes labels for object detection, lane marking, driveable areas, semantic and instance segmentation, tracking, and more.  This is a large dataset and training Object Detection models in EdgeFirst Studio using this dataset is a costly operation which can take up to 3 days.  Once trained, the models can also be deployed in the PC, NXP's i.MX 8M Plus EVK, or a field-ready [EdgeFirst Platform](../platforms/index.md) such as a Maivin or a Raivin.

    !!! note "Third Party Dataset"
        BDD100K is a third-party dataset that's provided for evaluation and research purposes only.  Please refer to their respective licensing restrictions.

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](bdd100k/index.md){ .md-button }
    </div>

=== "COCO People"

    The COCO People dataset is a subset of the original [COCO dataset](https://cocodataset.org/#home) created by Microsoft which was filtered to only include the annotations corresponding to the person class.  This dataset contains a single label "person" with image bounding box and instance segmentation annotations.  The images were primarily sourced from Flickr which provide excellent samples that represent real-world scenarios. This is a large dataset and training Object Detection models in EdgeFirst Studio using this dataset is a costly operation which can take up to 3 days.  Once trained, the models can also be deployed in the PC, NXP's i.MX 8M Plus EVK, or a field-ready [EdgeFirst Platform](../platforms/index.md) such as a Maivin or a Raivin.

    !!! note "Third Party Dataset"
        COCO People is a third-party dataset that's provided for evaluation and research purposes only.  Please refer to their respective licensing restrictions.

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](coco_people/index.md){ .md-button }
    </div>

=== "COCO"

    The [COCO dataset](https://cocodataset.org/#home) was created by Microsoft to advance state-of-the-art object recognition and scene understanding.  The dataset contains 80 classes chosen to be easily recognizable by a 4 year old.  This dataset contains image bounding box and instance segmentation annotations.  The images were primarily sourced from Flickr which provide excellent samples that represent real-world scenarios. This is a large dataset and training Object Detection models in EdgeFirst Studio using this dataset is a costly operation which can take up to 3 days.  Once trained, the models can also be deployed in the PC, NXP's i.MX 8M Plus EVK, or a field-ready [EdgeFirst Platform](../platforms/index.md) such as a Maivin or a Raivin.

    !!! note "Third Party Dataset"
        COCO is a third-party dataset that's provided for evaluation and research purposes only.  Please refer to their respective licensing restrictions.

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](coco/index.md){ .md-button }
    </div>

=== "Raivin Ultra Short"

    The Raivin Ultra Short dataset was created by Au-Zone Technologies using a [Raivin platform](../platforms/index.md) with either the base Radar module or a LiDAR module attached to the device to aid in the 3D annotation process.  The dataset contains a single label "person" with 2D (image-based bounding box and instance segmentation) and 3D (real-world bounding boxes) annotations useful for training Object Detection or Fusion models for scene-understanding and spatial-perception tasks.  The dataset samples contains both indoor and rigourous outdoor environments such as construction sites.  The dataset is set to an ultra short range where the field of the objects spans no more than 10 meters away from the Raivin sensor. A Fusion model can be trained in EdgeFirst Studio using this dataset in under 1 hour.  The trained models can be deployed in a field-ready [Raivin Platform](../platforms/index.md) for people awareness tasks.

    <div style="max-width: fit-content; margin-left: auto; margin-right: auto;" class="wizard-actions" markdown>
    [Read More](raivin_ultra_short/index.md){ .md-button }
    </div>

!!! tip "Additional Datasets"
    📬 If you need support for additional datasets,
    please do not hesitate and [email our support team](mailto:support@edgefirst.ai) — we’re here to help!

The [EdgeFirst Dataset Format](format/index.md) is purposely designed to efficiently store multiple annotation types and sensor types.

## Format Quick Reference

| Component | Contents | Purpose |
|-----------|----------|---------|
| **ZIP file** | Images, point clouds, sensor data | Raw captured data organized by sequence/frame |
| **Arrow file** | Annotations, labels, metadata | Efficient columnar storage for ML training |

This format is used throughout EdgeFirst Studio:

- **[Snapshots](../studio/snapshots.md)**: Portable ZIP+Arrow pairs for download and sharing
- **[MCAP uploads](../platforms/publishing.md)**: Converted to this format when restored as datasets
- **[Training](../models/training/vision.md)**: Arrow annotations feed directly into model training

Learn more in the [Format Documentation](format/index.md).

---

There are 2D and 3D types of annotations that correlate with each other. For example, a 2D annotation is a set of pixel-based bounding boxes and segmentation masks whereas a 3D annotation is a set of 3D bounding boxes in meters.  However, a single object can be described by all three linked annotation types: a 2D bounding box, a 2D mask, and a 3D bounding box.  There could be multiple sensors involved in creating the dataset such as the camera, Radar and/or LiDAR, etc.  The readings from these sensors is rarely modified and needs to be distinguished in the dataset.  Thus, the EdgeFirst Dataset is known for its file pairs (typically Zip and Arrow) for storing the sensor data and annotations separately.  The [EdgeFirst Dataset File Structure](format/structure.md) comes in various forms depending if the data is a sequence or not.

## Related Articles

1. [Capturing Data](tutorials/capture.md)
2. [Import Existing Datasets](tutorials/import.md)
3. Dataset Annotations
    - [Automatic Annotation Process](tutorials/annotations/automatic.md)
    - [Manual Annotation Process](tutorials/annotations/manual.md)
4. [Dataset Management](tutorials/management.md)
