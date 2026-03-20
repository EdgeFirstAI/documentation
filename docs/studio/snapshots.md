# Snapshots Dashboard

Snapshots are portable, frozen copies of datasets in the [EdgeFirst Dataset Format](../datasets/format/index.md). Each snapshot consists of a **ZIP + Arrow file pair**:

- **ZIP file**: Contains sensor data (images, point clouds, etc.)
- **Arrow file**: Contains annotations (labels, bounding boxes, masks, metadata)

This format makes snapshots easy to download, share, archive, and re-import into any EdgeFirst Studio project.

<figure markdown="span">
![Data Snapshots](assets/snapshots/data-snapshots.png){ align=center }
<figcaption>Data Snapshots</figcaption>
</figure>

The snapshots menu shows the list of snapshots with its name and status.

<figure markdown="span">
![Snapshot List](assets/snapshots/snapshot-list.png){ align=center }
<figcaption>Snapshot List</figcaption>
</figure>

## Create Snapshot

The tutorial for creating snapshots can be found under the [Dataset Annotations](../datasets/tutorials/annotations/automatic.md#create-snapshot) section.  This will create a Zip/Arrow file pair also known as an [EdgeFirst Dataset](../datasets/format/index.md) for each sequence in a dataset and stored in the cloud storage.  This snapshot can be later restored (into another dataset) or can be downloaded to a local folder on a PC.

The stages for creating a snapshot are shown below.

<figure markdown="span">
![Create Snapshot Stages](../datasets/assets/annotations/automatic/snapshot-creation-process.png){ align=center }
<figcaption>Create Snapshot Stages</figcaption>
</figure>

A snapshot can be created by the following ways:

1. Create from Existing Dataset.
2. Upload from MCAP File.
3. Upload from Zip/Arrow File

### Create from Existing Dataset

1. From the dataset card, open the context menu and select "Create Snapshot".
2. Select the dataset and annotation set to create a snapshot from and give it a description.
3. This will trigger the creation of a snapshot.
4. The status of the snapshot generation will be shown in the dataset card.
5. When completed, the snapshot will appear in the snapshots dashboard.

### Upload from MCAP File

1. Go to the snapshots dashboard.
2. Click on the "FROM FILE" button or drag and drop an MCAP file on the dashboard.

### Upload from Zip/Arrow File

This format is the [EdgeFirst Dataset Format](../datasets/format/index.md) where the [Zip file](../datasets/format/sensors.md) contains sensor reading and measurements and the [Arrow file](../datasets/format/schema.md#) contains dataset annotations.

1. Go to the snapshots dashboard.
2. Click on the "FROM FILE" button and then select the Zip and Arrow file pairs to import or drag and drop as a folder containing Zip and Arrow file pairs onto the dashboard.
3. Once the files are selected, this will start the import sequence progress shown below.

### Pipeline

When creating a snapshot a pipeline with the following stages are deployed.

1. Server Initialization: Initialize the backend server for handling the processes.
2. Downloading Files from Cloud Storage: Fetches the dataset images from the S3 bucket.
3. Exporting Files from Database: Fetches the dataset annotations from the Studio database.
4. Zipping Files for Upload: Formulation of the [EdgeFirst Dataset Format](../datasets/format/index.md) and placing the fetched dataset files as a single Zip file.
5. Uploading Snapshot to Cloud Storage: Uploading the dataset into S3 bucket.

## Restore Snapshot

This action will take an MCAP or Zip/Arrow files and create a dataset in EdgeFirst Studio.  The backend pipelines for auto depth map generation, object detection, and Automated Ground Truth Generation can also be selected at this time while restoring.

The tutorial for restoring snapshots can be found under the [Dataset Annotations](../datasets/tutorials/annotations/automatic.md#restore-snapshot) section.

The stages for restoring a snapshot are shown below.

<figure markdown="span">
![Restore Snapshot Stages](../datasets/assets/annotations/automatic/snapshot-restore-process.jpg){ align=center }
<figcaption>Restore Snapshot Stages</figcaption>
</figure>

1. Click on the snapshot context menu (three dots).
2. Select "Restore".

<figure markdown="span">
![Snapshot Options](assets/snapshots/options.png){ align=center }
<figcaption>Snapshot Options</figcaption>
</figure>

3. This will open the restore dialog for specifying the options.

<figure markdown="span">
![Restore Options](assets/snapshots/restore-dialog.png){ align=center }
<figcaption>Restore Options</figcaption>
</figure>

4. Select "Project" where the dataset will be created.
5. Enter the dataset name and description. If the dataset name is not provided a dataset, a dataset with the snapshot name will be created.
6. Check "Use MCAP Selected Topics" if selected topics are to be imported (for example ignoring Radar and only importing Segmentation).
7. Select "Use MCAP Frame Rate" to select a custom frame rate.
8. Select "Depth Generation" to use AI Model based depth map generation.
9. Select "AI Ground Truth Generation" to enable auto generation of 2D boxes, 3D boxes, and segmentation masks.
10. Click "RESTORE SNAPSHOT".
11. The dataset dashboard will have a new dataset with progress indication.
12. The progress for different stages will be at different rates.

### Pipeline

When restoring a snapshot a pipeline with the following stages are deployed.

1. Download Snapshot from Cloud Storage: Fetches the dataset from the S3 server.
2. Converting MCAP to Dataset: This is only present when the method of [creating a snapshot](#upload-from-mcap-file) is from an MCAP file.
3. Automatic Annotations Generation: Runs AGTG to auto annotate the dataset with COCO labels.
4. Prepare Data for Upload: Data preparation processes.
5. Importing Images and Annotations to Database: Uploading the images and annotations to the Studio database.
6. Uploading Files to Cloud Storage: Uploading the annotated dataset back into S3 bucket.

## Download Snapshot

1. Click on the snapshot context menu (three dots).
2. Select "Download".

This downloads the snapshot as a **ZIP + Arrow file pair** to your local machine:

```
my_snapshot.zip       # Sensor data (images, point clouds)
my_snapshot.arrow     # Annotations (labels, boxes, masks)
```

These files follow the [EdgeFirst Dataset Format](../datasets/format/index.md) and can be:

- Re-imported into any EdgeFirst Studio project as a new snapshot
- Used for offline analysis with Python/Polars
- Shared with collaborators or archived for backup
- Processed by custom ML pipelines outside of Studio

See [Dataset Organization](../datasets/format/structure.md) for details on the internal structure of these files.

## Delete Snapshot

1. Click on the snapshot context menu (three dots).
2. Select "Remove".

<figure markdown="span">
![Snapshot Options](assets/snapshots/options.png){ align=center }
<figcaption>Snapshot Options</figcaption>
</figure>

## Next Steps

Now that you are familiar with the Snapshots Dashboard, proceed to the next section for a proper introduction to the auto-annotation process in EdgeFirst Studio known as [Automatic Ground Truth Generation (AGTG)](agtg.md).
