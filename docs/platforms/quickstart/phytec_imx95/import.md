# Import Videos and Images into EdgeFirst Studio

Now that you have captured videos or images for your dataset, let's import the files into EdgeFirst Studio. If you haven't already signed up to {{ studio_link("sign up", "signup") }}, please follow the [Getting Started](../../../index.md) guide to sign up.

## Create a Project

Let’s start by creating a project in EdgeFirst Studio. A project is needed when starting a new experiment since it is treated as the top level directory that contains your datasets, annotations, and trained model artifacts of your experiment.

{% include-markdown "discrete/studio/create_project.md" %}

## Import Videos into EdgeFirst Studio

{% include-markdown "discrete/datasets/import_videos.md" %}

## Import Images into EdgeFirst Studio

{% include-markdown "discrete/datasets/import_images.md" %}

## Next Steps

Now that you have imported your videos or images into EdgeFirst Studio, let's take a look at how to [annotate the dataset](annotate.md) which can then be used to train a detection model based on the annotated objects.
