# Dataset Dashboard

The Dataset Dashboard shows a list of datasets in a project with a dataset summary in each dataset card.  For an in depth tutorial for creating datasets from capture to annotation, see the [Dataset Tutorials](../../datasets/tutorials/index.md). From the "Projects" page, we can click on the "Datasets" ![Dataset Button](../../assets/buttons/studio-datasets-button.jpg) button on the project card to see the project's datasets.  The public project "Sample Project" will contain the following datasets.

{{ figure("../assets/datasets/public-datasets.jpg", "Public Datasets") }}

Public datasets are readily available for user onboarding and trials, but these datasets are **READ-ONLY** datasets.  By default, users can [view the datasets](../../datasets/tutorials/management.md#view-dataset).  Otherwise, in order to have full access to the dataset, users **MUST** [copy the dataset](../../datasets/tutorials/management.md#copy-dataset) into the project they've created.

The dataset attributes are shown below.

{{ figure("../assets/datasets/dataset-attributes.jpg", "Dataset Attributes") }}

For datasets with **WRITE** access, the context menu will be shown like the following.

{{ figure("../assets/datasets/write-access-dataset-context-menu.jpg", "Dataset Write Access Context Menu") }}

This gives the user the options for [editing the dataset info](../../datasets/tutorials/management.md#edit-dataset-information), [importing existing datasets](../../datasets/tutorials/import.md), [exporting datasets into your local machine](../../datasets/tutorials/management.md#export-dataset), [creating snapshots](../snapshots.md#create-snapshot), and [copying datasets](../../datasets/tutorials/management.md#copy-dataset).  The rest of the options are described in the sections below such as the [dataset analytics](#analytics), [view on map](#view-on-map), [dataset history](#dataset-history), and [removing datasets](#remove-dataset).

## Labels

Click on labels (i) icon to open the dialog to edit labels.

{{ figure("../assets/datasets/edit-label.png", "Editing Labels") }}

The edit dialog allows to:

- Add Label (class).
- Change the color of the label.
- Change the order of the labels by changing its index.
- Delete a label.
- Change the name of a label.

Tutorials for these operations can be found under the [Dataset Annotations](../../datasets/tutorials/annotations/index.md#dataset-labels) section.

## Groups

- Groups splits the images into training and validation images
- One image can be associated with zero or only one group at a time
- Use the slider to adjust percentages for each group.
- If "Only non-grouped images" is unchecked, all images will be shuffled and assigned new groups.

The following image shows a dialog to split non-grouped images into 2 groups, *Training* and *Validation*

{{ figure("../assets/datasets/assign-groups.png", "Assigning Groups") }}

The tutorial for splitting the images in the dataset into groups can be found under the [Dataset Management](../../datasets/tutorials/management.md#split-dataset) section.

## Dataset Extended Menu

Click on the three dots on dataset card to open the extended menu.

{{ figure("../assets/datasets/dataset-menus.png", "Extended Dataset Menu") }}

### Edit Info

Change the name or description of the dataset as shown in [editing dataset information](../../datasets/tutorials/management.md#edit-dataset-information).

### Import Dataset

There are several import types available.

{{ figure("../assets/datasets/import-datasets.png", "Importing Datasets") }}

To import datasets proceed with the steps as follows or follow this in-depth tutorial for [importing datasets](../../datasets/tutorials/import.md).

1. Select an import type.  The [EdgeFirst Dataset Format](../../datasets/format/index.md) is the proprietary format used by many operations in EdgeFirst Studio.
2. Create an annotation set where annotations are to be imported.  If only images are imported, then this step is not required.
3. Drag and drop a folder or group of files.
4. Select an annotation set if the annotation type allows annotation import.
5. Click "START IMPORT".
6. Import will start in the background and the status is shown in the task progress popup.

{{ figure("../assets/datasets/import-taskbar.png", "Taskbar") }}

!!! warning "Termination of Background Processes"
    Although the import process is running in the background, closing the web browser or the tab will terminate all uploads in the *Local* tab of the task dialog. Moving to other pages in the studio is still fine.

### Export Dataset

The "Export Dataset" downloads the data from EdgeFirst Studio to the local folder in your PC.

{{ figure("../assets/datasets/export-dataset.png", "Export Dataset") }}

To export datasets proceed with the steps as follows or follow this in-depth tutorial for [exporting datasets](../../datasets/tutorials/management.md#export-dataset).

1. Select the dataset type: Detection (Bounding boxes) or Segmentation (Masks).
2. Select the export format.
3. Select the annotation set to be exported if required.
4. Select Mode:
    - Dataset - Exports images and annotations. Exports a zip file in the downloads folder.
    - Annotations Only - Exports only the annotations. Exports a zip file in the downloads folder.
    - Image URLS only - Useful for larger datasets. Exports a file with image urls in the downloads folder.

!!! tip "Large Datasets"
    For datasets larger than 10000 images, export image URLS and annotations separately and then use a script to download images.

### Copy Dataset

{{ figure("../../datasets/assets/management/copy-dataset-options.jpg", "Copying Datasets") }}

To copy datasets proceed with the steps as follows or follow this in-depth tutorial for [copying datasets](../../datasets/tutorials/management.md#copy-dataset).

1. Open the dataset extended menu.
2. Select "Copy Dataset".
3. Source project, dataset, and annotation set (if applicable) are auto-filled, but you can select a different source if required.
4. Destination project is selected by default. If *New Dataset (Dataset name)* is selected, a new dataset along with any annotation set from source will be created in the destination project. Otherwise, you can choose a dataset and an annotation set as destination.
5. Optionally select *Copy Selected Annotation Types Only* to only copy annotations and files that match the checked types.
6. Select filters if required. Please refer to [Gallery Filters](gallery.md#filters) for more information.  

### Analytics

Click on Analytics to see more statistical information about the dataset.

{{ figure("../assets/datasets/analytics.png", "Dataset Analytics") }}

### View on Map

When importing a dataset, the GPS location can be imported in the two following ways:

1. GPS location in the image EXIF.
2. GPS location as an annotation type.

If GPS location is present, then the annotation can be viewed on the map by using the "View on Map" option.

{{ figure("../assets/datasets/dataset-maps.png", "Dataset Maps") }}

### Dataset History

The dataset history introduces versioning for the dataset.  This allows any changes made to the dataset to be tracked via the "Changelog" section and allows the user to restore the state of the dataset with a known version, delete a dataset version, or add a new dataset version for the current state of the dataset.

{{ figure("../assets/datasets/dataset-history.jpg", "Dataset History") }}

### Remove Dataset

To delete a dataset, click "Move to Recycle Bin".  This moves the dataset and all of its contents to the Recycle Bin.

!!! info
    The deleted dataset goes to the recycle bin that can be restored.  The storage used by the dataset is only released when the dataset is purged from the recycle bin.

## Next Steps

This page has described the features and context of the dataset card.  Proceed to the next sections to learn more about the [Dataset Gallery](gallery.md) and [Annotation Sets](annotations.md).
