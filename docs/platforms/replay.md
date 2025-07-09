# MCAP Replay Service

## Overview
The Replay Service allows users to play back previously recorded MCAP files, enabling detailed analysis of MCAP data. This service provides flexible playback options and integrates with live fusion and model data for comprehensive testing and validation.

### How It Works
The Replay Service offers:

- Playback of recorded MCAP files
- Hybrid mode combining recorded and live data
- Real-time status monitoring
- Seamless integration with live system operations

## Using the Replay Service
The Replay Service is built into the [MCAP Recorder Modal](./recording.md).  You can visit the page by clicking the "MCAP Details" Button on any Raivin Page.

### Starting Playback
1. Locate your desired MCAP file in the file list
2. Click the "Play" button ![MCAP Replay Play Button](assets/replay_play.png) next to the file
3. In the playback options dialog, choose your preferred settings:
      - Fusion Source: Choose between Live or MCAP data for the post-processed radar topics
      - Model Source: Choose between Live or MCAP data for the post-processed image topics  

         <figure markdown="span">
         ![MCAP Replay Options](assets/replay_options.png){align=center}
         <figcaption>MCAP Replay Options</figcaption>
	      </figure>

4. Click "Start" to begin playback

During playback, the currently playing file will be have its "Play" button become a "Stop" button.  The State Indicator top ribbon will also note the platform is in "Replay Mode".  

<figure markdown="span">
![MCAP Replay Options](assets/replay_mode.png){align=center}
<figcaption>MCAP Replay Mode</figcaption>
</figure>

Now that the device is in "Replay Mode", the inputs to the Segmentation, Occupancy, GPS, and IMU pages will come from the MCAP file instead of from the live sensors.

### Playback Controls
- Click the "Live Mode" button to return to displaying live sensor data.  

<figure markdown="span">
![MCAP Replay Options](assets/replay_to_live_mode.png){align=center}
<figcaption>MCAP Replay Options</figcaption>
</figure>

- Click the stop button ![MCAP Replay Stop Button](assets/replay_stop.png) on the playing file to end playback

	!!! note
		Stopping a file from replaying will not put the device back into "Live Mode".  You must click the "Live Mode" button to return to "Live Mode".
   
!!! note
	When a file is playing, you cannot play another file until you stop the current playback.  Once you stop a file, you can start playing another file by clicking its "Play" button.

### Hybrid Mode
The Replay Service supports a hybrid mode where you can:

- Play back recorded sensor data while using live fusion and/or model data  

	<figure markdown="span">
	![MCAP Replay Options](assets/replay_options.png){align=center}
	<figcaption>MCAP Replay Options</figcaption>
	</figure>

- Use recorded data for some systems while maintaining live data for others
- Mix and match recorded and live data sources based on your testing needs

# Status Monitoring
This section describes the various states the system can be in and how they are reported.

## System Status Bar
The status bar provides real-time information about your system's operational state and service health.

### Status Indicator Button
Located in the top-right corner, the status indicator button shows status and state:

- **Live Mode** (Green): System mode is operating with live data and system status is working normally.
<figure markdown="span">
![Live Mode Status](./assets/replay_livemode.png)
<figcaption>Live Mode Status</figcaption>
</figure>
- **Replay Mode** (Blue): System is playing back an MCAP file and system status is working normally.
<figure markdown="span">
![Replay Mode Status](./assets/replay_replay_mode.png)
<figcaption>Replay Mode Status</figcaption>
</figure>
- **Stopped** (Red):  System is not playing back an MCAP nor operating with live data.  
<figure markdown="span">
![Stopped Status](./assets/replay_stopped.png)
<figcaption>Stopped Status</figcaption>
</figure>
- **Degraded Mode** (Amber): The system status is some expected services are not enabled.
<figure markdown="span">
![Degraded Status](./assets/replay_degraded_mode.png)
<figcaption>Degraded Status</figcaption>
</figure>

Click this button to view detailed service status, which shows the individual service states (Running/Stopped).  

<figure markdown="span">
![Service Status Modal](assets/quickStart-serviceStatusModal.png){align=center}
<figcaption>Service Status Modal</figcaption>
</figure>

### Recording Button
The button changes to contain a pulsing white circle and non-pulsing text on a red background when the system is actively recording.  

<figure markdown="span">
![MCAP Recording](assets/mcap_recording.png ){align=center}
<figcaption>Recording</figcaption>
</figure>