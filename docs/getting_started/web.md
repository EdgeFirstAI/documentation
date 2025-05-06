# Web-Based Workflow

In this workflow, we will explore recording a video or capturing images using a mobile device and then upload the captured data into EdgeFirst Studio for annotation and then model training, validation, and deployment using the PC. This workflow requires the user to have signed up and logged in to EdgeFirst Studio and followed the initial steps described in the [EdgeFirst Studio Quickstart](../index.md#initial-steps).

!!! warning
    It is recommended to use a mobile device connected to a Wifi network. A device connected to mobile data might be subject to intense usage when uploading files as video files or image files can be large in size. In the examples below, the video file used was ~15MB and the image files were ~2MB.

## 1. Capture Data Using a Mobile Device

In this workflow, we will be exploring capturing data with samples of coffee cups for training a detection model that detects coffee cups. However, you can choose any type of objects in your dataset, but be mindful that the label for these objects remains consistent for all samples. 

In this workflow, we will be recording a 5 second video on coffee cups as shown below. 

<figure markdown="span">
![Mobile Video Capture](assets/workflows/mobile-video-capture.jpg){ align=center }
<figcaption>Android Mobile Video Capture</figcaption>
</figure>

Furthermore, we will also capture images of coffee cups as shown below. 

<figure markdown="span">
![Mobile Image Capture](assets/workflows/mobile-image-capture.jpg){ align=center }
<figcaption>Android Mobile Image Capture</figcaption>
</figure>

## 2. Visit EdgeFirst Studio

Once you have captured your video and some sample images for your dataset on your mobile device, navigate to a web browser on your mobile device and [login][login] to EdgeFirst Studio. Once logged in to EdgeFirst Studio, navigate to the "Object Detection" project that was created in the [EdgeFirst Studio Quickstart](../index.md#initial-steps) and click on the datasets button that is indicated in red.

<figure markdown="span">
![Object Detection Project](assets/workflows/mobile-projects.jpg){ align=center }
<figcaption>Object Detection Project</figcaption>
</figure>

This will bring you to the Datasets page of the selected project. Create a new dataset container by clicking on "NEW DATASET".

<figure markdown="span">
![New Dataset](assets/workflows/mobile-new-dataset.jpg){ align=center }
<figcaption>New Dataset</figcaption>
</figure>

Add the dataset and annotation container name, labels, and dataset description as indicated by the fields below. This information can be specified by the user and does not have to strictly follow the example shown below. Click the "CREATE" button once the fields have been filled.

<figure markdown="span">
![Dataset Fields](assets/workflows/mobile-dataset-details.jpg){ align=center }
<figcaption>Dataset Fields</figcaption>
</figure>

Your created dataset will look as follows.

<figure markdown="span">
![Created Dataset](assets/workflows/mobile-created-dataset.jpg){ align=center }
<figcaption>Created Dataset</figcaption>
</figure>

## 3. Upload Data to EdgeFirst Studio

Once the dataset container has been created, click on the dataset extended menu (three dots) and select import.

<figure markdown="span">
![Dataset Import Option](assets/workflows/mobile-dataset-import-option.jpg){ align=center }
<figcaption>Dataset Import Option</figcaption>
</figure>

This will bring you to the "Import Dataset" page.

<figure markdown="span">
![Dataset Import](assets/workflows/mobile-import-dataset.jpg){ align=center }
<figcaption>Dataset Import</figcaption>
</figure>

First we will be importing the video recording from [step 1](#1-capture-data-using-a-mobile-device). Click on the dropdown that says "Select an Import Type" and then specify "Video" and then click "Done" as shown below. 

<figure markdown="span">
![Dataset Video Import](assets/workflows/mobile-video-import-type.jpg){ align=center }
<figcaption>Dataset Video Import</figcaption>
</figure>

Now that the import type is specified to a video file, click on "Select File" as indicated. 

<figure markdown="span">
![Select Video File](assets/workflows/mobile-select-video-file.jpg){ align=center }
<figcaption>Select Video File</figcaption>
</figure>

On an android device, this will bring up the option to specify the location of the files.

<figure markdown="span">
![Android Select File Options](assets/workflows/mobile-video-options.jpg){ align=center }
<figcaption>Android Select File Options</figcaption>
</figure>

In my current setup, I have selected "My Files" from the options above and then "Videos" which will allow me to pinpoint the location of the video I have recorded. 

<figure markdown="span">
![Android File Manager](assets/workflows/mobile-video-location.jpg){ align=center }
<figcaption>Android File Manager</figcaption>
</figure>

Once the video file has been selected, go ahead and click "START IMPORT" to start importing the video file. 

<figure markdown="span">
![Import Fields](assets/workflows/mobile-video-import-fields.jpg){ align=center }
<figcaption>Import Fields</figcaption>
</figure>

This will start the import process and once it is completed, you should see the number of images in the dataset increased. If you do not see any changes, refresh the browser. 

<figure markdown="span">
![Imported Video](assets/workflows/imported-video-outcome.jpg){ align=center }
<figcaption>Imported Video</figcaption>
</figure>

Next we will import the captured images from [step 1](#1-capture-data-using-a-mobile-device). 
Navigate back to the "Import Dataset" page (refer to the [top](#3-upload-data-to-edgefirst-studio)).

<figure markdown="span">
![Dataset Import](assets/workflows/mobile-import-dataset.jpg){ align=center }
<figcaption>Dataset Import</figcaption>
</figure>

Click on "Click to select images". This will bring up the option to specify the location of the files.

<figure markdown="span">
![Android Mobile Media Picker](assets/workflows/mobile-media-picker.jpg){ align=center }
<figcaption>Android Mobile Media Picker</figcaption>
</figure>

In my current setup, I have selected "Media Picker" from the options above and then I have multi-selected the images I want to import by press and hold on a single image to enable multi-select. To import, I pressed "Select".

<figure markdown="span">
![Android Multiselect Images](assets/workflows/mobile-multi-select-images.jpg){ align=center }
<figcaption>Android Multiselect Images</figcaption>
</figure>

Once the image files have been selected, the progress for the image import will be shown. 

<figure markdown="span">
![Image Import Progress](assets/workflows/image-import-progress.jpg){ align=center }
<figcaption>Image Import Progress</figcaption>
</figure>

Once it completes, you should see the number of images in the dataset increase by the amount of selected images. If you do not see any changes, refresh your browser.

<figure markdown="span">
![Imported Images](assets/workflows/imported-images-outcome.jpg){ align=center }
<figcaption>Imported Images</figcaption>
</figure>

Next [view the gallery of the dataset](../datasets/tutorials.md#viewing-datasets) to confirm all the captured data has been uploaded. You should see the imported video file and images in the gallery.

<figure markdown="span">
![Coffee Cup Gallery](assets/workflows/pc-dataset-gallery.jpg){ align=center }
<figcaption>Coffee Cup Gallery</figcaption>
</figure>

Once all the captured data has been uploaded to the dataset container, we will now assign groups to the data to split the data into training and validation sets. First delete the empty default groups that were created (if currently present). Follow the [tutorial for creating groups](../datasets/tutorials.md#splitting-datasets) with an 80% partition to training and 20% partition to validation. The final outcome for the groups should look as follows.

<figure markdown="span">
![Dataset Groups](assets/workflows/dataset-groups.jpg){ align=center }
<figcaption>Dataset Groups</figcaption>
</figure>

Now that we have imported some data into EdgeFirst Studio and have split the captured data into training and validation partitions, we can now start annotating our data as shown in the next section below.

## 4. Annotate Data in EdgeFirst Studio

In this step, we will be using a personal computer with access to Wifi to [log in][login] to EdgeFirst Studio for annotating the captured data. When annotating the dataset, we will be using AI assistance to annotate the ground truth to perform auto segmentation and bounding boxes on the objects of interest in the frame. Once logged in to EdgeFirst Studio, follow instructions for [auto-annotating the dataset](../datasets/tutorials.md#auto-annotations-via-gallery). Otherwise, for auditing individual annotations, following instructions from [Audit 2D Annotations](../datasets/tutorials.md#audit-2d-annotations).

A complete annotation will have a segmentation mask and a bounding box for each object in the frame. Shown below is an example. 

<figure markdown="span">
![Sample Annotation](assets/workflows/sample-2d-annotation.jpg){ align=center }
<figcaption>Sample Annotation</figcaption>
</figure>

## 5. Train a Model from the Annotated Data

Once you have a proper dataset that is fully annotated and split into training and validation groups, you can now start training your Vision model. For instructions to train a Vision model, please refer to the [Training ModelPack Tutorial](../models/modelpack/training.md).

A completed training session will look like the following figure.

<figure markdown="span">
![Training Session](assets/workflows/completed-training-session.jpg){ align=center }
<figcaption>Training Session</figcaption>
</figure>

## 6. Validate the Trained Model

Once the model is trained, you can now start validating the performance of the model to verify if the model is ready for deployment. 

For instructions to validate a Vision model, please refere to the [Validating ModelPack Tutorial](../models/modelpack/validation.md).

Once the validation session completes, the metrics will be displayed like the following figure.

<figure markdown="span">
![Validation Metrics](assets/workflows/sample-validation-metrics.jpg){ align=center }
<figcaption>Validation Metrics</figcaption>
</figure>

## 7. Deploy the Model

TBA.

[login]: #