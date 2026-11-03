# Raivin Quick Start

{{ figure("../../assets/raivin.png", "Raivin", "50%") }}

The Raivin configuration further extends the perception capabilities of the [Maivin platform](../maivin/index.md) through the addition of the [integrated radar module](../../hardware/radar.md) or [LiDAR module](../../hardware/lidar.md).  The EdgeFirst Perception Middleware is augmented for Raivin configurations with the fusion service which projects the radar and LiDAR point clouds onto the vision model output to classify targets, produce 3D bounding boxes, and an occupancy grid.  The [EdgeFirst Fusion Model](../../../models/fusion/index.md) additionally provides low-level radar data fusion with the vision data.  The low-level radar data is represented as the range and doppler data cube, the EdgeFirst Fusion Model fuses this data with the vision data to provide a more robust perception stack.  The traditional point-cloud data from the radar is also available for use by the Raivin perception stack, and is especially useful for augmenting the object detection and tracking capabilities through the additional parameters offered by the point cloud data.

## System Architecture

The Raivin runs a Linux operating system based on Toradex's [Torizon OS 7](https://www.toradex.com/torizon), we refer to the operating system as Torizon for Maivin.  The operating system packages include common libraries and tools you would expect to find on a typical embedded Linux operating system focused on computer vision and AI (Python, OpenCV, GStreamer, etc...) along with the Docker container engine for user applications.  Refer to the [Release Notes](../../software/release_notes.md) for the versions included in the current release and the [Software Updates](../../software/updates.md) for keeping the platform up to date.

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, what we call our collection of applications and libraries used in the implementation of the perception stack.  On the Raivin these applications run natively as systemd services, the radar or LiDAR publisher and the fusion service are enabled during provisioning in addition to the base Maivin services.  The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../perception/dev/index.md), for this document we focus on describing the application services and how they fit together to deliver the perception middleware.

This guide walks through the full loop: set up the Raivin, record a dataset, bring it into EdgeFirst Studio, annotate it, train a Fusion model, validate it, and deploy it back to the device &mdash; then repeat.  Each step below covers the actual clicks and commands, follow the linked guide for the full details.

## 1. Set Up Your Raivin

Unbox the Raivin, connect power and network, and power it on.  Once booted, browse to `https://<hostname>.local/` to confirm the device is online.

{{ figure("../../assets/setup/quickStart-mainPage.png", "Raivin Main Page") }}

Before recording, [SSH into the device](../../networking/ssh.md) and confirm the Radar or LiDAR mounting calibration matches your hardware configuration:

- Radar: `cat /etc/default/radarpub` and confirm `RADAR_TF_VEC` / `RADAR_TF_QUAT` match your mount, see [Radar Transform](../../configuration/radar.md#radar-transform)
- LiDAR: `cat /etc/default/lidarpub` and confirm `TF_VEC` / `TF_QUAT` match your mount, see [LiDAR Transform](../../configuration/lidar.md#transform-vector-and-rotation-quaternion)

Full details: [Setup Guide](setup.md)

## 2. Explore the Web UI

The main page shows one card for each running service:

- **Camera**: live video with detection/segmentation overlays and projected LiDAR points
- **LiDAR**: 3D point cloud (when the LiDAR publisher is running)
- **Radar**: point cloud over a polar occupancy grid
- **IMU**: 3D orientation with roll, pitch, and yaw
- **GPS**: map with current location and coordinates

Full details: [Web UI Walkthrough](webui.md)

## 3. Record a Dataset

**Access the device** using either method:

- SSH: `ssh torizon@<hostname>.local`
- Web UI: `https://<hostname>.local/`, click the gear icon to open Settings

**Confirm the recording settings** on the Settings page:

- Radar Settings: toggle "Enable Cube" **On** if you are training a low-level Fusion model
- MCAP Settings: set "Storage Location" to `/media/DATA` if recording to the SD card
- Service Status: toggle "Enable" and "Start" **On** for the camera, radar/LiDAR publisher, fusion, and recorder services

{{ figure("../../assets/configuration/configuration-servicesStatus.png", "Services Status page") }}

**Record**: close the settings modal, click the record button on the top navbar to start, click it again to stop.

{{ figure("../../assets/mcap_modal_while_recording.png", "MCAP Modal While Recording") }}

Full details: [Recording Guide](record.md)

## 4. Upload to EdgeFirst Studio

On the device's Web UI, click the EdgeFirst Studio button on the top ribbon and log in with your username and password.

{{ figure("../../../perception/assets/studio-login.png", "Login to EdgeFirst Studio") }}

Open the MCAP modal, click the "Upload" button for your recording, choose "Basic (Snapshot only)", and click "Upload".

{{ figure("../../../perception/assets/upload-basic.png", "Upload to EdgeFirst Studio") }}

Full details: [Upload Guide](upload.md)

## 5. Create a Project

If you haven't already created your own project in {{ studio_link("EdgeFirst Studio", "login") }}:

1. Click the "PROJECTS" button on the top navbar
2. Click "New Project"
3. Provide a name and description, then click "Create"

Full details: [Create Project](project.md)

## 6. Restore the MCAP into a Dataset

In {{ studio_link("EdgeFirst Studio") }}, open the Apps menu and click "Data Snapshots" to find your upload.

{{ figure("../../../perception/assets/studio-created-snapshot.jpg", "Data Snapshots") }}

Open the snapshot's context menu and click "Restore".  Choose your project, name the dataset, toggle "AI Ground Truth Generation" **On** to auto-annotate, then click "Restore".

{{ figure("../../../perception/assets/studio-restored-dataset.jpg", "Restoring the Dataset") }}

Full details: [Restore Guide](restore.md)

## 7. Split and Tag the Dataset

Restoring with AGTG enabled auto-generates the 2D boxes/masks and 3D boxes.  Review them in the gallery and fix any mistakes with the [manual 2D](../../../datasets/tutorials/annotations/manual.md#manual-2d-annotations) or [manual 3D](../../../datasets/tutorials/annotations/manual.md#manual-3d-annotations) annotation tools.

**Split**: on the dataset card, click the "+" button in the "Groups" field, set the Training/Validation percentages (default 80/20), and click "Split".

**Tag**: open the dataset options (three dots) → "History" → click the green "+" button, specify a tag version and description, and click "Create Tag".

Full details: [Split and Tag Guide](split.md)

## 8. Train the Fusion Model

From your project, open "Model Experiments" → create or open an experiment → "Training Sessions" → "New Session".  Set the Trainer Type to "EdgeFirst Fusion", pick your tagged dataset, and click "Start Session".

{{ figure("../../../models/assets/training/fusion-train-settings.jpg", "Training Session Fields") }}

Wait for the session to finish; the trained artifacts (ONNX, quantized TFLite) appear on the completed session card.

Full details: [Training Guide](train.md)

## 9. Validate the Model

**Cloud validation**: on the training session card, click "Validate", choose the model artifact and dataset partition, and click "Start Session".  Review the precision, recall, F1, and IoU charts once the session completes.

**On-device profiling**: [SSH into the Raivin](../../networking/ssh.md), install and sign in to the profiler, then create a **User Managed** validation session in Studio and run it on the device.

```sh
torizon@verdin-imx8mp-XXXXXXXX:~$ pip install edgefirst-profiler
torizon@verdin-imx8mp-XXXXXXXX:~$ edgefirst-profiler login
torizon@verdin-imx8mp-XXXXXXXX:~$ edgefirst-profiler validate --session-id v-XXXX
```

Full details: [Validation Guide](validate.md)

## 10. Deploy the Model

On the Web UI, go to Settings → "Fusion Settings", set the path to your trained model, and click "Save Configuration".

Go to Settings → "Service Status" and confirm the camera, radar/LiDAR, and fusion services are enabled and started.

{{ figure("../../../models/assets/deployment/occupancy-sample-1.png", "Model Inference on the Raivin") }}

Open the Camera or Radar card from the main page to see your model running live.

Full details: [Deployment Guide](deploy.md)

Once deployed, loop back to [recording a new dataset](#3-record-a-dataset) with the improved model running live to keep refining it.

## Optional: Review Your Recording

Download the MCAP from the [MCAP modal](../../../perception/data_collection/recording.md#download-mcap) and open it in [Foxglove Studio](../../../perception/data_collection/foxglove.md) to review the sensor data and model inference frame by frame.
