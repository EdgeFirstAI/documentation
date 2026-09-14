# Deploying a New Model to the Model Service

There are two ways to deploy a new, 2D model to the Raivin's Model Service: the Web UI Interface or via the command-line.

## From the Raivin Web UI

From the [Model Service Configuration page](../../platforms/configuration/model.md), enter the absolute filename `/home/torizon/modelpack.tflite` in the "MODEL" text-box.  Hit the "Save Configuration" button, the page reports when the model service has restarted with the new configuration.

{{ figure("../../models/assets/deployment/model_location_webui.png", "Model Configuration Page") }}

Remember to save the configurations at the end of the process. The  Model Configuration page can be accessed via the following url:
`https://verdin-imx8mp-xxxxx/config/model`

## Manual Model Deployment

In case the manual deployment is needed, you need to connect to the device via [SSH](../../platforms/networking/ssh.md):

```shell
ssh torizon@verdin-imx8mp-15141030
```

and edit the model parameters in `/etc/default/model`

```shell
sudo vi /etc/default/model
```

then restart the model service using the `systemctl` command

```shell
sudo systemctl restart model
```

!!! note

    Remember to use **sudo** to edit the configuration and to restart the model service.

Now that the model is running, open the Raivin's Web UI, go to the [Camera Page](../../platforms/quickstart/raivin/webui.md#the-camera-page), enable the segmentation overlay, and check the camera to see the model's detections.  

{{ figure("../../models/assets/deployment/segmentation-sample-1.png", "Deployment Results") }}
