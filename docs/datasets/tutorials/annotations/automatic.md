# Automatic Ground Truth Generation (AGTG)

The [AGTG pipeline](../../../studio/agtg.md) describes the stages for automating the annotation process of a dataset. There are two modes of operation.

1. *Fully Automatic*: This is invoked at the time of importing the dataset as a [snapshot](../../../studio/snapshots.md#restore-snapshot) and as a background process which deploys a detection model to drive SAM2.
2. *Semi-Automatic*: This is invoked when users trigger the "AI Segment Tool" inside the dataset gallery.  Users can select portions of the dataset to auto-annotate, but SAM2 requires initial annotations from the users as prompts.

## Fully Automatic Ground Truth Generation

This annotation feature is available at the time of importing the dataset via [snapshot restoration](../../../studio/snapshots.md#restore-snapshot).  The auto-annotation process is done in the background allowing the user to focus on separate tasks.  This section will show the steps for performing this type of auto-annotation in EdgeFirst Studio.  This feature can also be deployed using the [EdgeFirst Client](../../../client/cli/index.md#restore-a-snapshot) from the command line.

A complete description of dataset snapshots and related features can be found under [Studio Snapshots](../../../studio/snapshots.md).

This feature is a two-step process: *Create Snapshot* and *Restore Snapshot*.

### Create Snapshot

Recall that [snapshots](../../../studio/snapshots.md) are frozen and compact form of datasets.  There are three ways of creating snapshots.

1. Create from Existing Dataset

    On the dataset card, open the dataset context menu and select "Create Snapshot".

    {{ figure("../../assets/annotations/automatic/create-snapshot.jpg", "Create Snapshot From Dataset") }}

    Next enter the name for the dataset snapshot.  Click on "Add Snapshot" to begin the snapshot creation.

    {{ figure("../../assets/annotations/automatic/create-snapshot-fields.jpg", "Name the Snapshot") }}

2. Upload from MCAP File

    An MCAP file is a [recording captured](../capture.md#capture-with-an-edgefirst-platform) by an [EdgeFirst Platform](../../../platforms/index.md) such as a Maivin or a Raivin.

    To create a snapshot from an MCAP file, visit the "Snapshots" page.

    {{ figure("../../assets/annotations/automatic/data-snapshots.jpg", "Snapshots Page") }}

    Either drag and drop an MCAP file into the page OR click on the "From File" button to allow selection of the MCAP file from your directories.

    {{ figure("../../assets/annotations/automatic/mcap-file-import.jpg", "MCAP Import Snapshot") }}

3. Upload from ZIP/Arrow (EdgeFirst Dataset) Files

    The ZIP/Arrow files together forms the [EdgeFirst Dataset Format](../../format/index.md).

    To create a snapshot from ZIP/Arrow files, visit the "Snapshots" page.

    {{ figure("../../assets/annotations/automatic/data-snapshots.jpg", "Snapshots Page") }}

    Either drag and drop the ZIP/Arrow files into the page OR click on the "From File" button to allow selection of the ZIP/Arrow files from your directories.

    {{ figure("../../assets/annotations/automatic/zip-arrow-files-import.jpg", "ZIP/Arrow Import Snapshot") }}

    !!! warning "Uniform Names"
        The name of corresponding ZIP and Arrow files must be same.

    !!! info "ZIP/Arrow File pairs"
        The upload must come into ZIP and Arrow file pairs.
        If there are multiple ZIP and Arrow pairs, then each pair will become a sequence.

A snapshot can be created from one of the three ways as described above: *Create from Existing Dataset*, *Upload from MCAP File*, *Upload from ZIP/Arrow File*.  The next section will show how to restore these created snapshots for auto-annotations.

{% include-markdown "discrete/datasets/restore_snapshot.md" heading-offset=2 %}

{{ figure("../../assets/annotations/automatic/coffeecup-restored-ds.jpg", "Restored Dataset") }}

Next [navigate to the gallery](../management.md#view-dataset) of the dataset by clicking on the gallery button.  The 2D annotations for both segmentation masks and bounding boxes should have been auto-generated in the background.

{{ figure("../../assets/annotations/automatic/agtg-restored-annotations.jpg", "Restored Annotations") }}

The next section will describe the *Semi-Automatic Ground Truth Generation* for additional user control during the auto-annotation process.

## 2D Automatic Ground Truth Generation

{% include-markdown "discrete/datasets/annotate_2d_dataset.md" %}

## 3D Automatic Ground Truth Generation

{% include-markdown "discrete/datasets/annotate_3d_dataset.md" %}

{% include-markdown "discrete/datasets/key_frames.md" %}

## Video Tutorials

This is a high level video tutorial shown an MCAP recording restored as a snapshot.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=720&end=1163" title="Auto Annotate Dataset" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## Next Steps

If you notice any errors on the annotations that require adjustments or any missing annotations that needs to be added, follow these tutorials that describe the [manual annotation](manual.md) features.
