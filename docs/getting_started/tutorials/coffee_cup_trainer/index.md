# Coffee Cup Trainer

## Introduction

The aim of this walkthrough is to capture video using mobile phone, upload to Edgefirst Studio, perform AI assisted annotation and train a coffee cup detection model.

## Basic Setup

1. Create a project if not already created. Refer to [Project Dashboard](../../../studio/project/create_project.md) for instructions on how to create and manage projects.
2. Add a dataset for uploading tha captured data. ([Dataset Dashboard](../../../studio/datasets/index.md)) 

## Data Capture

1. Using a cellphone capture videos of few types of coffee cups.   
2. Each video may be 30-60 seconds
3. Try to move the camera around the cup to capture it from different angles and distances
4. Upload the video to EdgeFirst Studio (EFS) - select a PFT of around 10 for uploading
    - Either use data connection on mobile to directly open EFS in a mobile browser and upload video to the dataset   
    - Or transfer the video file from mobile phone to a PC and upload it from there to EFS
    - Details of uploading video to EFS can be found [here](../../workflows/web.md#capture-with-a-phone).
5. Use the above process to upload all the captures videos 

## Dataset Annotation

1. in order to train a model, the dataset is annotated. 
2. The annotation type in this case are 2D bounding boxes identifying coffee cups
3. There a are two main methods of annotation, Manual Annotation and AI Assisted Annotations as described below:

### Manual Annotation

This method involves going to the editor page and drawing 2D boxes around coffee cups. For more information for using this method, please refer to ????

### AI Assisted Annotation

## Dataset Partitioning

In this step, the dataset is partitioned into train (training) and val (validation) groups. It is recommended to use the default partitioning of 80% train and 20% val. 

If more information is required please refer to [Dataset Groups](../../../studio/datasets/index.md#groups) 

This method involves activating the AGTG server to assist in annotation. This method greatly reduces the annotation time. This method is described in [Automatic Ground Truth Generation](../../../studio/agtg.md)

# Model Training

1. Go to the training page and create an experiment
2. In this experiment create a new training session
    a. Select Modelpack 
    b. Select the dataset that was imported
    c. Select the annotation set that was created and annotated
    d. Select parameters  as required. However default parameters will work fine
3. On start training, a new training session will be started and its progress will be displayed
4. Once the training is complete, click on the training detail page and preview training charts amd metrics.

More info on training is available on [Model Training](../../../models/modelpack/training.md) 

# Validating Model

1. Open training details modal and start a validation session
2. Validation session will take some time to complete. Once completed, the validation results a re available to be examined.

More info on training is available on [Model Validation](../../../models/modelpack/validation/managed.md) 





In this tutorial, you have created your very first project and ran your first experiment by capturing images and videos, annotating datasets, training a Vision model, validating the trained model, and deploying the model back into the PC, EdgeFirst Platform, or the i.MX 8M Plus EVK.





