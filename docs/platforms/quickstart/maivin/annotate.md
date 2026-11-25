# Annotate Dataset

A detection model learns from 2D bounding boxes and/or segmentation masks on the camera frame. If you chose an auto-generated annotation source when you [restored the MCAP](restore.md), EdgeFirst Studio's [Automatic Ground Truth Generation (AGTG)](../../../studio/agtg.md) has already annotated the dataset. Proceed to ["audit the annotations"](#audit-annotations) to correct mistakes that resulted from the auto-annotation process. Otherwise follow this section from start to finish to annotate your dataset from scratch.

{% include-markdown "discrete/datasets/annotate_2d_dataset.md" %}

When every sequence is annotated and the boxes are correct, continue to the next step: [Split and Tag Dataset](split.md).

## More Information

- [Automatic Ground Truth Generation (AGTG)](../../../studio/agtg.md): how the AGTG pipeline works and what each control in the tool does.
- [AGTG Tutorial](../../../datasets/tutorials/annotations/automatic.md#2d-automatic-ground-truth-generation): fully automatic annotation upon snapshot restore, and 2D semi-automatic annotation in the gallery, with video tutorials.
- [Manual Annotations](../../../datasets/tutorials/annotations/manual.md#manual-2d-annotations): adjusting 2D boxes and segmentation masks by hand.
- [Dataset Annotations](../../../datasets/tutorials/annotations/index.md): adding, editing and removing labels.

## Next Steps

Once every sequence is annotated, the next step in the Maivin Quick Start guide is to prepare the dataset for training by [splitting and tagging the dataset](split.md).
