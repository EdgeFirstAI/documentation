# Automatic Ground Truth Generation (AGTG)

AGTG allows datasets to have annotations populated on a dataset with minimal human interaction. There are two modes of operation.

1. Background Operation: This is invoked at the time of importing the dataset.
2. Semi-automatic: Users can select portions of dataset sequenced and manually trigger AI assisted annotations.

## Fully Automatic Ground Truth Generation

This functionality is available at the time of restoring a snapshot. To invoke the restore feature, import/create a snapshot and then enable AGTG while restoring the snapshot. Please refer to [Restoring a snapshot](snapshots.md) for more information.

## Semi-Automatic Ground Truth Generation

This process is used to generate 2D Bounding boxes, 2D segmentation masks, and 3D bounding boxes using AI assisted pipelines in EdgeFirst Studio.

### Creating AI Assisted Annotations

1. Open a dataset and go to its gallery.
2. Click on a sequence or image.
5. Select *AI Segment Tool*.

<figure markdown="span">
![AI Segment Tool](assets/agtg/agtg-tool.png){ align=center }
<figcaption>AI Segment Tool</figcaption>
</figure>

6. Start the Automated Ground Truth Server. Note that you will be billed while the server is running.
7. When the server is ready, start drawing bounding boxes or use clicks to create masks.

<figure markdown="span">
![AGTG Sidebar](assets/agtgsidebar.png){ align=center }
<figcaption>AGTG Sidebar</figcaption>
</figure>

<figure markdown="span">
![Segmented Annotation](assets/segmented-annotation.png){ align=center }
<figcaption>Segmented Annotation</figcaption>
</figure>

8. For a sequence, you can select choose how many frames from current frame to propagate and click *PROPAGATE*.
9. You can also select *Reverse Propagate* to apply propagation backwards from current frame.
10. This will start a counter and propagate the object from the starting frame to the ending frame.
11. If satisfied, click on the *SAVE ANNOTATIONS* to store the annotations to the dataset.
12. If the dataset has LIDAR, then 3D bounding boxes are also created for the same object.
13. Click *CLEAR ANNOTATIONS* to clear every unsaved annotation. Use this to restart AI-Assisted Annotation.
14. Repeat for other objects as necessary.
