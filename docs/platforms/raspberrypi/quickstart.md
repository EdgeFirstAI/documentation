# Quickstart Guide

<figure markdown="span">
![RaspberryPi](assets/raspberrypi.webp){align=center, width=50%}
</figure>

To get started using EdgeFirst Studio with the Raspberry Pi you simply need to install the EdgeFirst Perception Middleware using the following command on your Raspberry Pi terminal.

```bash
$ pip install edgefirst
```

This will install the EdgeFirst Perception Middleware into your Python environment allowing you to easily collect datasets and evaluate models trained in EdgeFirst Studio on your Raspberry Pi.

Sign up for a free trial on EdgeFirst Studio and then use your login information to connect your Raspberry Pi to EdgeFirst Studio.

```bash
$ edgefirst login
Username: myself
Password: *****
```

You're now ready to evaluate the various public models or collect a custom dataset on your Raspberry Pi!

A default model has been provided which will detect and segment people using the camera.  To start the demo simply run the following command and then point your browser to your Raspberry Pi.

```bash
$ edgefirst webui
```

## Supported Topics

Most EdgeFirst Middleware topics are supported by the RaspberryPi platform.  A summary of the topics is provided here, the ones with a red outline are currently unsupported by the RaspberryPi while those with an orange outline have certain hardware requirements outlined further below.  The topics with a green outline are fully supported.

```mermaid
graph LR
    camera --> model["vision model"] --> zenoh    
    radar --> fusion["fusion model"] --> zenoh
    lidar --> zenoh
    camera --> fusion
    radar --> zenoh
    camera --> zenoh    
    model --> fusion
    navsat --> zenoh
    imu --> zenoh
    zenoh --> recorder --> mcap
    zenoh --> webui --> https
    zenoh --> user["user apps"]
    https --> user

    style zenoh stroke:green,stroke-width:5px
    style recorder stroke:green,stroke-width:5px
    style webui stroke:green,stroke-width:5px
    style https stroke:green,stroke-width:5px
    style mcap stroke:green,stroke-width:5px
    style user stroke:green,stroke-width:5px
    style model stroke:green,stroke-width:5px,stroke-dasharray: 5 5    

    style camera stroke:orange,stroke-width:5px,stroke-dasharray: 5 5
    style navsat stroke:orange,stroke-width:5px,stroke-dasharray: 5 5    
    style lidar stroke:orange,stroke-width:5px,stroke-dasharray: 5 5

    style radar stroke:red,stroke-width:5px,stroke-dasharray: 5 5
    style fusion stroke:red,stroke-width:5px,stroke-dasharray: 5 5
    style imu stroke:red,stroke-width:5px,stroke-dasharray: 5 5
```

## Hardware Requirements

- Raspberry Pi 5
    - Older Pi devices may work but have not been tested
- Raspberry Pi OS (64bit)
- Raspberry Pi Camera Module (optional)
    - Raspberry Pi or compatible modules through GStreamer with the libcamera driver
- USB Camera (optional)
    - USB cameras are supported through GStreamer with the UVC V4L2 driver
- Models will run on the CPU by default
    - Ara-2 and Hailo accelerators are also supported for improved performance
