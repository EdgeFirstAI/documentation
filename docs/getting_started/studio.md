# EdgeFirst Studio: Overview

This page will describe the structure and layout of EdgeFirst Studio.  The elements and sub-elements of any given project is based on an hierarchical structure that will be described in detail below. 

This page breaks down important concepts used in EdgeFirst Studio, namely:

- *projects*: high-level collections of sensor datasets, model experiments, and other automation and management tasks associated with the dataset inputs and model outputs.  
- *datasets*: a collection of sensor data, such as images, videos, radar cubes, etc. logically grouped together by the user. Usually, each dataset contained within a project will come from a single recording session.
- *model experiments*: high-level collections of training and validation sessions.
- *training sessions*: the functionality to convert datasets recorded into vision- and radar-based models that can be deployed back to the edge platforms/devices.
- *validation sessions*: the functionality to take a model and determine its accuracy against other models or a standardized validation dataset to see if it is ready for deployment.

## Project Structure

As you saw from the [initial steps](../index.md#initial-steps), when you first login, you will be greeted by the "Projects" page which contains a sample project called "Sample Project". 

To return to this splash page from any other page, you can:

* click your browser's "Back" button until back here.
* click the Apps ![Apps Button](../assets/apps_button.png) waffle button and select the "Projects" menu item.
* click on the "Au-Zone" Home button in the top-left corner.

The following figure describes the UI elements of the "Project" card.  Take special note of the project attributes (datasets, auditing tasks, etc.) as these are the buttons that lead into further parts of the project. The "Sample Project" project has three datasets, zero auditing tasks, and four model experiments associated with it.

<figure markdown="span">
![Project Attributes](../studio/assets/project-attributes.jpg){ align=center }
<figcaption>Project UI Breakdown</figcaption>
</figure>

A project will contain datasets and model experiments. A model experiment will contain training and validation sessions. The project structure hierarchy is shown below.

<div style="text-align: center;">
    ```mermaid
    ---
    title: Project Hierarchy
    ---
    graph TD
    project[Project] --> datasets[Datasets]
    datasets --> audit[Auditing Tasks]
    project --> model[Model Experiments]
    model --> train[Training Sessions]
    train --> validation[Validation Sessions]
    ```
</div>

This hierarchy describes the span of deletion of the project attributes. When a project is deleted, all elements in the project including datasets and model experiments will be deleted. When a dataset is deleted, only its child element such as auditing tasks will be deleted. When a model experiment is deleted, only its child elements will be deleted such as training and validation sessions.

### Datasets

From the "Projects" page, we can click on the "Datasets" ![Dataset Button](../assets/datasets_button.png) button to see the three datasets associated with this project: "COCO", "Ravin Ultra Short 2025.03", and "CARDS".  These public datasets are readily available for user onboarding and trials, but these datasets are **READ-ONLY** datasets. By default, users can [view the datasets](../datasets/tutorials.md#viewing-datasets). Otherwise, in order to have full access to the dataset, users **MUST** [copy the dataset](../datasets/tutorials.md#copying-datasets) into the project they've created. 

<figure markdown="span">
![Public Datasets](assets/public-datasets.jpg){ align=center }
<figcaption>Public Datasets</figcaption>
</figure>

The "Raivin Ultra Short 2025.03" dataset contains 3D bounding box annotations which are used only for [training Fusion models](../models/fusion/training.md). The "COCO" and "CARDS" dataset contains 2D bounding box annotations which are only valid for [training Vision models](../models/modelpack/training.md).

The following figure breaks down the elements of a "Dataset" card.

<figure markdown="span">
![Dataset Attributes](../studio/assets/datasets/dataset-attributes.jpg){ align=center }
<figcaption>Dataset Card UI Breakdown</figcaption>
</figure>

For an in-depth tutorial for managing datasets in EdgeFirst Studio from capture and annotation to export and deployment, see our [Dataset Tutorials](../datasets/tutorials.md).

### Model Experiments

#### Training Sessions

Training sessions take in datasets and synthesize from them new AI models -- for object recognition (vision) or object perception (fusion).

From the "Projects" page, we can click on the "Trainers" ![Trainers Button](../assets/trainers_button.png) button to see the training experiments in the project.

The sample project will contain completed training sessions using the public datasets provided. The training session shown below is based on training a Vision model from the public dataset *COCO*.

<figure markdown="span">
![Sample Training Session](assets/training-session.jpg){ align=center }
<figcaption>Sample Training Session</figcaption>
</figure>

The following figure describes the attributes of any given training session.

<figure markdown="span">
![Training Session Attributes](../models/assets/training/training-session-attributes.jpg){ align=center }
<figcaption>Training Session Attributes</figcaption>
</figure>

For more details regarding deploying training sessions, please see 
[Training ModelPack](../models/modelpack/training.md) for training Vision models and 
[Training Fusion](../models/fusion/training.md) for training Fusion models.

#### Validation Sessions

The sample project will contain completed validation sessions using the models trained in the training sessions. The validation session shown below is based on the training session from training a Vision model using the dataset *COCO*.

<figure markdown="span">
![Sample Validation Session](assets/validation-session.jpg){ align=center }
<figcaption>Sample Validation Session</figcaption>
</figure>

The following figure describes the attributes of any given validation session.

<figure markdown="span">
![Validation Session Attributes](../models/assets/validation/validation-session-attributes.jpg){ align=center }
<figcaption>Validation Session Attributes</figcaption>
</figure>

For more details regarding deploying validation sessions, please see 
[Validating ModelPack](../models/modelpack/validation.md) for validating Vision models and 
[Validating Fusion](../models/fusion/validation.md) for validating Fusion models.

## Next Steps

Now that you are familiar with the layout of EdgeFirst Studio including the element definitions and it's hierarchy, checkout our end-to-end [User Workflows](workflows/index.md) to start experimenting with data capture, model training, and model deployment. 

It is recommended for new users to visit the following tutorials to be familiar with the layout and features that EdgeFirst Studio offers.

* [Navigating EdgeFirst Studio](../studio/navigation.md)
* [Project Dashboard](../studio/projects.md)
* [Dataset Dashboard](../studio/datasets/index.md)
