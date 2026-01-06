# Automatic Ground Truth Generation (AGTG)

The [AGTG pipeline](../../../studio/agtg.md) describes the stages for automating the annotation process of a dataset. There are two modes of operation.

1. *Fully Automatic*: This is invoked at the time of importing the dataset as a [snapshot](../../../studio/snapshots.md) and as a background process which deploys a detection model to drive SAM-2.
2. *Semi-Automatic*: This is invoked when users trigger the AI assisted annotations in the dataset gallery.  Users can select portions of the dataset to auto-annotate, but SAM-2 requires initial annotations from the users as prompts.

## Fully Automatic Ground Truth Generation

This annotation feature is available at the time of importing the dataset via [snapshot restoration](../../../studio/snapshots.md#restore-snapshot).  The auto-annotation process is done in the background allowing the user to focus on separate tasks.  This section will show the steps for performing this type of auto-annotation in EdgeFirst Studio.  However, this feature can also be deployed using the [EdgeFirst Client](../../../perception/studio.md#restore-snapshots) in the command line.

A complete description of this feature along with the buttons associated in this tutorial can be found under [Studio](../../../studio/snapshots.md).

This feature is a two-step process: *Create Snapshot* and *Restore Snapshot*.

### Create Snapshot

Recall that [snapshots](../../../studio/snapshots.md) are frozen and compact form of datasets.  There are three ways of creating snapshots.

1. Create from Existing Dataset

    On the dataset card, open the dataset context menu and select "Create Snapshot".

    <figure markdown="span">
    ![Create Snapshot From Dataset](../../assets/annotations/automatic/create-snapshot.jpg){ align=center }
    <figcaption>Create Snapshot From Dataset</figcaption>
    </figure>

    Next enter the name for the dataset snapshot.  Click on "Add Snapshot" to begin the snapshot creation.

    <figure markdown="span">
    ![Name the Snapshot](../../assets/annotations/automatic/create-snapshot-fields.jpg){ align=center }
    <figcaption>Name the Snapshot</figcaption>
    </figure>

    The snapshot creation process will be shown like the following.

    <figure markdown="span">
    ![Snapshot Process](../../assets/annotations/automatic/snapshot-creation-process.png){ align=center }
    <figcaption>Snapshot Process</figcaption>
    </figure>

2. Upload from MCAP File

    An MCAP file is a [recording captured](../capture.md#capture-with-an-edgefirst-platform) by an [EdgeFirst Platform (Maivin or Raivin)](../../../platforms/quickstart.md).

    To create a snapshot from an MCAP file, visit the "Data Snapshots" page.

    <figure markdown="span">
    ![Data Snapshots](../../assets/annotations/automatic/data-snapshots.jpg){ align=center }
    <figcaption>Data Snapshots</figcaption>
    </figure>

    Either drag and drop an MCAP file into the page OR click on the "From File" button to allow selection of the MCAP file from your directories.

    <figure markdown="span">
    ![MCAP Import Snapshot](../../assets/annotations/automatic/mcap-file-import.jpg){ align=center }
    <figcaption>MCAP Import Snapshot</figcaption>
    </figure>

3. Upload from Zip/Arrow (EdgeFirst Dataset) Files

    The Zip/Arrow files together creates the [EdgeFirst Dataset Format](../../format/index.md).

    To create a snapshot from a Zip/Arrow files, visit the "Data Snapshots" page.

    <figure markdown="span">
    ![Data Snapshots](../../assets/annotations/automatic/data-snapshots.jpg){ align=center }
    <figcaption>Data Snapshots</figcaption>
    </figure>

    Either drag and drop the Zip/Arrow files into the page OR click on the "From File" button to allow selection of the Zip/Arrow files from your directories.

    <figure markdown="span">
    ![Zip/Arrow Import Snapshot](../../assets/annotations/automatic/zip-arrow-files-import.jpg){ align=center }
    <figcaption>Zip/Arrow Import Snapshot</figcaption>
    </figure>

    !!! warning "Uniform Names"
        The name of corresponding Zip and Arrow files must be same.

    !!! info "Zip/Arrow File pairs"
        The upload must come into Zip and Arrow file pairs.
        If there are multiple Zip and Arrow pairs, then each pair will become a sequence.

A snapshot can be created from one of the three ways as described above: *Create from Existing Dataset*, *Upload from MCAP File*, *Upload from Zip/Arrow File*.  The next section will show how to restore these created snapshots for auto-annotations.

{% include-markdown "discrete/datasets/restore_snapshot.md" heading-offset=2 %}

[Insert Image]

Next [navigate to the gallery](../management.md#view-dataset) of the dataset by clicking on the gallery button.  The figure below shows a side-by-side display of the annotations from frames 1-3.  The 2D annotations for both segmentation masks and bounding boxes were auto-generated in the background.

**Frame 1** | **Frame 2** | **Frame 3**
:------------------:|:------------------:|:------------------:
![Annotation 1]() | ![Annotation 2]() | ![Annotation 3]()

The next section will describe the *Semi-Automatic Ground Truth Generation* for additional user control during the auto-annotation process.

## Semi-Automatic Ground Truth Generation

This annotation feature is available after [capturing the dataset](../capture.md) into EdgeFirst Studio.  This process occurs in the [dataset gallery](../management.md#view-dataset) where the user has more
control over the annotation process.  This feature will preload all frames of a *video* sequence in the dataset into SAM-2 to generate segmentation masks, 2D bounding boxes, 3D bounding boxes (For Raivin/LiDAR Only) by tracking the object across the frames.

A complete description of this feature along with the functionalities of each buttons shown in this tutorial can be found under [Studio](../../../studio/agtg.md#semi-automatic-ground-truth-generation).

This feature is a three-step process: *Initialize AGTG Server*, *Annotate Starting Frame*, *Propagate*.

### Initialize AGTG Server

Inside the dataset gallery, click on the "AI Segment Tool" to start the AGTG server.

<figure markdown="span">
![Auto Segment Mode](../../assets/annotations/automatic/agtg-segment-tool.jpg){ align=center }
<figcaption>Auto Segment Mode</figcaption>
</figure>

If there is currently no AGTG server available, go ahead and click on "Launch AGTG Server".

<figure markdown="span">
![Launch AGTG Server](../../assets/annotations/manual/confirm-agtg-server-launch.jpg){ align=center }
<figcaption>Launch AGTG Server</figcaption>
</figure>

Please wait while the server is being initialized.

<figure markdown="span">
![Launch AGTG Server](../../assets/annotations/manual/agtg-server-initialization.jpg){ align=center }
<figcaption>Launch AGTG Server</figcaption>
</figure>

!!! warning "Active AGTG Server"
    This server is costing credits to run.  An inactivity of 15 minutes will auto-terminate this server.  Otherwise, once you have completed the annotations, please ensure to [terminate the AGTG server](index.md#terminate-agtg-server) to avoid spending more of your credits.

### Annotate Starting Frame

Once the server has been initialized, annotate the starting frame.  This is the only annotation required by the user. The rest of the frames will be annotated by SAM-2 and the AGTG process.  This step is also known as initializing the SAM-2 state.  Each object must be annotated independently so the tracker can assign a unique ID.

Start by drawing a bounding box for the first object by clicking and dragging.  For multiple objects in the frame, click "+" to add a new object as shown in red below.  The process for each object should be: *Add a new object* -> *Draw object prompt*.

By default, the prompts provided to SAM-2 are bounding boxes (mouse click and drag) which should cover the object to be annotated in the frame.  However, points can also be provided (mouse clicks) by clicking areas that are part of the object.

<figure markdown="span">
![AGTG Initial Prompts](../../assets/annotations/automatic/agtg-prompts.jpg){ align=center }
<figcaption>AGTG Initial Prompts</figcaption>
</figure>

### Propagate

Once the first frame has been annotated (*prompts for SAM-2*), specify the "End Frame" which marks the point where SAM-2 stops propagating.  By default this is the end of the sequence (last frame).  Once this has been specified, click on "Propagate" to start the propagation process.

As the frames propagate, you should see the frames being auto-annotated.  To stop the propagation process click on "Stop Propagation".

<figure markdown="span">
![Propagation Process](../../assets/annotations/automatic/propagation-process.jpg){ align=center }
<figcaption>Propagation Process</figcaption>
</figure>

Once the propagation completes as it reached the end frame, click on "Save Annotations" to save the generated annotations.

<figure markdown="span">
![Propagation Completed](../../assets/annotations/automatic/agtg-propagation-completed.jpg){ align=center }
<figcaption>Propagation Completed</figcaption>
</figure>

## Video Tutorials

This is a high level video tutorial shown an MCAP recording restored as a snapshot.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=720&end=1163" title="Auto Annotate Dataset" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## Next Steps

If you notice any errors on the annotations that require adjustments or any missing annotations that needs to be added, follow these tutorials that describe the [manual annotation](manual.md) features.
