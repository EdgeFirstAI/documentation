# On Target Validation

This tutorial will show the steps for running validation on target.  This type of validation is hosted as a user-managed validation session in EdgeFirst Studio.  A user-managed validation session is hosted in an embedded platform for a proper assessment of the model performance and timings when deployed on target.  In this tutorial, you will validate a **Vision** model that was trained through the [end-to-end workflows](../../../getting_started/workflows/index.md) or [Training Vision](../../training/vision.md).

Another type of validation is the [On Cloud Validation](managed.md) which is hosted as a managed validation session in EdgeFirst Studio.  A managed validation session creates an EC2 server to deploy the model for validation.

!!! info "i.MX 95 Validation"
    To deploy TFLite models in the i.MX 95, first [convert the models using eIQ's Neutron Converter](../../ultralytics/neutron.md) prior to deploying the model in the platform.  This modifies the model's architecture to allow deployment using the device's Neutron NPU delegate.

{% include-markdown "discrete/studio/create_mpk_validation_session.md" %}

You will be greeted with a validation session dialog.  In this dialog, check the "User Managed Validator" checkbox.  Next specify the name of the validation session, the model to validate, and the dataset to deploy.  In this example, the TFLite model will be validated and the "Coffee Cup" dataset with the validation partition will be used.  Next specify, the validation parameters on the right.  Additional information on these parameters are provided by hovering over the info button ![Info Button](../../../assets/buttons/studio-info-button.jpg).

<figure markdown="span">
![Validation Session Fields](../../assets/validation/user-managed-vision-session-fields.jpg){ align=center }
<figcaption>Validation Session Fields</figcaption>
</figure>

Once the configurations have been made, go ahead and click on the "Start Session" button on the bottom right of the window.  This will create the validation session to track validation progress that will run in the embedded platform.

The validation session card will appear like the following below.  Each session has a session ID.  Make a note of the session ID circled in red below.  In this case it is `v-c1f`.

<figure markdown="span">
![Validation Session ID](../../assets/validation/user-managed-vision-session-id.jpg){ align=center }
<figcaption>Validation Session ID</figcaption>
</figure>

## Session Progress

Once the validation session has been created, [SSH](../../../platforms/ssh.md) into the platform and install the following dependencies.

!!! warning "Virtual Environment"
    To avoid re-installation of existing system packages, we recommend setting up a [Python virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments)
    prior to running the pip installations below.  Append `--system-site-packages` when creating the environment to include existing packages in the system.  For example:

    * Linux `python3 -m venv /path/to/myvenv --system-site-packages`
    * Windows `python -m venv /path/to/myenv --system-site-packages`

    Activate the environment via:

    * Linux: `source /path/to/myenv/bin/activate`
    * Windows: `/path/to/myenv/Scripts/activate`

```shell
pip install edgefirst-validator
```

Next login to your account in EdgeFirst Studio by using the [EdgeFirst Client](../../../perception/studio.md) which comes installed with the validator package. The command below will prompt you to enter your EdgeFirst Studio credentials.

```
edgefirst-client login
```

!!! note "Server Specification"
    Specify the EdgeFirst Studio server using `--server` among these variations: "test", "stage", "saas".  This is an optional parameter as the default is set to "saas".  To modify the studio server, first `edgefirst-client logout` then `edgefirst-client --server <server> login`.

!!! info "EdgeFirst Studio Token"
    Once logged in, an EdgeFirst Studio Token will be saved under `~/.config/edgefirststudio/token` granting access to the EdgeFirst Studio API which will remain valid for a period of time, usually 12 hours. Using this token will refresh the expiration timer.

Once the validator is installed and authenticated, run validation using the following command.  Replace the session ID specific to your session card.

```shell
edgefirst-validator --session-id v-c1f
```

!!! note
    Replace the session ID parameter specific to the validation session ID in your session.

If the model already exists in your system, you can run this command `edgefirst-validator /path/to/mymodel.tflite --session-id v-c1f`.  Otherwise, the model will be downloaded as an artifact from the EdgeFirst Studio training session.

Once entered, the following validation progress should now be indicated in EdgeFirst Studio as shown below.

<figure markdown="span">
![Validation Session](../../assets/validation/user-managed-vision-session-progress.jpg){ align=center }
<figcaption>Validation Session</figcaption>
</figure>

## Completed Session

The completed session will look as follows with the status set to "Complete".

<figure markdown="span">
![Completed Session](../../assets/validation/user-managed-vision-completed-session.jpg){ align=center }
<figcaption>Completed Session</figcaption>
</figure>

The attributes of the validation sessions in EdgeFirst Studio are labeled below.

<figure markdown="span">
![Validation Session Attributes](../../assets/validation/validation-session-attributes.jpg){ align=center }
<figcaption>Validation Session Attributes</figcaption>
</figure>

## Validation Metrics

Once the validation session completes, you can view the validation metrics by clicking the "View Validation Charts" button on the top of the session card.

<figure markdown="span">
![Validation Charts](../../assets/validation/vision-charts.jpg){ align=center }
<figcaption>Validation Charts</figcaption>
</figure>

!!! info
    See [detection](../metrics/detection.md) and [segmentation](../metrics/segmentation.md) metrics for further details.

You can go back to the validation session card by pressing the "Back" button as indicated in red below on the top left corner of the page.

<figure markdown="span">
![Back to the Session Card](../../assets/validation/back-button.jpg){ align=center }
<figcaption>Back to the Session Card</figcaption>
</figure>

## Comparing Metrics

It is also possible to compare validation metrics for multiple sessions.  See [Validation Sessions](../../../studio/models.md#validation-sessions) in the Model Experiments Dashboard.

## Next Steps

Now that you have validated your Vision model, you can find examples for deploying your model in the [EVK](../../deployment/evk.md) or the [Maivin Platform](../../deployment/maivin.md).  Furthermore, you can also find examples for running your [ModelPack model](../../deployment/pc/mpk.md) or [Ultralytics model](../../deployment/pc/ultralytics.md) in your PC.
