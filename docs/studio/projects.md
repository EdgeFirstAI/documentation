# Project Dashboard

{{ figure("assets/projects/studio-from-scratch.jpg", "Starting Page") }}

The "Projects" page organizes data into logical project partitions.  A project is a high-level collections of sensor datasets, model experiments, and other automation and management tasks associated with the dataset inputs and model outputs.  When you first login, this page will already contain public projects called "Sample Project", "COCO Detection", "COCO Instance Segmentation".

To return to this page from any other page, you can click on the "Projects" button on the top navigation bar.

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

1. Click on project context menu (three vertically aligned dots) on the project card.
2. Click "Move to Recycle Bin".
2. The project is moved to the recycle bin.  Remove the project from the recycle bin to actually free the storage space.

## Edit Project

1. Click on project context menu (three vertically aligned dots) on the project card.
2. Click "Edit".
3. Change the name or description as desired.
4. Click "Apply Changes".

## Project Access Control

Project access control allows project resources to be selectively available to different users.

1. Click the project's extended menu shown as the three vertical dots in the top-right corner of the project card.
2. Click **Manage Access**.

{{ figure("assets/projects/access_control.jpg", "Project Access Control") }}

The **Manage Access** dialog lets you review the current visibility of the project and grant access to additional users. To add a user, click the icon highlighted in red.

{{ figure("assets/projects/project_access_control.jpg", "Project Access Control Modal") }}

Access Type:

1. **Organization**: Everyone in your organization has access to this project.
2. **Public**: Share this project with the EdgeFirst Studio community. By default, users outside your organization can read but not write to the project.
3. **Private**: Limit access to the project owner and organization admins.

Use the access control dialog to view and edit which users can access the selected project.

!!! note "Read-only projects"
    Public sample projects are read-only, so the extended menu and **Manage Access** option are only available on projects that your organization can modify.

## Next Steps

Now that you are familiar with the Project Dashboard, learn more about the [Datasets Dashboard](datasets/index.md) next.
