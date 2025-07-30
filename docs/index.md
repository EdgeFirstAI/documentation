# Getting Started

Welcome to EdgeFirst Studio!  Follow this Quickstart for user onboarding from start to finish.

{% include-markdown "discrete/user/signup.md" %}

{% include-markdown "discrete/user/login.md" %}

{% include-markdown "discrete/studio/create_project.md" %}

The next sections will invite you to follow along the end-to-end workflow for recording a video or capturing images using a phone and then upload the captured data into EdgeFirst Studio for annotation and then model training, validation, and deployment on various platforms. 

!!! info "Workflows"
    The workflow below is based on the *Web-Based Workflow* which requires only a phone and a PC.  There are other [workflows](getting_started/workflows/index.md) that support different hardware requirements. 

## Capture with a Phone

The examples below will show recording of a five second video and image captures of coffee cups using a phone for training a Vision model that detects coffee cups. However, you can choose any type of objects in your dataset.

{% include-markdown "discrete/datasets/recording_on_phone.md" heading-offset=2 %}

{% include-markdown "discrete/datasets/create_dataset_container.md" %}

{% include-markdown "discrete/datasets/uploading_video_to_studio.md" %}

{% include-markdown "discrete/datasets/uploading_images_to_studio.md" %}

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

In this step, you will need a personal computer (PC) with access to Wifi to [log in][login] to EdgeFirst Studio for annotating the dataset.  When annotating the dataset, you will be using AI assistance to reduce the effort by running auto segmentation and bounding boxes on the objects in the frame.  Once logged in to EdgeFirst Studio, follow the [Auto Annotations](datasets/tutorials/annotations/automatic.md) instructions to auto-annotate the video sequence that was imported.  Otherwise, follow the [Manual 2D Annotations](datasets/tutorials/annotations/manual.md) instructions to annotate the images captured.

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

In this Quickstart guide, you have created your EdgeFirst Studio Account, logged in to EdgeFirst Studio, and created your very first project and ran your first experiment by capturing images and videos, annotating datasets, training a Vision model, validating the trained model, and deploying the model back into the PC, EdgeFirst Platform, or the i.MX 8M Plus EVK. 

## Next Steps

For these next steps, it is recommended to be familiar in [navigating EdgeFirst Studio](studio/navigation.md).  Next, users are invited to follow along other various [User Workflows](getting_started/workflows/index.md) that are tailored towards various hardware requirements and resources available to the user.

!!! tip "Need Help?"
    📬 Have questions or ran into an issue?  
    Feel free to [email our support team](mailto:support@edgefirst.ai) — we’re here to help!
