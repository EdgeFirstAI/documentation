# Deploying a New Model to the Model Service

There are two ways to deploy a new, 2D model to the Raivin's Model Service: the Web UI Interface or via the command-line.

## From the Raivin Web UI

From the [Model Service Configuration page](../../platforms/configuration/model.md), enter the absolute filename `/home/torizon/modelpack.tflite` in the "MODEL" text-box.  Also, confirm the "Draw Boxes" check box is enabled, as the current trainer only supports 2D Box detection.  Hit the "Save Configuration" box and continue on.

![Model Configuration Page](../../models/assets/deployment/model_location_webui.png)

Remember to save the configurations at the end of the process. The  Model Configuration page can be accessed via the following url:
`https://verdin-imx8mp-xxxxx/config/model`

## Manual Model Deployment

In case the manual deployment is needed, you need to connect to the device via [SSH](../../platforms/networking/ssh.md):

```shell
ssh torizon@verdin-imx8mp-15141030
```

and edit the model parameters in `/etc/default/model`

```shell
vi /etc/default/model
```

then restart the model service using the `systemctl` command

```shell
sudo systemctl stop model
sudo systemctl start model 
```

!!! note
    Remember to use **sudo** to start and stop model services

Now the model is running, open the Raivin's WebUI, go to the [Segmentation Page](../../platforms/walkthrough.md#the-segmentation-page), and check the camera to see the model detection the object.  
![Deployment Results](../../models/assets/deployment/deployment-results.png)
