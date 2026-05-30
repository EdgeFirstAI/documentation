# Record MCAP

MCAP recordings can be started and stopped using the Recording Button at the device's [top navbar](../../platforms/quickstart/maivin/webui.md#the-top-ribbon).  It is to the left of the MCAP Details hamburger button, which is used to open the [MCAP Details Modal](../../perception/data_collection/recording.md#the-mcap-modal).

{{ figure("/perception/assets/mcap-RecordingButton_McapDetailsButton.png", "MCAP Recording and Details Buttons") }}

Both of these buttons are available on every page of the Maivin, Raivin, and other edge devices running the EdgeFirst middleware.
!!! note
     You must close all modals to be able to click the "Recording" and "Details" Buttons.

For more information about recording MCAPs, please read the [MCAP Recording section](../../perception/data_collection/recording.md).

## Start Recording

To start a recording, simply click the "Recording" button to begin capturing data.

{{ figure("/perception/assets/mcap_recording.png", "MCAP Recording") }}

!!! note
     It may take up to 30 seconds for a recording to start, depending on topic tracked.

!!! warning "Low Disk Space"
     If there is not enough room on the drive to record an MCAP, recording will automatically stop and you will get a "Low Disk Space" error.
     {{ figure("/platforms/assets/mcap_low-disk-space.png", "MCAP Low Disk Space Warning") }}

If you were to open the MCAP Details Modal while recording, you would see a new MCAP file in the MCAP list.

{{ figure("/platforms/assets/mcap_modal_while_recording.png", "MCAP Modal While Recording") }}

## Stop Recording

To stop recording, click the "Recording" button a second time.
