# Restore Snapshot

The snapshot restoration process involves several dataset transformations such as the frame rate specification, depth map generation, and auto-annotations. More information can be found in [Studio](../../studio/snapshots.md).

The created snapshots can be found in the "Snapshots" page.

{{ figure("/datasets/assets/annotations/automatic/data-snapshots.jpg", "Snapshots Page") }}

To restore the snapshot, click on the snapshot context menu and select "Restore".

{{ figure("/datasets/assets/annotations/automatic/restore-snapshot.jpg", "Restore Snapshots") }}

Restoring a snapshot will create a new dataset entirely with annotations.  Specify the project to contain this new dataset and specify the name and the description of the dataset.  Furthermore, select the method for annotating the dataset. We recommend the second option which is by deploying a custom YOLOx model to annotate the dataset with [COCO classes](../../datasets/coco/index.md#coco-labels). If you need to auto-annotate with your own custom classes, you will need a model trained in Studio with your custom classes.

{{ figure("/datasets/assets/annotations/automatic/restore-snapshot-fields.jpg", "Restore Snapshots Fields") }}

Click "Start App" to the start the annotation process. The progress is reported in the ["Tasks" page](../../studio/tasks.md).

{{ figure("/datasets/assets/annotations/automatic/snapshot-restore-process.jpg", "Restore Snapshots Progress") }}

Once completed, the new dataset will now contain annotations that resulted from the auto-annotation process. You can also click on the dataset link shown above to navigate directly to the created dataset.
