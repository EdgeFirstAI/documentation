# Split Dataset

Partitioning the dataset is crucial in reserving dataset portions used for training and portions used for validation to assess the performance of the model.  In EdgeFirst Studio, the partitions are 80% towards training and 20% towards validation.  This operation randomly shuffles the data prior to assigning them to the specified groups.

!!! warning
    The dataset needs to be re-split whenever new sample images or frames are added to the dataset.  Newly added samples are not automatically added to any group that already exists.

Consider the following dataset without any groups reserved.

<figure markdown="span">
![No Groups](../../datasets/assets/management/dataset-no-groups.jpg){ align=center }
<figcaption>No Groups</figcaption>
</figure>

To create the dataset groups, click on the "+" button in the "Groups" field.

<figure markdown="span">
![Add Groups](../../datasets/assets/management/add-groups-button.jpg){ align=center }
<figcaption>Add Groups</figcaption>
</figure>

This will open a new dialog to specify the percentages of the partition belonging to the "Training" group or "Validation" group. By default 80% of the samples will be dedicated to training and 20% remaining will be dedicated towards the validation samples.

<figure markdown="span">
![Groups Field](../../datasets/assets/management/groups-field.jpg){ align=center }
<figcaption>Groups Field</figcaption>
</figure>

Once the groups are specified, click "Split" to create the groups.  This will automatically divide the samples in the dataset based on the percentages of each group specified.

<figure markdown="span">
![Dataset Groups](../../datasets/assets/management/dataset-with-groups.jpg){ align=center }
<figcaption>Dataset Groups</figcaption>
</figure>
