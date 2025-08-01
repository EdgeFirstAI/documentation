# Dataset Import

This page will provide tutorials for importing annotated datasets with various formats in EdgeFirst Studio.  

## Import Darknet Datasets

This tutorial will show how to import a Darknet dataset such as [COCO128](https://www.kaggle.com/datasets/ultralytics/coco128) into EdgeFirst Studio.

To import a dataset, first [create a dataset](management.md#create-dataset) container in EdgeFirst Studio. The following dataset is created with the name set to "COCO128" and the description as "Demo import".  Furthermore, an annotation set has also been created called "annotations".

<figure markdown="span">
![COCO128 Dataset Container](../assets/import/coco128-container.jpg){ align=center }
<figcaption>COCO128 Dataset Container</figcaption>
</figure>

For an example dataset, [COCO128](https://www.kaggle.com/datasets/ultralytics/coco128?resource=download) was downloaded using the link provided.  This will download a ZIP archive which can then be extracted into a "coco128" directory which contains "images" and "labels" subdirectories.

<figure markdown="span">
![COCO128](../assets/import/coco128-directories.jpg){ align=center }
<figcaption>COCO128</figcaption>
</figure>

Once a container has been created, open the dataset context menu denoted by the three vertical dots on the top right corner of the dataset card.

<figure markdown="span">
![Dataset Options](../assets/import/coco128-options.jpg){ align=center }
<figcaption>Dataset Options</figcaption>
</figure>

Select "Import".

<figure markdown="span">
![Import Option](../assets/import/coco128-import-option.jpg){ align=center }
<figcaption>Import Option</figcaption>
</figure>

This will popup a new window for you to specify the dataset to be imported.  In these options, select the "Import Type" to be "Darknet Dataset".  Specify the dataset folder "coco128" to be imported.  Specify the annotation set to the "annotations" annotation set.  The following figure shows the specifications.

<figure markdown="span">
![Import Options](../assets/import/coco128-import-options.jpg){ align=center }
<figcaption>Import Options</figcaption>
</figure>

Select "Start Import" at the bottom right to start the import process.

<figure markdown="span">
![Start Import](../assets/import/coco128-start-import.jpg){ align=center }
<figcaption>Start Import</figcaption>
</figure>

This will start the import process as shown.

<figure markdown="span">
![Import Process](../assets/import/coco128-import-process.jpg){ align=center }
<figcaption>Import Process</figcaption>
</figure>

Once completed, the dataset container will now contain 128 images from COCO and 
the annotations stored in the "annotations" container.

<figure markdown="span">
![Imported COCO128 Dataset](../assets/import/coco128-imported.jpg){ align=center }
<figcaption>Imported COCO128 Dataset</figcaption>
</figure>

See the dataset and its annotations by following the tutorial for [viewing the dataset gallery](management.md#view-dataset).

## Import EdgeFirst Datasets

This tutorial will show how to import an [EdgeFirst Dataset](../format.md) into EdgeFirst Studio. This tutorial will show importing a dataset such as COCO2017 that is structured as an EdgeFirst Dataset as shown below.

<figure markdown="span">
![COCO2017 EdgeFirst Dataset](../assets/import/edgefirst-dataset-coco.jpg){ align=center }
<figcaption>COCO2017 EdgeFirst Dataset</figcaption>
</figure>

To import a dataset, first [create a dataset](management.md#create-dataset) container in EdgeFirst Studio. The following dataset is created with the name set to "COCO2017" and the description as "Demo Import".  Furthermore, an annotation set has also been created called "annotations".

<figure markdown="span">
![COCO2017 Dataset Container](../assets/import/coco2017-container.jpg){ align=center }
<figcaption>COCO2017 Dataset Container</figcaption>
</figure>

Once a container has been created, open the dataset context menu denoted by the three vertical dots on the top right corner of the dataset card.

<figure markdown="span">
![Dataset Options](../assets/import/coco2017-options.jpg){ align=center }
<figcaption>Dataset Options</figcaption>
</figure>

Select "Import".

<figure markdown="span">
![Import Option](../assets/import/coco2017-import-option.jpg){ align=center }
<figcaption>Import Option</figcaption>
</figure>

This will popup a new window for you to specify the dataset to be imported.  In these options, select the "Import Type" to be "EdgeFirst Dataset".  Specify the Zip and Arrow file in your machine to be imported.  Specify the annotation set to the "annotations" annotation set to store the dataset annotations.  The following figure shows the specifications.

<figure markdown="span">
![Import Options](../assets/import/coco2017-import-options.jpg){ align=center }
<figcaption>Import Options</figcaption>
</figure>

Select "Start Import" at the bottom right to start the import process.

<figure markdown="span">
![Start Import](../assets/import/coco2017-start-import.jpg){ align=center }
<figcaption>Start Import</figcaption>
</figure>

This will start the import process as shown.

<figure markdown="span">
![Import Process](../assets/import/coco2017-import-process.jpg){ align=center }
<figcaption>Import Process</figcaption>
</figure>

See the dataset and its annotations by following the tutorial for [viewing the dataset gallery](management.md#view-dataset).

## Next Steps

Now that you have seen how to import datasets in EdgeFirst Studio, see how the [annotations](annotations/index.md) are being managed in EdgeFirst Studio.
