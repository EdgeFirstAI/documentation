# Getting Started

Welcome to EdgeFirst Studio!  Follow this Quickstart for user onboarding from start to finish.

{% include-markdown "discrete/signup.md" %}

{% include-markdown "discrete/login.md" %}

## Create Project

1. Now that you are in the *Projects* or Main page, create your first project by clicking on the "New Project" button on the top-right corner of the page.

    <figure markdown="span">
    ![Create Project](assets/create-project.jpg){ align=center }
    <figcaption>The location of the "New Project" button</figcaption>
    </figure>

2. Provide a name and a description of the project as shown in the example below.  Click the "Create" button to create your new project.

    <figure markdown="span">
    ![Project Details](assets/create-project-fields.jpg){ align=center }
    <figcaption>Project Details</figcaption>
    </figure>

3. Your created project will be shown like the example below.  

    <figure markdown="span">
    ![New Project](assets/new-project.jpg){ align=center }
    <figcaption>Both Projects</figcaption>
    </figure>

The next sections will invite you to follow along the end-to-end workflow for recording a video or capturing images using a phone and then upload the captured data into EdgeFirst Studio for annotation and then model training, validation, and deployment on various platforms. 

!!! warning "Data Usage"
    It is recommended to use a phone connected to a Wifi network. A device connected to mobile data might be subject to intense usage when uploading files as video files or image files can be large in size. In the examples below, the video file used was ~15MB and the image files were ~2MB.

!!! info "Workflows"
    The workflow below is based on the *Web-Based Workflow* which requires only a phone and a PC.  There are other [workflows](getting_started/workflows/index.md) that support different hardware requirements. 

## Capture with a Phone

The examples below will show capturing image samples of coffee cups using a phone for training a Vision model that detects coffee cups. However, you can choose any type of objects in your dataset.

To capture samples of coffee cups, you can record a video as shown below.  In this example, a five second video was recorded. 

<figure markdown="span">
![Mobile Video Capture](getting_started/assets/workflows/mobile-video-capture.jpg){ align=center }
<figcaption>Android Mobile Video Capture</figcaption>
</figure>

Furthermore, you can also capture individual images of coffee cups as shown below. 

<figure markdown="span">
![Mobile Image Capture](getting_started/assets/workflows/mobile-image-capture.jpg){ align=center }
<figcaption>Android Mobile Image Capture</figcaption>
</figure>

!!! tip
    It is recommended to use videos rather than individual images.  This is because the Automatic Ground Truth Generation (AGTG) feature leverages SAM-2 with tracking information which only needs a single annotation to annotate all frames.  However, individual images requires more effort to annotate each image separately.

!!! warning
    For demo purposes, the dataset is kept small.  However, training on limited datasets will result in poor model performances when the model is deployed under conditions that differs from the dataset samples.  It is suggested to increase the amount of training data under various conditions to train a more robust model.

## Create a Dataset

Once you have captured your video and some sample images for your dataset, navigate to a web browser on your mobile device and [login][login] to EdgeFirst Studio.  Once logged in to EdgeFirst Studio, navigate to the "Object Detection" project that was created and click on the datasets button that is indicated in red.

<figure markdown="span">
![Object Detection Project](getting_started/assets/workflows/mobile-projects.jpg){ align=center }
<figcaption>Object Detection Project</figcaption>
</figure>

This will bring you to the "Datasets" page of the selected project.  Create a new dataset container by clicking the "New Dataset" button that is indicated in red.

<figure markdown="span">
![New Dataset](getting_started/assets/workflows/mobile-new-dataset.jpg){ align=center }
<figcaption>New Dataset</figcaption>
</figure>

Add the dataset and annotation container name, labels, and dataset description as indicated by the fields below.  It is up to you to specify the information in the fields and you do not have to strictly follow the example shown below.  Click the "Create" button once the fields have been filled.

<figure markdown="span">
![Dataset Fields](getting_started/assets/workflows/mobile-dataset-details.jpg){ align=center }
<figcaption>Dataset Fields</figcaption>
</figure>

Your created dataset will look as follows.

<figure markdown="span">
![Created Dataset](getting_started/assets/workflows/mobile-created-dataset.jpg){ align=center }
<figcaption>Created Dataset</figcaption>
</figure>

## Upload Videos or Images

Once the dataset container has been created, click on the dataset extended menu (three dots) and select import.

<figure markdown="span">
![Dataset Import Option](getting_started/assets/workflows/mobile-dataset-import-option.jpg){ align=center }
<figcaption>Dataset Import Option</figcaption>
</figure>

This will bring you to the "Import Dataset" page.

<figure markdown="span">
![Dataset Import](getting_started/assets/workflows/mobile-import-dataset.jpg){ align=center }
<figcaption>Dataset Import</figcaption>
</figure>

First you will be importing the video recording from [step 1](#capture-with-a-phone).  Click on the dropdown that says "Select an Import Type" and then specify "Video" and then click "Done" as shown below. 

<figure markdown="span">
![Dataset Video Import](getting_started/assets/workflows/mobile-video-import-type.jpg){ align=center }
<figcaption>Dataset Video Import</figcaption>
</figure>

Now that the import type is specified to a video file, click on "Select File" as indicated. 

<figure markdown="span">
![Select Video File](getting_started/assets/workflows/mobile-select-video-file.jpg){ align=center }
<figcaption>Select Video File</figcaption>
</figure>

On an android device, this will bring up the option to specify the location of the files.

<figure markdown="span">
![Android Select File Options](getting_started/assets/workflows/mobile-video-options.jpg){ align=center }
<figcaption>Android Select File Options</figcaption>
</figure>

In my current setup, I have selected "My Files" from the options above and then "Videos" which will allow me to pinpoint the location of the video I have recorded. 

<figure markdown="span">
![Android File Manager](getting_started/assets/workflows/mobile-video-location.jpg){ align=center }
<figcaption>Android File Manager</figcaption>
</figure>

!!! warning
    
    Only one video can be imported at a time.

Once the video file has been selected, set the desired FPS (frames per second) ratio, and then go ahead and click the "Start Import" button to start importing the video file. 

<figure markdown="span">
![Import Fields](getting_started/assets/workflows/mobile-video-import-fields.jpg){ align=center }
<figcaption>Import Fields</figcaption>
</figure>

This will start the import process and once it is completed, you should see the number of images in the dataset increased.  If you do not see any changes, refresh the browser. 

<figure markdown="span">
![Imported Video](getting_started/assets/workflows/imported-video-outcome.jpg){ align=center }
<figcaption>Imported Video</figcaption>
</figure>

Next, if you have captured images from [step 1](#capture-with-a-phone) you will import the captured images.  Navigate back to the "Import Dataset" page (refer to the [top](#upload-videos-or-images)).

<figure markdown="span">
![Dataset Import](getting_started/assets/workflows/mobile-import-dataset.jpg){ align=center }
<figcaption>Dataset Import</figcaption>
</figure>

Click on "Click to select images".  This will bring up the option to specify the location of the files.

<figure markdown="span">
![Android Mobile Media Picker](getting_started/assets/workflows/mobile-media-picker.jpg){ align=center }
<figcaption>Android Mobile Media Picker</figcaption>
</figure>

In my current setup, I have selected "Media Picker" from the options above and then I have multi-selected the images I want to import by press and hold on a single image to enable multi-select.  To import, I pressed "Select".

<figure markdown="span">
![Android Multiselect Images](getting_started/assets/workflows/mobile-multi-select-images.jpg){ align=center }
<figcaption>Android Multiselect Images</figcaption>
</figure>

Once the image files have been selected, the progress for the image import will be shown. 

<figure markdown="span">
![Image Import Progress](getting_started/assets/workflows/image-import-progress.jpg){ align=center }
<figcaption>Image Import Progress</figcaption>
</figure>

Once it completes, you should see the number of images in the dataset increase by the amount of selected images.  If you do not see any changes, refresh your browser.

<figure markdown="span">
![Imported Images](getting_started/assets/workflows/imported-images-outcome.jpg){ align=center }
<figcaption>Imported Images</figcaption>
</figure>

Next [view the gallery of the dataset](datasets/tutorials/management.md#viewing-datasets) to confirm all the captured data has been uploaded.  You should see the imported video file and images in the gallery.  Note that videos appear as sequences with a play button overlay on the preview thumbnail.

<figure markdown="span">
![Coffee Cup Gallery](getting_started/assets/workflows/pc-dataset-gallery.jpg){ align=center }
<figcaption>Coffee Cup Gallery</figcaption>
</figure>

Once all the captured data has been uploaded to the dataset container, you will now assign groups to the data to split the data into training and validation sets.  Follow the [tutorial for creating groups](datasets/tutorials/management.md#splitting-datasets) with an 80% partition to training and 20% partition to validation.  The final outcome for the groups should look as follows.

<figure markdown="span">
![Dataset Groups](getting_started/assets/workflows/dataset-groups.jpg){ align=center }
<figcaption>Dataset Groups</figcaption>
</figure>

Now that you have imported captured images or videos into EdgeFirst Studio and have split the captured data into training and validation partitions, you can now start annotating your data as shown in the next section below.

## Annotate the Dataset

In this step, you will need a personal computer (PC) with access to Wifi to [log in][login] to EdgeFirst Studio for annotating the dataset.  When annotating the dataset, you will be using AI assistance to reduce the effort by running auto segmentation and bounding boxes on the objects in the frame.  Once logged in to EdgeFirst Studio, follow the [Auto Annotations](datasets/tutorials/annotations.md#auto-annotations-via-gallery) instructions to auto-annotate the video sequence that was imported.  Otherwise, follow the [Audit 2D Annotations](datasets/tutorials/annotations.md#audit-2d-annotations) instructions to annotate the images captured.

A complete annotation will have a segmentation mask and a bounding box for each object in the frame.  Shown below is an example. 

<figure markdown="span">
![Sample Annotation](getting_started/assets/workflows/sample-2d-annotation.jpg){ align=center }
<figcaption>Sample Annotation</figcaption>
</figure>

## Train a Vision Model 

Once you have a proper dataset that is fully annotated and split into training and validation groups, you can now start training your Vision model.  For instructions to train a Vision model, please refer to the [Training ModelPack Tutorial](models/modelpack/training.md).

A completed training session will look like the following figure.

<figure markdown="span">
![Training Session](getting_started/assets/workflows/completed-training-session.jpg){ align=center }
<figcaption>Training Session</figcaption>
</figure>

## Validate the Trained Model

Once the model is trained, you can now start validating the performance of the model to verify if the model is ready for deployment. 

For instructions to validate a Vision model, please refer to the [Validating ModelPack Tutorial](models/modelpack/validation/managed.md).

Once the validation session completes, the metrics will be displayed like the following figure.

<figure markdown="span">
![Validation Metrics](getting_started/assets/workflows/sample-validation-metrics.jpg){ align=center }
<figcaption>Validation Metrics</figcaption>
</figure>

## Deploy the Model

Once you have validated your trained model, let's take a look at an example of how this model can be deployed in your PC by following the tutorial [Deploying to the PC](models/modelpack/deployment/pc.md). 

If you have an NXP i.MX 8M Plus EVK you can also run your model directly on the device using the EdgeFirst Middleware by following the tutorial [Deploying to Embedded Targets](models/modelpack/deployment/evk.md).

!!! note

    Support for additional platforms beyond the NXP i.MX 8M Plus will be available soon.  Let us know which platform you'd like to see supported next!

If you have an [EdgeFirst Platform](platforms/index.md) such as the Maivin or Raivin then you can deploy and run the model using the bundled EdgeFirst Middleware by following the tutorial [Deploying to EdgeFirst Platforms](models/modelpack/deployment/maivin.md).

In this Quickstart guide, you have created your EdgeFirst Studio Account, logged in to EdgeFirst Studio, and created your very first project and ran your first experiment by capturing images and videos, annotating datasets, training a Vision model, validating the trained model, and deploying the model back into the PC, EdgeFirst Plaform, or the i.MX 8M Plus EVK. 

## Next Steps

For these next steps, it is recommended to be familiar with the concepts and UI elements in EdgeFirst Studio as described in the [EdgeFirst Studio: Overview](getting_started/studio.md).  Next, users are invited to follow along other various [User Workflows](getting_started/workflows/index.md) that are tailored towards various hardware requirements and resources available to the user.

!!! tip "Need Help?"
    📬 Have questions or ran into an issue?  
    Feel free to [email our support team](mailto:support@edgefirst.ai) — we’re here to help!
