# Copy Sample Dataset

This page will show you how to copy a dataset from "Sample Project" in [EdgeFirst Studio][studio].  You will be using this dataset to train your model.  In the following examples, you will be copying the "Coffee Cup" dataset for faster training ~15 minutes.

!!! note "Have you created a project?"
    It is important that you have followed through the [Getting Started](../../index.md) which shows you how to [sign up][signup], [login][login], and [create a project](../../getting_started/create_project.md) in EdgeFirst Studio which is crucial before starting any experiments.

Once you have your own project created, you can finally copy a dataset inside your project.  In this example, the project that was created is called "My First Project".

{{ figure("/studio/assets/projects/new-project.jpg", "New Project") }}

Under "Sample Project", click on the "Datasets" button.

{{ figure("/studio/assets/projects/sample-datasets-button.jpg", "Sample Datasets Button") }}

Inside "Sample Project", you will find a sample dataset called "Coffee Cup".  You will be copying this dataset to train a Vision model for detecting coffee cups on images.

## Copy Dataset

{% include-markdown "discrete/datasets/copy_dataset.md" heading-offset=0 %}

## Tag Dataset

{% include-markdown "discrete/datasets/tag_dataset.md" heading-offset=0 %}

Once you have copied and tagged the dataset, you can now begin training your model.

[studio]: https://test.edgefirst.studio/
[signup]: https://test.edgefirst.studio/signup
[login]: https://test.edgefirst.studio/login
