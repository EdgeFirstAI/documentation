# Annotate Dataset

A fusion model learns from 2D and 3D bounding boxes, so every object you want the model to detect needs both in every frame.  If you chose an auto-generated annotation source when you [restored the MCAP](restore.md), EdgeFirst Studio's [Automatic Ground Truth Generation (AGTG)](../../../studio/agtg.md) has already annotated the dataset. Proceed to ["audit the annotations"](#audit-annotations) to correct mistakes that resulted from the auto-annotation process. Otherwise follow this section from start to finish to annotate your dataset from scratch.

{% include-markdown "discrete/datasets/annotate_3d_dataset.md" %}

When every sequence is annotated and the boxes are correct, continue to the next step: [Split and Tag Dataset](split.md).

## More Information

- [Automatic Ground Truth Generation (AGTG)](../../../studio/agtg.md): how the AGTG pipeline works and what each control in the tool does.
- [AGTG Tutorial](../../../datasets/tutorials/annotations/automatic.md#3d-automatic-ground-truth-generation): fully automatic annotation upon snapshot restore, and 2D/3D semi-automatic annotation in the gallery, with video tutorials.
- [Manual Annotations](../../../datasets/tutorials/annotations/manual.md): adjusting 2D and 3D boxes by hand.
- [3D Annotations](../../../3D/annotations/index.md): what the 3D boxes represent and how they are built from Radar or LiDAR point clouds.
- [Dataset Annotations](../../../datasets/tutorials/annotations/index.md): adding, editing and removing labels.

## Next Steps

Once every sequence is annotated, the next step in the Raivin Quick Start guide is to prepare the dataset for training by [splitting and tagging the dataset](split.md).
