# On Target Validation

This tutorial walks through how to run validation on target using EdgeFirst Studio. In this setup, validation is executed as a **user-managed validation session**, where the model is deployed directly on an embedded platform.  This approach provides an accurate assessment of real-world performance, including latency and resource usage on the target device.

In this tutorial, you will validate a **Vision** model trained using either the [end-to-end workflows](../../../getting_started/workflows/index.md) or the [Training Vision](../../training/vision.md) guide.  Note that a Vision model detects objects in camera frames or images.  If you are working with Fusion models, refer to [Validating Fusion Models](../fusion/managed.md).

Alternatively, EdgeFirst Studio also supports **On-Cloud Validation**, which runs as a managed validation session.  In this mode, an EC2 instance is provisioned to host and validate the model remotely. For more details, see [On Cloud Validation](managed.md).

!!! info "i.MX 95 Validation"
    To deploy TFLite models in the i.MX 95, first [convert the models using eIQ's Neutron Converter](../../ultralytics/neutron.md) prior to deploying the model in the platform.  This modifies the model's architecture to allow deployment using the device's Neutron NPU delegate.

{% include-markdown "discrete/models/create_validation_session.md" %}

You will be greeted with a validation session dialog.  In this dialog, select the "User Managed" option.  Next specify the name of the validation session, the model to validate, and the dataset to deploy.  In this example, the ONNX model will be validated and the "Coffee Cup" dataset with the validation partition will be used. Additional parameters are available on the right for user override. Otherwise the same parameters set in the training session will be used. For more information on these parameters hover over the info button ![Info Button](../../../assets/buttons/studio-info-button.jpg).

{{ figure("../../assets/validation/user-managed-vision-session-fields.jpg", "Validation Session Fields") }}

Once the configurations have been made, go ahead and click on the "Start Session" button on the bottom right of the window.  This will create the validation session to track validation progress that will run in the embedded platform.

The validation session card will appear like the following below.  Each session has a session ID.  Make a note of the session ID circled in red below.  In this case it is `v-1b51`.

{{ figure("../../assets/validation/user-managed-vision-session-id.jpg", "Validation Session ID") }}

## Session Progress

Once the validation session has been created, [SSH](../../../platforms/networking/ssh.md) into the platform and install the EdgeFirst Validator.

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

Next login to your account in EdgeFirst Studio by using [EdgeFirst Client](../../../perception/studio.md) which comes installed with the validator package. The command below will prompt you to enter your EdgeFirst Studio credentials.

```shell
edgefirst-client login
```

!!! note "Server Specification"
    Specify the EdgeFirst Studio server using `--server` among these variations: "test", "stage", "saas".  This is an optional parameter as the default is set to "saas".

!!! info "EdgeFirst Studio Token"
    Once logged in, an EdgeFirst Studio Token will be saved under `~/.config/edgefirststudio/token` granting access to the EdgeFirst Studio API which will remain valid for a period of time, usually 12 hours. Using this token will refresh the expiration timer.

Once the validator is installed and authenticated, run validation using the following command.  Replace the session ID specific to your session card.

```shell
edgefirst-validator --session-id v-1b51
```

!!! note
    Replace the session ID parameter specific to the validation session ID in your session.

If the model already exists in your system, you can run this command `edgefirst-validator /path/to/mymodel.onnx --session-id v-1b51`.  Otherwise, the model will be automatically downloaded from the EdgeFirst Studio training session.

Once entered, the following validation progress should now be indicated in EdgeFirst Studio as shown below.

{{ figure("../../assets/validation/user-managed-vision-session-progress.jpg", "Validation Session") }}

## Completed Session

The completed session will look as follows with the status set to "Complete".

{{ figure("../../assets/validation/user-managed-vision-completed-session.jpg", "Completed Session") }}

The attributes of the validation sessions in EdgeFirst Studio are labeled below.

{{ figure("../../assets/validation/validation-session-attributes.jpg", "Validation Session Attributes") }}

## Validation Metrics

Once the validation session completes, you can view the validation metrics by clicking the "view validation charts" button on the top of the session card.

{{ figure("../../assets/validation/vision-charts.jpg", "Validation Charts") }}

!!! info
    See [detection](../metrics/detection/index.md) and [segmentation](../metrics/segmentation.md) metrics for further details.

You can go back to the validation session card by pressing the "Back" button as indicated in red below on the top left corner of the page.

{{ figure("../../assets/validation/back-button.jpg", "Back to the Session Card") }}

## Comparing Metrics

It is also possible to compare validation metrics for multiple sessions.  See [Validation Sessions](../../../studio/models.md#validation-sessions) in the Model Experiments Dashboard.

## Next Steps

Now that you have validated your model, you can find examples for deploying your model in [EdgeFirst Studio](../../deployment/studio.md), [PC](../../deployment/pc/index.md), [Embedded Targets](../../deployment/launcher.md), the [Maivin](../../deployment/maivin.md), and the [Raivin](../../deployment/2d_raivin.md). 
