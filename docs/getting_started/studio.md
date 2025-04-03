# Studio Tutorials

These EdgeFirst Studio tutorials cover various aspects of the workflow in deeper detail than the quickstart guide.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/MmoDCXj72jk?si=I8gTw2VCtcts69ks" title="EdgeFirst Studio Overview" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>



### Guided Workflow


#### EdgeFirst Studio Workspace

Next become familiar with the EdgeFirst Studio workspace. 

The following figure provides a general overview of the workspace layout. 

<figure markdown="span">
![Navigation](studio/navigation/assets/image.png){ align=center }
<figcaption>Navigation</figcaption>
</figure>

Please see the overview of [Navigating the Workspace](studio/navigation/index.md) for more details.

#### Create a Project

Using the account you just created, sign in to EdgeFirst Studio. 
Once you're logged in, create your first project. Provide a name and description of the project 
that reflects your goals. 

<figure markdown="span">
![Create a New Project](getting_started/assets/new_project.jpg){ align=center }
<figcaption>Create a New Project</figcaption>
</figure>

#### Explore Dataset

Try our sample Raivin dataset for training a Fusion Model.

<figure markdown="span">
![Raivin Dataset](getting_started/assets/raivin-ultra-short.jpg){ align=center }
<figcaption>Raivin Dataset</figcaption>
</figure>

<figure markdown="span">
![Dataset Fields](datasets/assets/dataset-fields.png){ align=center }
<figcaption>Dataset Fields</figcaption>
</figure>

Please see the overview of the [Datasets Dashboard](datasets/index.md) for more details regarding the 
dataset attributes in EdgeFirst Studio.

#### Train Model

The following training session is a completed session from training a Fusion model
from the dataset provided. 

<figure markdown="span">
![Sample Training Session](getting_started/assets/training-session.jpg){ align=center }
<figcaption>Sample Training Session</figcaption>
</figure>

<figure markdown="span">
![Training Session Fields](models/assets/training/training-session-fields.jpg){ align=center }
<figcaption>Training Session Fields</figcaption>
</figure>

For more details regarding deploying training sessions, please see 
[Training Modelpack](models/modelpack/training.md) for training Vision models and 
[Training Fusion](models/fusion/training.md) for training Fusion models.

#### Validate Model

The following validation session is a completed session from validating a Fusion model
from the dataset provided.

<figure markdown="span">
![Sample Validation Session](getting_started/assets/validation-session.jpg){ align=center }
<figcaption>Sample Validation Session</figcaption>
</figure>

<figure markdown="span">
![Validation Session Fields](models/assets/validation/validation-session-fields.jpg){ align=center }
<figcaption>Validation Session Fields</figcaption>
</figure>

For more details regarding deploying validation sessions, please see 
[Validating Modelpack](models/modelpack/validation.md) for validating Vision models and 
[Validating Fusion](models/fusion/validation.md) for validating Fusion models.

### Hands-on Workflow

This workflow requires the user has signed up and logged in to EdgeFirst Studio
and that the user is familiar with the EdgeFirst Studio workspace. Please see
the [Guided Workflow](#guided-workflow) above for more details. 

#### Record Data

This step requires an [EdgeFirst Platform](platforms/quickstart.md) for recording
data. However, we also provide [public datasets](TBA) for user onboarding
or licensing. When starting from scratch, it is common to start recording your own data to
build your own dataset. 

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/GVlkq9p0G5c" title="Dataset Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

On your browser, enter the following URL `https://<hostname>/mcap` and the following page will appear.

!!! note
    Replace `<hostname>` with the hostname of your device.

<figure markdown="span">
![MCAP Recording Page](getting_started/assets/mcap-recording-page.jpg){ align=center }
<figcaption>MCAP Recording Page</figcaption>
</figure>

To start recording toggle/enable the *Recording* button indicated above and
to stop the recording retoggle/disable the same button. 

!!! note
    For more information, please see [MCAP Recording Service](platforms/recording.md).

#### Download Recorded Data

Once recorded, download the MCAP file.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=0&end=558" title="Download Recording" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

The MCAP file will appear under the list of MCAP files which can then be downloaded.

<figure markdown="span">
![Recorded MCAP](getting_started/assets/recorded-mcap.jpg){ align=center }
<figcaption>Recorded MCAP</figcaption>
</figure>

#### Upload Recorded Data

Once an MCAP has been recorded, upload the data into EdgeFirst Studio.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=558&end=720" title="Upload MCAP" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

Inside EdgeFirst Studio, select *Data Snapshots* under the tool options.

<figure markdown="span">
![Data Snapshots](getting_started/assets/data-snapshots.jpg){ align=center }
<figcaption>Data Snapshots</figcaption>
</figure>

!!! note
    A project has already been created intended for people detection. This step
    has been covered in [Create a Project](#create-a-project).

Upload the recorded MCAP by clicking *FROM FILE* which opens a new window dialog
for selecting the MCAP downloaded in your PC.

<figure markdown="span">
![Upload MCAP](getting_started/assets/mcap-upload.jpg){ align=center }
<figcaption>Upload MCAP</figcaption>
</figure>

Once the MCAP file is selected, this would start the upload progress in EdgeFirst Studio.

**Upload Progress** | **Completed Upload** 
:------------------:|:------------------:
![Progress](getting_started/assets/upload-progress.jpg) | ![Complete](getting_started/assets/upload-completed.jpg)

!!! note
    For more information, please see [Uploading MCAP Recordings](TBA).

#### Annotate Dataset

If you have imported an annotated public dataset, you do not need to follow
these steps as the dataset has already been annotated, but feel free to follow
along to be familiar with the annotation workflow in EdgeFirst Studio. 

##### Auto Annotations

To reduce the effort required by the user to annotate the dataset, part of this
process is to auto-annotate the dataset upon upload.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=720&end=1163" title="Auto Annotate Dataset" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

To run auto-annotations on the recorded data, click *Restore* on the uploaded snapshot.

<figure markdown="span">
![Restore Snapshot](getting_started/assets/restore-snapshot.jpg){ align=center }
<figcaption>Restore Snapshot</figcaption>
</figure>

The following fields are for the user to specify. Adjust the following fields for your own use case.

<figure markdown="span">
![Restore Snapshot Fields](getting_started/assets/restore-snapshot-fields.jpg){ align=center }
<figcaption>Restore Snapshot Fields</figcaption>
</figure>

Once specifed, click *RESTORE SNAPSHOT* to start the auto-annotation process. This
will start the auto-annotation process.

<figure markdown="span">
![Restore Process](getting_started/assets/snapshot-started.jpg){ align=center }
<figcaption>Restore Process</figcaption>
</figure>

The progress will be shown on the dataset specified in the project.

<figure markdown="span">
![Restore Progress](getting_started/assets/restore-snapshot-progress.jpg){ align=center }
<figcaption>Restore Progress</figcaption>
</figure>

!!! note
    For more information, please see [Dataset Auto-Annotation](TBA).

##### Audit Annotations

This step requires verifying the outputs of the auto-annotations and to make
corrections if necessary in order to have a proper fully annotated dataset.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/j-75Q5-_dC0?start=1536&end=2144" title="Visualize Annotations" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

Navigate to the gallery of the dataset and then select the sequence in the dataset 
to visualize each image with the annotations generated.

**Annotation 1** | **Annotation 2** | **Annotation 3** 
:------------------:|:------------------:|:------------------:
![Annotation 1](getting_started/assets/annotation-1.jpg) | ![Annotation 2](getting_started/assets/annotation-2.jpg) | ![Annotation 3](getting_started/assets/annotation-3.jpg)

Some annotations were missed from the auto-annotations and to correct those errors, we can utilize the auto-segment tool.
Start by enabling an AI Assisted Ground Truth server by navigating to the *Cloud Instances* under the tool options.

<figure markdown="span">
![Cloud Instances](getting_started/assets/cloud-instances.jpg){ align=center }
<figcaption>Cloud Instances</figcaption>
</figure>

Start and launch a new server to host the auto-segmentation backend.

<figure markdown="span">
![Start a Server](getting_started/assets/launch-ai-server.jpg){ align=center }
<figcaption>Start a Server</figcaption>
</figure>

Navigate back to the dataset and enable edit mode.

<figure markdown="span">
![Edit Mode](getting_started/assets/edit-mode.jpg){ align=center }
<figcaption>Edit Mode</figcaption>
</figure>

Select the *AI Image Segment Tool* and then enable the *SAM Box Tool*

<figure markdown="span">
![Auto Segment Mode](getting_started/assets/enable-auto-segment-tool.jpg){ align=center }
<figcaption>Auto Segment Mode</figcaption>
</figure>

Draw a bounding box around the person that was missed and then click *CREATE ANNOTATION* to create
the drawn segmentation mask. Click *SUBMIT* to accept the annotation. 

<figure markdown="span">
![Segment Tool](getting_started/assets/segment-tool.jpg){ align=center }
<figcaption>Segment Tool</figcaption>
</figure>

Draw a bounding box annotation around the person that was missed by selecting the *Box Tool*.
Click *SUBMIT* to accept the annotation. 

<figure markdown="span">
![Box Tool](getting_started/assets/box-tool.jpg){ align=center }
<figcaption>Box Tool</figcaption>
</figure>

As part of the audit process is to go over each sample in the dataset and correcting
any missed annotations or incorrect annotations.

!!! note
    There are more features available for correcting the annotations.
    For more information, please see [Dataset Audit Annotation](TBA)

#### Combine Multiple Datasets

If you want to expand your dataset you can combine multiple datasets.

#### Split Dataset

Before training your model, it is highly suggested to split your dataset into
dedicated training and validation groups. This intention is to reserve samples 
only for training and samples only for validation. In this manner, we have samples
for training a model and validating a model. 

#### Train Model

You can now start training your model with a dataset that is fully annotated with
samples reserved for training and validation. 

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Q8uiYJb1HJ4" title="EdgeFirst Training" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

#### Validate Model

After a model is trained, we can validate the performance of the model to verify
if the model is "field ready" to be deployed. 

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/oKh4k0CCLmU?si=PPmbJ1-8dZPLhGh2" title="EdgeFirst Validation" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

#### Deploy Model

Once the model has been validated, we can now deploy the model on device and
start running inference on the model.