# Tutorial 1: Detection and Segmentation of Measurement tapes

This tutorial shows step by step the whole Machine Learning process on Edgefirst Studio. The tutorial is split in the following sections:

* [Data Collection](#data-collection)
* [Data Annotation using AGTG](#data-annotation-using-agtg)
* [Model Training](#model-training)
* [Model Inference on PC](#model-inference-on-pc)

## Data Collection

Data collection process starts as simple as collecting pictures and videos of the objects. 

![Data Collection](assets/measurement_tap/data_collection.png)

The image above shows measurement tape images captured from different angles and positions using an iPhone 15. We recorded both images and videos with varying camera orientations to ensure diverse perspectives.

To create a dataset in EdgeFirst Studio, navigate to the Tutorials project and click the `Create New` button. Name the dataset "MeasurementTape" and add a single label: `tape`. You can keep the default `Annotations Set Name` or modify it as needed. Adding a description will be useful when accessing the dataset through the `edgefirst-client` API.

![Create New Dataset Dialog](assets/measurement_tap/create_new_dataset.png)

Once the dataset is created, click the menu in the top-right corner of the dataset card to import data from your PC or smartphone.

![Import Dataset Menu](assets/measurement_tap/import_dataset.png)

In the Import Dialog, you can choose between importing an Images Folder or Video. For images, you can drag and drop multiple files at once. For videos, you can only import one at a time and set the FPS (Frames per Second) ratio.

![Import Dialog](assets/measurement_tap/import_dialow.png)

After importing, check the gallery view to verify that all data (videos and images) has been imported successfully.

![Dataset Galery](assets/measurement_tap/dataset_view.png)

Note that videos appear as sequences with a play button overlay on the preview.

!!! info
    We recommend using videos rather than individual images. This is because AGTG leverages tracking information, allowing you to annotate just a single frame. With individual images, you'll need to annotate each one separately.


## Data Annotation using AGTG

Once the dataset is loaded, you can start the AGTG server from the gallery view. Select any dataset instance (image or video) from the gallery view to automatically enter editing mode.

![AGTG Start Server](assets/measurement_tap/start_agtg_server.png)

Click the AI-assisted button on the left side of the GUI to open the AGTG Manager View. On first use, you'll see an empty server list. Click the LAUNCH AGTG SERVER button and wait a few minutes for the server to initialize.

![AGTG Ready](assets/measurement_tap/agtg_ready.png)

The annotation process is straightforward. For each video, you'll need to initialize the state and begin annotating. You can use multiple prompts per object (Boxes, Points). Each object must be annotated independently so the tracker can assign a unique ID. Use the **`(+)`** button to add more objects. In the example below, we used box prompts. Click the **`SAVE PENDING ANNOTATIONS`** button to save your work. Continue this process until you've annotated the entire dataset.

You can also annotate in reverse mode by starting with the last occurrence of an object and tracking backwards.

![AGTG annotations](assets/measurement_tap/agtg_annotate.png)

!!! info
    The first object in each sequence may take a few seconds to initialize, which is normal.

After completing the annotations, the gallery will display previews of all annotated videos and images.

![Annotations Preview](assets/measurement_tap/gallery_full_annotations_view.png)

You are now ready to begin model training.


## Model Training

Different to many Machine Learning frameworks, to train a model on Edgefirst studio is very trivial. The first step is to make sure the dataset contains the training and validation groups. In case the GUI shows 0 Grops the user should create them before start training. The **`(+)`** button on the groups section will randomly shuffle the data and create the groups.

![Create Groups](assets/measurement_tap/create_dataset_groups.png)

Witht he grops already being created the user can select a training session for ModelPack under Model Experiments menu.

![Model Experiments](assets/measurement_tap/model_experiments.png)

Then create a **`New Experiment`** and call it *Measurement Tape Tutorial*

![New Experiment](assets/measurement_tap/new_experiment_creation.png)

After creating the experiment a new preview will be created on the GUI showing some stats about the experiments made on this dataset (At creation time everything is empty).

![Experiment Card](assets/measurement_tap/expriment_card.png)

You can select the experiment and create a new instance of ModelPack now by clicking the training section on the preview card. By Clicking in the **`NEW SESSION`** button you can configure ModelPack parameters. It is mandatory to select a dataset as well as to provide a descriptive name. Also, remember to check segmentation to make the model able to train on both tasks. It is recommended to change the input resolution to be 640x360 to maximize the detection rate on samll datasets. Once the GUI is configure click **`START SESSION`** and waith few minutes until the model completes training and quantization process.

![New ModelPack training session](assets/measurement_tap/new_modelpack_training_session.png)

Now that everything has started, we just need to wait until the model finishes the process and the status changes from `Running` to `Complete`

![Status Training](assets/measurement_tap/training_status.png)

## Model Inference on PC 
