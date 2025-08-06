# Restore Snapshot

The snapshot restoration process involves several dataset transformations such as the frame rate specification, depth map generation, and auto-annotations. More information can be found in [Studio](../../studio/snapshots.md).

!!! info "COCO Annotations"
    The labels supported during the auto-annotation process for the *Fully Automatic Ground Truth Generation* are the [COCO labels](../../datasets/coco/index.md#coco-labels) listed.

The created snapshots can be found under "Data Snapshots".

<figure markdown="span">
![Data Snapshots](../../datasets/assets/annotations/automatic/data-snapshots.jpg){ align=center }
<figcaption>Data Snapshots</figcaption>
</figure>

To restore the snapshot, click on the snapshot context menu and select "Restore".

<figure markdown="span">
![Restore Snapshots](../../datasets/assets/annotations/automatic/restore-snapshot.jpg){ align=center }
<figcaption>Restore Snapshots</figcaption>
</figure>

Restoring a snapshot will create a new dataset entirely with annotations.  Specify the project to contain this new dataset and specify the name and the description of the dataset.  Furthermore, toggle the "AI Ground Truth Generation" to auto annotate the dataset samples.  The rest of the settings can be kept in their defaults for this tutorial.  Click "Restore" to start the restoration process. 

<figure markdown="span">
![Restore Snapshots Fields](../../datasets/assets/annotations/automatic/restore-snapshot-fields.jpg){ align=center }
<figcaption>Restore Snapshots Fields</figcaption>
</figure>

The snapshot restore process can be found under the project datasets.

<figure markdown="span">
![Restore Snapshots Progress](../../datasets/assets/annotations/automatic/snapshot-restore-process.jpg){ align=center }
<figcaption>Restore Snapshots Progress</figcaption>
</figure>

Once completed, the dataset will now contain annotations that resulted from the auto-annotation process.
