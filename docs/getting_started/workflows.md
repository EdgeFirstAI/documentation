# EdgeFirst Studio: From Start to Deployment

This tutorial will walk a user through a high-level overview of getting started with EdgeFirst Studio by exploring individual processes from collecting
and curating datasets to training, validating, and deploying EdgeFirst models.

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/MmoDCXj72jk?si=I8gTw2VCtcts69ks" title="EdgeFirst Studio Overview" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

This tutorial will showcase two workflows. The first workflow will provide a guided user experience by providing completed experiments for users to follow along merely acting as an observer to get a general idea of the process. The second workflow will be much more user involved by providing instructions for the user to be familiar with using the tools available. 

## Guided Workflow with Completed Experiments

*coming soon*

## Hands-on Workflow

This workflow continues from the steps shown in [Getting Started](../index.md#edgefirst-studio-quickstart) which requires the user to have signed up for
EdgeFirst Studio, logged in to EdgeFirst Studio, and created their first project.

This tutorial shows the process of recording data from scratch, annotating data
in EdgeFirst Studio, training and validating models, and then finally deploying 
models in an EdgeFirst platform. 

!!! note
    This tutorial will provide examples on training, validating, and deploying
    *Vision models* described in [Modelpack Tutorials](models.md#modelpack-tutorials).

If you have an EdgeFirst Platform, please proceed to step 1. Otherwise, proceed to step 5 for using a provided public dataset. However, feel free to follow along all the steps laid out to become familiar with the workflow.

### 1. Record Data

When starting from scratch, it is common to start recording your own data to build your own dataset. This step requires an [EdgeFirst Platform](../platforms/quickstart.md) for recording data. However, we also provide [Public Datasets](../datasets/tutorials.md#public-datasets) for users without an EdgeFirst Platform. 

Deploying an EdgeFirst Platform will allow users access to the following page for recording data.

<figure markdown="span">
![WebUI Service Page](../datasets/assets/webui-service-page.jpg){ align=center }
<figcaption>Preview: WebUI Service</figcaption>
</figure>

For instructions on capturing and recording data, refer to the [Capture/Record Data Tutorial](../datasets/tutorials.md#capturerecord-data).

### 2. Download Recorded Data

Once data is recorded which is stored as an MCAP file, download the MCAP file.

<figure markdown="span">
![Recorded MCAP](../datasets/assets/recorded-mcap.jpg){ align=center }
<figcaption>Preview: Download MCAP</figcaption>
</figure>

For instructions on downloading the recorded MCAP file, refer to the [Download Captured Data Tutorial](../datasets/tutorials.md#download-recorded-data).

### 3. Upload Recorded Data to EdgeFirst Studio

Once an MCAP file has been downloaded, upload the MCAP recording to EdgeFirst Studio.

<figure markdown="span">
![Upload MCAP](../datasets/assets/mcap-upload.jpg){ align=center }
<figcaption>Preview: Upload Feature</figcaption>
</figure>

For instructions on uploading the recorded MCAP file to EdgeFirst Studio, refer to the [Upload Recorded Data Tutorial](../datasets/tutorials.md#upload-recorded-data-to-edgefirst-studio).

### 4. Annotate Dataset

Once an MCAP recording has been uploaded to EdgeFirst Studio, we can then run auto-annotations on the recording to reduce the effort needed from the user. Otherwise, the user can manually annotate the dataset.

<figure markdown="span">
![Restore Snapshot](../datasets/assets/restore-snapshot.jpg){ align=center }
<figcaption>Preview: Restore for Auto-Annotations Feature</figcaption>
</figure>

For instructions on annotating the uploaded data, refer to the [Annotating Data Tutorial](../datasets/tutorials.md#data---dataset-annotating-data).

### 5. Combine Multiple Datasets

This step utilizes the [copy dataset feature](../datasets/tutorials.md#copying-datasets) in EdgeFirst Studio. This feature
allows copying of *read-only* datasets into your own dataset to give write permissions. This feature can also copy multiple datasets into a single container to expand the overall dataset. 

<figure markdown="span">
![Copy Dataset Options](../datasets/assets/copy-dataset-options.jpg){ align=center }
<figcaption>Preview: Copy Datasets</figcaption>
</figure>

For users that do not have an EdgeFirst Platform, but would like to use the public *read-only* datasets provided, follow the instructions for [Copying Datasets](../datasets/tutorials.md#copying-datasets) into
a dataset container with write access.

For users that followed steps 1-4 and would like to expand their dataset, follow the
instructions for [Combining Datasets](../datasets/tutorials.md#combining-datasets)

### 6. Split Dataset

Before training your model, it is highly suggested to split your dataset into
dedicated training and validation groups. This intention is to reserve samples 
only for training and samples only for validation.

<figure markdown="span">
![Groups Field](../datasets/assets/groups-field.jpg){ align=center }
<figcaption>Preview: Dataset Split</figcaption>
</figure>

For instructions on splitting the dataset in train and validation groups, refer to the [Splitting Datasets Tutorial](../datasets/tutorials.md#splitting-datasets)

### 7. Train Model

Once you have a proper dataset that is fully annotated and split into training and validation groups, you can now start training your model.

<figure markdown="span">
![Training Options](../models/assets/training/modelpack-training-options.jpg){ align=center }
<figcaption>Preview: Training Options</figcaption>
</figure>

Since the dataset provided in the demo contains 2D annotations (bounding boxes and segmentation masks) we can train a Vision model using Modelpack. For instructions to train a Vision model, please refer to [Training Modelpack Tutorial](../models/modelpack/training.md)

### 8. Validate Model

Once the model is trained, you can now start validating the performance of the model to verify if the model is ready for deployment. 

<figure markdown="span">
![Validation Options](../models/assets/validation/modelpack-validation-options.jpg){ align=center }
<figcaption>Preview: Validation Options</figcaption>
</figure>

For instructions to validate a Vision model, please refer to [Validating Modelpack Tutorial](../models/modelpack/validation.md)

### 9. Deploy Model

Once the model has been validated and deemed the performance to be reasonable for deployment, you can now deploy the model on an EdgeFirst Platform and start running inference on the model. 

*coming soon*