

## Auto Annotations via Gallery

Once the propagation completes, click on "Save Pending Annotations" to save the annotations.  A completed propagation will show the 2D annotations with masks and 2D bounding boxes for each object across the video frames.

<figure markdown="span">
![Save Pending Annotations](../assets/agtg-save-pending-annotations.jpg){ align=center }
<figcaption>Save Pending Annotations</figcaption>
</figure>

!!! warning

    For cases where the object exits and then re-enters the frame, the object might not be tracked properly.  Repeat the steps as necessary to annotate the objects that were missed.

If you notice any errors on the annotations or missing annotations, follow the tutorial for [auditing 2D annotations](#audit-2d-annotations).  Furthermore, there is also a tutorial for [auditing 3D annotations](#audit-3d-annotations). 

## Auto Annotations via Snapshot

This tutorial describes the steps for auto-annotating an [uploaded MCAP recording](management.md#upload-mcaps) by restoring a dataset snapshot.  This feature can be deployed using [EdgeFirst-Client](../../perception/studio.md#restore-snapshots) via the command line.  However, this tutorial will show the steps in EdgeFirst Studio. 

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=720&end=1163" title="Auto Annotate Dataset" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

To run auto-annotations on the recorded data, click *Restore* on the uploaded snapshot.

<figure markdown="span">
![Restore Snapshot](../assets/restore-snapshot.jpg){ align=center }
<figcaption>Restore Snapshot</figcaption>
</figure>

The following fields are for you to specify.  Adjust the following fields for your own use case.

<figure markdown="span">
![Restore Snapshot Fields](../assets/restore-snapshot-fields.jpg){ align=center }
<figcaption>Restore Snapshot Fields</figcaption>
</figure>

Once specifed, click *RESTORE SNAPSHOT* to start the auto-annotation process.  This
will start the auto-annotation process.

<figure markdown="span">
![Restore Process](../assets/snapshot-started.jpg){ align=center }
<figcaption>Restore Process</figcaption>
</figure>

The progress will be shown on the dataset specified in the project.

<figure markdown="span">
![Restore Progress](../assets/restore-snapshot-progress.jpg){ align=center }
<figcaption>Restore Progress</figcaption>
</figure>

Once completed, the dataset will now contain annotations that resulted from the auto-annotation process.

<figure markdown="span">
![Restored Dataset](../assets/restored-dataset.jpg){ align=center }
<figcaption>Restored Dataset</figcaption>
</figure>

Next [navigate to the gallery](management.md#viewing-datasets) of the dataset by clicking on the gallery button as indicated in red to visualize the annotations.  The figure below shows a side-by-side display of the annotations from frames 1-3.  The annotations for "people" are shown as both segmentation masks and bounding boxes. 

**Frame 1** | **Frame 2** | **Frame 3** 
:------------------:|:------------------:|:------------------:
![Annotation 1](../assets/annotation-1.jpg) | ![Annotation 2](../assets/annotation-2.jpg) | ![Annotation 3](../assets/annotation-3.jpg)

If you notice any errors on the annotations or missing annotations, follow the tutorial for [auditing 2D annotations](#audit-2d-annotations).  Furthermore, there is also a tutorial for [auditing 3D annotations](#audit-3d-annotations). 
