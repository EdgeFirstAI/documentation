# Automatic Ground Truth Generation (AGTG)

The [AGTG pipeline](../../../studio/agtg.md) describes the stages for automating the annotation process of a dataset. There are two modes of operation.

1. Fully Automatic Ground Truth Generation: A background operation invoked at the time of dataset import as a [snapshot](../../../studio/snapshots.md).
2. Semi-Automatic Ground Truth Generation: User controlled dataset annotation process.

### Fully Automatic Ground Truth Generation

This annotation feature is available at the time of importing the dataset via [snapshot restoration](../../../studio/snapshots.md#restore-snapshot).  The auto-annotation process is done in the background allowing the user to focus on separate tasks.  This section will show the steps for performing this type of auto-annotation in EdgeFirst Studio.  However, this feature can also be deployed using the [EdgeFirst Client](../../perception/studio.md#restore-snapshots) in the command line.

This feature is a two-step process: **Create Snapshot** and **Restore Snapshot**.

#### Create Snapshot

##### Create from Existing Dataset

##### Upload from MCAP File

##### Upload from Zip/Arrow File

#### Restore Snapshot


### Semi-Automatic Ground Truth Generation

This annotation feature is available after [capturing the dataset](../capture.md) into EdgeFirst Studio.  This process occurs in the [dataset gallery](../management.md#viewing-datasets) where the user has more
control over the annotation process.  This feature will preload all frames of a *video* sequence in the dataset into SAM-2 to generate segmentation masks, 2D bounding boxes, 3D bounding boxes (For Raivin/LiDAR Only) by tracking the object across the frames. 

Inside the dataset gallery, click on the "AI Segment Tool" to start the AGTG server.

<figure markdown="span">
![Auto Segment Mode](../../assets/agtg-segment-tool.jpg){ align=center }
<figcaption>Auto Segment Mode</figcaption>
</figure>

If there is currently no AGTG server available, go ahead and click on "Launch AGTG Server".

<figure markdown="span">
![Launch AGTG Server](../../assets/confirm-agtg-server-launch.jpg){ align=center }
<figcaption>Launch AGTG Server</figcaption>
</figure>

Please wait while the server is being initialized.

<figure markdown="span">
![Launch AGTG Server](../../assets/agtg-server-initialization.jpg){ align=center }
<figcaption>Launch AGTG Server</figcaption>
</figure>

!!! warning "Active AGTG Server"
    This server is costing credits to run.  An inactivity of 15 minutes will auto-terminate this server.  Otherwise, once you have completed the annotations, please ensure to [terminate the AGTG server](index.md#terminate-agtg-server) to avoid spending more of your credits.

Once the server has been initialized, annotate the starting frame.  This is the only annotation required by the user at the start and the rest of the frames will be handled by SAM-2 and the AGTG process.

Start by drawing a bounding box for the first object by clicking and dragging.  For multiple objects in the frame, click "+" to add a new object as shown in red below.  The process for each object should be: *Add a new object* -> *Draw object prompt*. 

By default, the prompts provided to SAM-2 are bounding boxes (mouse click and drag) which should cover the object to be annotated in the frame.  However, points can also be provided (mouse clicks) by clicking areas that are part of the object. 

<figure markdown="span">
![AGTG Initial Prompts](../../assets/agtg-prompts.jpg){ align=center }
<figcaption>AGTG Initial Prompts</figcaption>
</figure>

Once the first frame has been annotated which acts as prompts for SAM-2, specify the "End Frame" which marks the point where SAM-2 stops propagated.  By default this is the end of the sequence (last frame).  Once this has been specified, click on "Propagate" to start the propagation process. 

As the frames propagate, you should see the frames being auto-annotated.  To stop the propagation process click on "Stop Propagation".



