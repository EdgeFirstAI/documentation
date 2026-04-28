# Validate Vision Model

Now that you have trained a model, you can validate the model's performance on target by following the instructions on this page.

If you haven't already, click on the training session card for more information.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

On the top right corner of the page, click on the "validate" button as indicated.

{{ figure("/models/assets/validation/training_validate_button.jpg", "Validate Button") }}

Select the "User Managed" option. Specify the name of the validation session and the model and the dataset for validation.  The rest of the settings were kept as defaults.  Click "Start Session" at the bottom to start the validation session.

{{ figure("/models/assets/validation/user-managed-vision-session-fields.jpg", "Start Validation Session") }}

The validation session card will appear like the following below.  Each session has a session ID.  Make a note of the session ID circled in red below.  In this case it is `v-1b51`.

{{ figure("/models/assets/validation/user-managed-vision-session-id.jpg", "Validation Session ID") }}

Once the validation session has been created, [SSH](../../platforms/networking/ssh.md) into the platform and install the following dependencies.

!!! warning "Virtual Environment"
    If you don't have a virtual environment already setup, please follow these steps below.
    
    To avoid re-installation of existing system packages, we recommend setting up a [Python virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) prior to running the pip installations below.  Append `--system-site-packages` when creating the environment to include existing packages in the system.  For example:

    * Linux `python3 -m venv /path/to/myenv --system-site-packages`
    * Windows `python -m venv /path/to/myenv --system-site-packages`

    Activate the environment via:

    * Linux: `source /path/to/myenv/bin/activate`
    * Windows: `/path/to/myenv/Scripts/activate`

```shell
$ pip install edgefirst-validator
```

Next login to your account in EdgeFirst Studio by using the [EdgeFirst Client](../../perception/studio.md) which comes installed with the validator package. The command below will prompt you to enter your EdgeFirst Studio credentials.

```shell
$ edgefirst-client login
```

Once the validator is installed and authenticated, run validation using the following command.  Replace the session ID specific to your session card.

```shell
$ edgefirst-validator --session-id v-1b51
```

If the model already exists in your system, you can run this command `edgefirst-validator /path/to/mymodel.tflite --session-id v-1b51`.  Otherwise, the model will be downloaded as an artifact from the EdgeFirst Studio training session.

Once entered, the following validation progress should now be indicated in EdgeFirst Studio as shown below.

{{ figure("/models/assets/validation/user-managed-vision-session-progress.jpg", "Validation Session") }}

The completed session will look as follows with the status set to "Complete".

{{ figure("/models/assets/validation/user-managed-vision-completed-session.jpg", "Completed Session") }}

Once the validation session completes, you can view the validation metrics by clicking the "view validation session charts" button at the top right of the session card.

{{ figure("/models/assets/validation/vision-charts.jpg", "Validation Charts") }}

Now that you have validated the performance of the model, you can move forward to deploying the model on target.
