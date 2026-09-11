# Deploying a New Model to the Fusion Service

The Fusion Service model can be configured from the "The Radar model" field of the [Fusion Settings page](../../platforms/configuration/fusion.md), or by SSH into the device and editing the `/etc/default/fusion` file, using the following the command:

```bash
sudo vi /etc/default/fusion
```

Change the model line to point to the new Fusion model `/home/torizon/fusion.tflite`.  The fusion model pipeline is disabled while this setting is empty, the RadarExp models shipped with the Raivin are available under `/usr/share/edgefirst/fusion/`.

```ini
# Path to the radar-camera fusion model (TFLite).
MODEL="/home/torizon/fusion.tflite"
#MODEL="/usr/share/edgefirst/fusion/radarexp-ultra-short.tflite"
```

The fusion model requires the [radar cube](../../platforms/configuration/radar.md#enable-cube) to be enabled on the radar publisher.  After that, restart the Fusion Service using the following command:

```bash
sudo systemctl restart fusion
```
