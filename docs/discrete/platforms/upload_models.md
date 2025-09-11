# Uploading Models to the Raivin
In the [SCP section in the SSH Tutorial](../../platforms/ssh.md#secure-copy), files can be uploaded to the Raivin using the command:
```bash
scp input_file torizon@verdin-imx8mp-XXXXXXX:.
```
!!! note
    The above command assumes you have an SSH client, such as OpenSSH, installed.  Please review the [SSH documentation](../../platforms/ssh.md) to confirm.

For the following examples, we will have the Fusion model of `fusion.tflite` and the ModelPack model `modelpack.rtm` that we want to upload to target device `verdin-imx8mp-07130049`.

First, we need to upload the files to the Raivin target using SCP:
```bash
$ scp fusion.tflite torizon@verdin-imx8mp-07130049:.
$ scp modelpack.rtm torizon@verdin-imx8mp-07130049:.
```
We should be able to confirm the files are there by using commands via SSH.
```bash
$ ssh torizon@verdin-imx8mp-07130049 ls fusion.rtm modelpack.rtm
fusion.tflite  modelpack.rtm
```
These files will be the `/home/torizon` directory, so their absolute filenames will be `/home/torizon/fusion.tflite` and `/home/torizon/modelpack.rtm`.  Once the files have been uploaded, we can then configure the device with the files.