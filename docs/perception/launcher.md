# EdgeFirst Launcher

The EdgeFirst Launcher is responsible for managing the EdgeFirst Middleware in user-mode, which means a user launches the services manually from the command-line rather than system-managed where the services are under the control of systemd and installed into the system.

The user-mode Middleware is meant to be installed using `pip install edgefirst` which will install the service binaries, webui, and supporting assets such as the default people detection model.  Deploying the launcher can be as simple as `edgefirst live` like the example shown in [Deploying to Embedded Targets](../models/deployment/launcher.md).  However, descriptions of each service are provided in the sections below and such as the commands used to deploy these services individually.

### Services

The `edgefirst` launcher is the preferred method of launching multiple services as user-mode whereas system-mode would prefer using systemd to manage services.  The services are described below which is intended for more advanced manual configuration of the services.

#### Camera Service

The Camera Service or EdgeFirst Camera Publisher implements the standard ROS2 camera interfaces plus a proprietary extension to provide DMA support.  As with all EdgeFirst services the ROS2 interfaces are implemented over Zenoh and can plug into a true ROS2 setup using the zenoh-bridge-dds service.

Deploy this service in your target with the following command.  The `&` parameter will run the service in the background allowing you to continue using the terminal.  We also specify `--mirror none` to avoid any horizontal or vertical flip to the camera feed.  By default, the camera is flipped both horizontally and vertically to compensate for the orientation of the Maivin camera which is installed upside-down.

```shell
$ edgefirst-camera --h264 --mirror none &
```

The command below lists all available parameters from this service.

```shell
$ edgefirst-camera -h
```

!!! info

    To bring background executed commands to the foreground, enter `fg` allowing you to exit the program via CTRL-C.

#### Model Service

The Model Service or Maivin Detection Service deploys a ModelPack Detection and Segmentation model for inference to output bounding boxes or segmentation masks on the detected objects in the camera feed.

Deploy this service in your target with the following command.  In this command specify the path to the model denoted by `--model`.  We recommend using a quantized TFLite model in embedded targets.

```shell
$ edgefirst-model --model mymodel.tflite &
```

The command below lists all available parameters from this service.

```shell
$ edgefirst-model -h
```

!!! warning

    The camera service needs to be running in the background as described [above](#camera-service) to fetch camera frames for model inference. 

#### Webserver Service

The Webserver Service or the EdgeFirst Web UI Server deploys a webserver on target to provide a GUI that's accessible using the target's IP address as the endpoint on a browser `https://MY_DEVICE_IP`.  The GUI provides visualizations from the camera feed and model inferences and exposes the features for recording an MCAP, downloading an MCAP locally, deleting an MCAP, or listing the recorded MCAPs as shown in the [Live Camera Mode](../models/deployment/launcher.md#live-camera-mode) section.

If a virtual environment was created, deploy this service using the command below.  The `--docroot` directory needs to be specified.

```shell
$ edgefirst-websrv --docroot venv/share/edgefirst/webui
```

If a virtual environment was not created, deploy this service using the command below.

```shell
$ edgefirst-websrv --docroot /usr/share/edgefirst/webui/
```
