# Project Dashboard

{{ figure("assets/projects/studio-from-scratch.jpg", "Starting Page") }}

The "Projects" page organizes data into logical project partitions.  When you first login, this page will already contain a project called "Sample Project".

To return to this page from any other page, you can click the Apps Menu ![Apps Button](../assets/buttons/studio_apps_button.png) waffle button and select the "Projects" menu item or click on the "Projects" button on the top navigation bar.

The following figure describes the UI elements of the "Project" card.  Take special note of the project attributes (datasets, auditing tasks, etc.) as these are the buttons that lead into further parts of the project.  Furthermore, the figure below describes "Sample Project" which is a **Read-Only** public project and therefore, the project context menu is unavailable.  For your own created projects, this option will be available.

{{ figure("assets/projects/project-attributes.jpg", "Project Attributes") }}

A project will contain datasets and model experiments.  A model experiment will contain training and validation sessions.  The project structure hierarchy is shown below.

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

This hierarchy describes the span of deletion of the project attributes.  When a project is deleted, all elements in the project including datasets and model experiments will be deleted.  When a dataset is deleted, only its child element such as auditing tasks will be deleted.  When a model experiment is deleted, only its child elements will be deleted such as training and validation sessions.

## Create Project

{% include-markdown "discrete/studio/create_project.md" %}

## Delete Project

1. Click on project contect menu (three vertically aligned dots) on the project card.
2. Click "Move to Recycle Bin".
2. The project is moved to the recycle bin.  Remove the project from the recycle bin to actually free the storage space.

## Edit Project

1. Click on project context menu (three vertically aligned dots) on the project card.
2. Click "Edit".
3. Change the name or description as desired.
4. Click "Apply Changes".

## Project Access Control

Project access control allows project resources to be selectively available to different users.

For more information please visit [Access Control](user/organization.md#roles).

## Next Steps

Now that you are familiar with the Project Dashboard, learn more about the [Datasets Dashboard](datasets/index.md) next.
