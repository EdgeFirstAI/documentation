# Record a Dataset

Before recording, open Settings from the Menu on the Web UI and confirm:

- **Service Status**: "Enable" and "Start" are **On** for the camera, radar/LiDAR publisher, and fusion services, see [Service Status](../../configuration/service_status.md)
- **Radar Settings**: "Enable Cube" is **On** if you are training a low-level Fusion model, see [Radar Settings](../../configuration/radar.md#enable-cube)
- **MCAP Settings**: "Storage Location" is set to `/media/DATA` if recording to the SD card, see [Recorder Settings](../../configuration/mcap_recording.md#storage-location)

{% include-markdown "discrete/datasets/recording_mcap_on_device.md" %}

{% include-markdown "discrete/datasets/downloading_mcap_from_device.md" %}

## Next Steps

Now that you have recorded an MCAP, you can [upload the MCAP to EdgeFirst Studio](upload.md) to begin building your dataset using this MCAP.
