# Capture with a Phone

The examples below will show recording of a five second video and image captures of coffee cups using a phone for training a Vision model that detects coffee cups. However, you can choose any type of objects in your dataset.

{% include-markdown "discrete/datasets/recording_on_phone.md" heading-offset=2 %}

{% include-markdown "discrete/datasets/create_dataset_container.md" heading-offset=0 %}

{% include-markdown "discrete/datasets/uploading_video_to_studio.md" heading-offset=0 %}

{% include-markdown "discrete/datasets/uploading_images_to_studio.md" heading-offset=0 %}

Next [view the gallery of the dataset](../../datasets/tutorials/management.md#view-dataset) to confirm all the captured data has been uploaded.  You should see the imported video file and images in the gallery.  Note that videos appear as sequences with a play button overlay on the preview thumbnail.

<figure markdown="span">
![Coffee Cup Gallery](../../getting_started/assets/workflows/pc-dataset-gallery.jpg){ align=center }
<figcaption>Coffee Cup Gallery</figcaption>
</figure>

Once all the captured data has been uploaded to the dataset container, you will now assign groups to the data to split the data into training and validation sets.  Follow the [tutorial for creating groups](../../datasets/tutorials/management.md#split-dataset) with an 80% partition to training and 20% partition to validation.  The final outcome for the groups should look as follows.

<figure markdown="span">
![Dataset Groups](../../getting_started/assets/workflows/dataset-groups.jpg){ align=center }
<figcaption>Dataset Groups</figcaption>
</figure>

Now that you have imported captured images or videos into EdgeFirst Studio and have split the captured data into training and validation partitions, you can now start annotating your data as shown in the next section below.

# Annotate the Dataset

In this step, you will need a personal computer (PC) with access to Wifi to [log in][login] to EdgeFirst Studio for annotating the dataset.  When annotating the dataset, you will be using AI assistance to reduce the effort by running auto segmentation and bounding boxes on the objects in the frame.  Once logged in to EdgeFirst Studio, follow the [Auto Annotations](../../datasets/tutorials/annotations/automatic.md) instructions to auto-annotate the video sequence that was imported.  Otherwise, follow the [Manual 2D Annotations](../../datasets/tutorials/annotations/manual.md) instructions to annotate the images captured.

A complete annotation will have a segmentation mask and a bounding box for each object in the frame.  Shown below is an example. 

<figure markdown="span">
![Sample Annotation](../../getting_started/assets/workflows/sample-2d-annotation.jpg){ align=center }
<figcaption>Sample Annotation</figcaption>
</figure>

{% include-markdown "discrete/models/train_vision.md" heading-offset=0 %}

{% include-markdown "discrete/models/validate_vision.md" heading-offset=0 %}

# Deploy the Model

Once you have validated your trained model, let's take a look at an example of how this model can be deployed in your PC by following the tutorial [Deploying to the PC](../../models/modelpack/deployment/pc.md). 

If you have an NXP i.MX 8M Plus EVK you can also run your model directly on the device using the EdgeFirst Middleware by following the tutorial [Deploying to Embedded Targets](../../models/modelpack/deployment/evk.md).

!!! note

    Support for additional platforms beyond the NXP i.MX 8M Plus will be available soon.  Let us know which platform you'd like to see supported next!

If you have an [EdgeFirst Platform](../../platforms/index.md) such as the Maivin or Raivin then you can deploy and run the model using the bundled EdgeFirst Middleware by following the tutorial [Deploying to EdgeFirst Platforms](../../models/modelpack/deployment/maivin.md).
