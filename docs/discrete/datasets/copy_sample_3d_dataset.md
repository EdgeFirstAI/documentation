# Copy Sample Dataset

This page will show you how to copy a dataset from "Sample Project" in {{ studio_link("EdgeFirst Studio") }}.  You will be using this dataset to train your model.  In the following examples, you will be copying the "Raivin Ultra-Short 2025.03" dataset.

!!! note "Have you created a project?"
    It is important that you have followed through the [Getting Started](../../index.md) which shows you how to {{ studio_link("sign up", "signup") }}, {{ studio_link("login", "login") }}, and [create a project](../../getting_started/create_project.md) in EdgeFirst Studio which is crucial before starting any experiments.

Once you have your own project created, you can finally copy a dataset inside your project.  In this example, the project that was created is called "My First Project".

{{ figure("/studio/assets/projects/new-project.jpg", "New Project") }}

Under "Sample Project", click on the "Datasets" button.

{{ figure("/studio/assets/projects/sample-datasets-button.jpg", "Sample Datasets Button") }}

Inside "Sample Project", you will find a sample dataset called "Raivin Ultra-Short 2025.03".  You will be copying this dataset to train a Fusion model for people detection.

## Copy Dataset

{% include-markdown "discrete/datasets/copy_3d_dataset.md" heading-offset=0 %}

## Tag Dataset

{% include-markdown "discrete/datasets/tag_3d_dataset.md" heading-offset=0 %}

Once you have copied and tagged the dataset, you can now begin training your model.
