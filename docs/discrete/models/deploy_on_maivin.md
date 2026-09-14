This guide will showcase two methods of deploying the model.

1. [Live View (Camera Page)](#live-view-camera-page): Displays the live camera feed with the model output overlaid.
2. [MCAP Recording](../../perception/data_collection/recording.md#record-mcap): Allows control of the recording options and provides download file options to replay the recording.

{% include-markdown "discrete/models/download_model.md" %}

## Visit the Web UI Service

Use your browser to connect to the Web UI of the remote device, enter the following URL `https://<hostname>/`.

!!! note
    Replace `<hostname>` with the hostname of your device.

You will be greeted with the Maivin [Web UI Main Page](../../platforms/quickstart/maivin/webui.md) page.

{{ figure("/platforms/assets/setup/ui-maivinMain.png", "Web UI Main Page") }}

For more information, please see the [Web UI Walkthrough](../../platforms/quickstart/maivin/webui.md).

## Update the Model Path

Next you will need to specify the path to the model in the device.  You can either update the model path in the Web UI or via the command line.

!!! note "Configure Model Settings"
    Whenever a new model has been updated, ensure that the [model settings](../../platforms/configuration/model.md) such as the score and the IoU thresholds are ideal for this model.

=== "via Web UI"

    Once you are in the Web UI main page, you can specify the path to the model by following the steps below.

    Click the settings icon on the top right corner of the page.

    {{ figure("/models/assets/deployment/raivin-settings.png", "Settings") }}

    Select "Model Settings".

    {{ figure("/models/assets/deployment/raivin-model-settings.png", "Model Settings") }}

    Configure the path to the model in your device as specified under "MODEL:", then click "Save Configuration" to save your changes.  The page reports when the model service has restarted with the new model.

    {{ figure("/models/assets/deployment/configure-model-path-maivin.png", "Model Path") }}

=== "via Command Line"

    To update the model path using the command line in the device, edit the following file using `sudo vi /etc/default/model`.

    Next, you will see the file with the following contents.

    ```ini
    # ---------------------------------------------------------------------------
    # Model Path
    # ---------------------------------------------------------------------------
    # Path to the inference model file (e.g., a .tflite model). This is required
    # and the service will not start without it.
    MODEL="/usr/share/edgefirst/modelzoo/yolov8n-det-int8-smart.tflite"
    ```

    Edit the `MODEL=` line to point to the specific path to your model, for example `MODEL="/home/torizon/mymodel.tflite"`.  To edit, press `i` to enter into "Insert Mode".  You should now be able to edit the lines.  To exit "Insert Mode", press the ESC key on your keyboard.  Next save and exit the file by typing `:wq` on your keyboard.  More examples for using `vi` can be found [here](https://coderwall.com/p/adv71w/basic-vim-commands-for-getting-started).

    Once the path to the model has been updated, restart the model service using `sudo systemctl restart model`.

## Enable and Start the Services

Once the model path in the device is specified, ensure that the Camera, Model, and Recorder services are enabled.  To verify, go back to the settings and click on the "Service Status" button.

{{ figure("/models/assets/deployment/raivin-service-status.png", "Service Status") }}

You will be greeted with the "Service Overview" page.  Ensure that the "camera" and "model" services are enabled and running by toggling the "Enable" and "Start" buttons as shown.  Only "Enable" the "recorder" service as shown.  You will be using the recorder service in [MCAP Recording](../../perception/data_collection/recording.md#record-mcap).

{{ figure("/models/assets/deployment/raivin-service-overview.png", "Service Overview") }}

## Live View (Camera Page)

Now you will see live inference of the model in the device.  Once the model and camera services are enabled, go back to the main page and then select the "Camera" card as shown, then enable the segmentation overlay from the page controls.

{{ figure("/models/assets/deployment/raivin-segmentation-app.png", "Segmentation App") }}

This will run inference on the model specified to generate segmentation masks on the detected objects.  In this case, the model is identifying coffee cups in the video feed.  An example is shown below.

{{ figure("/models/assets/deployment/segmentation-sample-1.png", "Segmentation Sample 1") }}

Now that the model has been updated, you can [make new recordings](../../perception/data_collection/recording.md#record-mcap) using the model's inference and then [visualize the recording using Foxglove Studio](../../perception/data_collection/foxglove.md).

## Inference Visualization in Foxglove

Once the MCAP recording has been downloaded, you can use Foxglove Studio to see the playback of MCAP recordings and the model inference.  The following preview is a frame from the MCAP with the model inference masks overlaid on top of the video.

{{ figure("/models/assets/deployment/foxglove-sample-1.jpg", "Foxglove Sample 1") }}

More information on the MCAP playback is provided in [Foxglove Studio](../../perception/data_collection/foxglove.md).  Modifying panels and customizing various settings are also shown in [Advanced Foxglove](../../perception/data_collection/advanced_foxglove.md).
