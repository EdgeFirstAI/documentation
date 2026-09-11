# MCAP Replay Service

## Overview

The Replay Service allows users to play back previously recorded MCAP files, enabling detailed analysis of MCAP data. This service provides flexible playback options and integrates with live fusion and model data for comprehensive testing and validation.

!!! warning "Torizon for Maivin 2026.08"

    The Replay service included in Torizon for Maivin 2026.08.0 predates the hostname namespace and EdgeFirst Schemas 4.0 migration of the other services and was not verified for this release.  Replayed camera frames are not consumed by the current Model service and radar, LiDAR, and fusion replay were not tested.  Refer to the [Known Issues](../../platforms/software/issues.md#replay-service-not-verified-on-2026080) and prefer [Foxglove Studio](foxglove.md) for reviewing recordings.

### How It Works

The Replay Service offers:

- Playback of recorded MCAP files
- Hybrid mode combining recorded and live data
- Real-time status monitoring
- Seamless integration with live system operations

## Using the Replay Service

The Replay Service is built into the [MCAP Recorder Modal](recording.md).

{{ figure("../../platforms/assets/setup/quickStart-mcap.png", "MCAP Recorder Interface") }}

You can visit the page by clicking the "MCAP Details" Button on any Raivin Page.

{{ figure("../assets/mcap-RecordingButton_McapDetailsButton.png", "MCAP Recording and Details Buttons") }}

### Starting Playback

1. Locate your desired MCAP file in the file list
2. Click the "Play" button ![MCAP Replay Play Button](../assets/replay_play.png) next to the file
3. In the playback options dialog, choose your preferred settings:

    - Fusion Source: Choose between Live or MCAP data for the post-processed radar topics
    - Model Source: Choose between Live or MCAP data for the post-processed image topics  

        {{ figure("../assets/replay_options.png", "MCAP Replay Options") }}

4. Click "Start" to begin playback

During playback, the currently playing file will have its "Play" button become a "Stop" button.  The State Indicator top ribbon will also note the platform is in "Replay Mode".  

{{ figure("../assets/replay_mode.png", "MCAP Replay Options") }}

Now that the device is in "Replay Mode", the inputs to the Segmentation, Occupancy, GPS, and IMU pages will come from the MCAP file instead of from the live sensors.

### Playback Controls

- Click the "Live Mode" button to return to displaying live sensor data.  

{{ figure("../assets/replay_to_live_mode.png", "MCAP Replay Options") }}

- Click the stop button ![MCAP Replay Stop Button](../assets/replay_stop.png) on the playing file to end playback

 !!! note
  Stopping a file from replaying will not put the device back into "Live Mode".  You must click the "Live Mode" button to return to "Live Mode".

!!! note
 When a file is playing, you cannot play another file until you stop the current playback.  Once you stop a file, you can start playing another file by clicking its "Play" button.

### Hybrid Mode

The Replay Service supports a hybrid mode where you can:

- Play back recorded sensor data while using live fusion and/or model data  

    {{ figure("../assets/replay_options.png", "MCAP Replay Options") }}

- Use recorded data for some systems while maintaining live data for others
- Mix and match recorded and live data sources based on your testing needs

## Configuration

The Replay service is started by the Web UI with the selected recording, the remaining settings are stored in `/etc/default/replay` following the same conventions as the other [service configuration files](../../platforms/configuration/index.md#configuration-files).

| Key | Default | Description |
|-----|---------|-------------|
| `MCAP` | | Path to the MCAP recording to replay, set by the Web UI |
| `REPLAY_SPEED` | `1.0` | Playback speed multiplier, `0.5` is half speed and `2.0` double speed |
| `TOPICS` | | Space-separated list of topics to publish from the recording, all topics when empty |
| `IGNORE_TOPICS` | | Space-separated list of topics to skip, the Web UI uses this to keep the live model or fusion output |

## Status Monitoring

This section describes the various states the system can be in and how they are reported.

### Status Indicator Button (Maivin/Raivin only)

Located in the top-right corner, the status indicator button shows status and state:

- **Live Mode** (Green): System mode is operating with live data and system status is working normally.

    {{ figure("../assets/replay_livemode.png", "Live Mode Status") }}

- **Replay Mode** (Blue): System is playing back an MCAP file and system status is working normally.

    {{ figure("../assets/replay_replay_mode.png", "Replay Mode Status") }}

- **Stopped** (Red):  System is not playing back an MCAP nor operating with live data.

    {{ figure("../assets/replay_stopped.png", "Stopped Status") }}

- **Degraded Mode** (Amber): The system status is some expected services are not enabled.

    {{ figure("../assets/replay_degraded_mode.png", "Degraded Status") }}

Click this button to view detailed service status, which shows the individual service states (Running/Stopped).  

{{ figure("../../platforms/assets/setup/quickStart-serviceStatusModal.png", "Service Status Modal") }}

### Recording Button

The button changes to contain a pulsing white circle and non-pulsing text on a red background when the system is actively recording.  

{{ figure("../assets/mcap_recording.png ", "MCAP Recording") }}
