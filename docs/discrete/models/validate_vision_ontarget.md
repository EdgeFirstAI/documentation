# Validate Vision Model

Now that you have trained a model, you can validate the model's performance on target by following the instructions on this page.

If you haven't already, click on the training session card for more information.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

On the top right corner of the page, click on the "validate" button as indicated.

{{ figure("/models/assets/validation/training_validate_button.jpg", "Validate Button") }}

Select the "User Managed" option. Specify the name of the validation session and the model and the dataset for validation.  *Under the model selection, you can select various trained model artifacts from the choices of ONNX, TFLite, TensorRT, Kinara, Hailo, etc.  Choose the model you plan to deploy on target.  The purpose of validation is to assess the model of whether or not it meets the performance requirements needed to be deployed on target.*  The rest of the settings were kept as defaults.  Click "Start Session" at the bottom to start the validation session.

{{ figure("/models/assets/validation/user-managed-vision-session-fields.jpg", "Start Validation Session") }}

The validation session card will appear like the following below.  Each session has a session ID.  Make a note of the session ID circled in red below.  In this case it is `v-1b51`.

{{ figure("/models/assets/validation/user-managed-vision-session-id.jpg", "Validation Session ID") }}

Once the validation session has been created, [SSH](../../platforms/networking/ssh.md) into the platform and install the [EdgeFirst Profiler](../../profiler/index.md).

!!! warning "Virtual Environment"
    If you do not have a virtual environment already set up, please follow these steps below.

    To avoid re-installation of existing system packages, we recommend setting up a [Python virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) prior to running the pip installations below.  Append `--system-site-packages` when creating the environment to include existing packages in the system.  For example:

    * Linux `python3 -m venv /path/to/myenv --system-site-packages`
    * Windows `python -m venv /path/to/myenv --system-site-packages`

    Activate the environment via:

    * Linux: `source /path/to/myenv/bin/activate`
    * Windows: `/path/to/myenv/Scripts/activate`

```shell
$ pip install edgefirst-profiler
```

See [Installation](../../profiler/installation/index.md) for platform installer alternatives and per-target dependencies.

Next sign in to EdgeFirst Studio. The profiler stores the credentials and refreshes them automatically while you are using it.

```shell
$ edgefirst-profiler login
```

Run validation against the session ID from the session card:

```shell
$ edgefirst-profiler validate --session-id v-1b51
```

The profiler downloads the model artifact and dataset partition, runs the pipeline on the target, and uploads the predictions and trace back to Studio when the run completes.

If the model already lives on disk and you want to skip the download, pass `--model` alongside the session ID:

```shell
$ edgefirst-profiler validate --session-id v-1b51 --model /path/to/mymodel.tflite
```

Once the run is underway, the session card in Studio updates with progress.

{{ figure("/models/assets/validation/user-managed-vision-session-progress.jpg", "EdgeFirst Studio — session card showing progress during a running validation") }}

The completed session will look as follows with the status set to "Complete".

{{ figure("/models/assets/validation/user-managed-vision-completed-session.jpg", "Completed Session") }}

Once the validation session completes, you can view the validation metrics by clicking the "view validation session charts" button at the top right of the session card.

{{ figure("/models/assets/validation/vision-charts.jpg", "Validation Charts") }}

Now that you have validated the performance of the model, you can move forward to deploying the model on target.
