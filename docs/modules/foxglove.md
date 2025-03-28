# Foxglove Studio
[Foxglove Studio][foxglove] is an open source application developed by FoxGlove Technologies, Inc.  It is part of the [Robot Operating System (ROS)][ros] ecosystem and supports playback for MCAP recordings.  You can [download Foxglove Studio][foxglove_dl] as well as our [EdgeFirst plug-in for Foxglove][github_edgefirst_dl] and customized [Raivin Foxglove layout](static/Raivin_Foxglove_Layout.json).

## Getting Started
Let's discuss how to install our custom plug-ins once you've installed Foxglove Stuiods.

### Installing EdgeFirst Plugin
```{note}
These will describe installing the 1.0.2 version of the EdgeFirst plug-in for Foxglove, which is current as of time of writing.
```

1. Open Foxglove Studio

2. If necessary, uninstall any existing versions of the EdgeFirst plug-in
   - Click the User Settings button on the right side of the top menu bar.
   - Select the Extensions option in the pull-down menu.  
   ![Foxglove settings](static/foxglove_setting.png){align=center}
   - Click the EdgeFirst Detect plugin  
   ![Foxglove extension view](static/foxglove_extension_view.png){align=center}
   - Click the "Uninstall" button  
   ![Foxglove install extenstion](static/foxglove_install_extenstion.png){align=center}
   - Click the "Back to dashboard" button in the top-left corner of the application main window.

3. Install the current version of the EdgeFirst plug-in.
   - Click the User Settings button on the right side of the top menu bar.
   - Select the Extensions option in the pull-down menu.  
   ![Foxglove settings](static/foxglove_setting.png){align=center}
   - Click the "Install local extension..." button.  
   ![Foxglove extension view](static/foxglove_extension_view.png){align=center}
   - Select the `edgefirst.detect-1.0.2.foxe` file from the downloads directory.

4. Confirm that the 1.0.2 version was installed  
   ![Foxglove extension view with 1.0.2](static/foxglove_extension_view_1.0.2.png){align=center}

5. Close Foxglove Studio and restart it.

### Installing Foxglove Layout
We have included a [custom Raivin Layout for Foxglove Studio](static/Raivin_Foxglove_Layout.json).To install it, please download it and follow the instructions below.

1. Open Foxglove Studio
2. Load an MCAP file downloaded from the Raivin.
3. Click the "Layout" buttom in the top taskbar.
4. Select the "Import from file..." option in the Layout menu.  
   ![Foxglove layout](static/foxglove_layout.png){align=center}
5. Go to the download directory holding the JSON layout file and select the file.
6. Confirm the layout JSON file is loaded.  
   ![Foxglove scene](static/foxglove_scene.png){align=center}

### Layout Features
The default Raivin layout includes:
- Top panel: H.264 camera stream with bounding box overlays
  - Shows detection results (i.e. the coloured boxes around people when using a detection model)
  - Shows segementation masks (i.e. the coloured blobs covering detected objects when using a segmentation model)
- Bottom right panel: GPS coordinates map view
  - Interactive map with zoomable blue target showing camera position
- Bottom left panel: IMU sensor readings
  - Can be configured to show real-time plots
- Bottom timeline: Playback controls for navigation

## Visualization Features
In the example above, we see both detection boxes and segmentation masks in the H.264 Camera topic.

### Viewing Detection Messages
The detection boxes are contained in the `/model/boxes2d` topic.  By default, this topic is not enabled.  See the Maivin Dataset Recording section for details on how to enable this topic and record an MCAP with the Raivin.

```{note}
Not all vision models are able produce detection results.  The default model on the Raivin can produce both detection and segmentation results.
```

1. Record a MCAP file that captures the `/model/boxes2d` topic.
2. Confirm with the "Details" button that the newly recorded MCAP has a `/model/boxes2d` topic.  
   ![MCAP details](static/foxglove_mcap_details.png){align=center}
3. Download the file from the Raivin and load it in Foxglove Studio.
4. Click the "Settings" gear icon on the right side of the `/camera/h264/` panel task bar.
5. The `/model/boxes2d` option should appear in the "Image annotations" dropdown menu in the "Image Panel" settings sidebar (bottom left of image below).  
   ![Foxglove detect plugin view](static/foxglove_detect_plugin_view.png){align=center}
6. Enable the `/model/boxes2d` image annotations by clicking the closed eye icon. This will draw boxes around the detected objects.  
   ![Foxglove detect boxes enabled](static/foxglove_open_box_eye.png){align=center}

### Viewing Segmentation Messages
Segmentation masks are contained in the `/model/mask_compressed` topic which is enabled on the Raivin by default.  Because of the amount of data included within this stream, it is not compatible with the default Image drawing API in Foxglove Studio. To visualize the Segmentation Mask, the EdgeFirst Foxglove plug-in must be installed to view segmentation masks in Foxglove.

The instructions to view these masks are the same as above but using the `/model/mask_compressed` topic instead of the `/model/boxes2d` topic.  
![Foxglove detect boxes enabled](static/foxglove_open_seg_eye.png){align=center}

### Viewing /radar/cube Messages
By default, none of the radar topics are recorded as part of an MCAP file.  The Image panel in Foxglove can viewer can 

1. Record a MCAP file that has the `/radar/cube` message in it. See Maivin Dataset Recording for details
2. Play the MCAP file in Foxglove Studio. See Playback MCAP with Foxglove Studio for details.
3. In the image panel, the `/radar/cube` topic should appear under the list of valid image topics.  
![Foxglove radar mask](static/foxglove_radar_mask.png){align=center}
4. Select the `/radar/cube` topic
5. Change the color mode to Color Map, and select Turbo for the color map.  
![Foxglove radar message](static/foxglove_radar_msg.png){align=center}
6. Leave the value min and value max on auto
7. You can now see the `/radar/cube` message.  
![Foxglove final radar view](static/foxglove_final_radar_view.png){align=center}

### IMU Data Plotting
To create IMU sensor plots:

1. Convert bottom left panel to Plot view
2. Click "Add a Series"
3. Select `/imu` as the topic
4. Choose desired parameters (e.g, angular_velocity, x, y, z)
5. Repeat to add additional plot series as needed  
   ![IMU](static/imu.png){align=center}
   ![static/imu_to_plot.png](IMU to plot){align=center}
   ![plot](static/plot.png){align=center}
   ![IMU message](static/imu_msg.png){align=center}
   ![IMU velocity](static/imu_velocity.png){align=center}
   ![IMU final view](static/imu_final_view.png){align=center}

## Additional Resources

For more detailed information about Foxglove Studio features, visit the [Foxglove Documentation website][foxglove_doc].


[foxglove]: https://foxglove.dev/
[foxglove_dl]: https://foxglove.dev/download
[foxglove_doc]: https://docs.foxglove.dev/docs/introduction/
[github_edgefirst_dl]: https://github.com/MaivinAI/foxglove-edgefirst/releases/latest
[ros]: https://ros.org/