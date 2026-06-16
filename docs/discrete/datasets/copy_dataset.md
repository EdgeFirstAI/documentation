To copy a dataset, navigate to the dataset you would like to copy.  On the dataset card, select "Copy Dataset" from the dataset options as shown below.

{{ figure("/datasets/assets/management/copy-dataset-option.jpg", "Copy Dataset") }}

This action opens a dialog where you can specify the source and destination for the dataset copy operation.

* Source: The current location of the dataset being copied. This field is automatically populated with the dataset card you selected before opening the dialog.
* Destination: The location where the copied dataset will be created.

In the example below, the source is the "Coffee Cup" dataset in "Sample Project". The copied dataset will be created in the location specified by the destination fields.

By default, the copy operation creates a new dataset container in the selected destination project. Alternatively, you can [create a dataset container](../../datasets/tutorials/management.md#create-dataset) before starting the copy operation and then select that existing container as the destination.

Once you have made your selection, click "Apply" at the bottom right to start the copy process.

{{ figure("/datasets/assets/management/copy-dataset-options.jpg", "Copy Dataset Options") }}

You can navigate to the copied dataset by clicking the "Project" button and then clicking on the "Datasets" button on your project as shown below.

{{ figure("/datasets/assets/management/navigate-to-project.jpg", "Navigate to your Project") }}

The progress for the dataset copy will be shown on the dataset card.

{{ figure("/datasets/assets/management/copy-dataset-progress.jpg", "Copy Dataset Progress") }}

Once the copying process completes, the frames and the annotations would have been copied.

**Original Dataset** | **Copied Dataset**
:------------------:|:------------------:
![Original](../../datasets/assets/management/original-public-dataset.jpg) | ![Copied](../../datasets/assets/management/copied-dataset-result.jpg)
