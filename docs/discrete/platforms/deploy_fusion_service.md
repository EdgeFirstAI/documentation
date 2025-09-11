# Deploying a New Model to the Fusion Service
As the Fusion Service Configuration page does not currently have a line item for Model, you will need to SSH into the device and edit the `/etc/default/fusion` file, using the following the command:
```bash
$ sudo vi /etc/default/fusion
```
Change the model line to point to the new Fusion model `/home/torizon/fusion.tflite`:

```
# The radar model
MODEL = "/usr/share/fusion/radarexp-ultra-short.tflite"
#MODEL = "/home/torizon/fusion.tflite"
```
After that, restart the Fusion Service using the following command:
```bash
$ systemctl restart fusion
```