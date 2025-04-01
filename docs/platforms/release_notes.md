# Release Notes

## Version 2025.01

This is the first official release of the Maivin Perception Platform.

For Maivin users this software release is a major upgrade which unifies the Torizon for Maivin branches of Raivin and Maivin into a single software release.  As part of this release the version naming has been updated to follow the the YEAR.MONTH.PATCH format instead of using the Torizon version number as the base.  The YEAR and MONTH refer to the data of the initial release of the software and the PATCH will be included for incremental patch release within this release cycle.  The upstream Torizon OS version number is documented in the release notes.

This release includes a major update to the WebUI interface of the Maivin Perception Platform.  The new interface provides a collection of panels that can be used to monitor and control the platform.  The primary page for the Maivin is the "Segmentation View" page, where the Raivin provides a combined segmentation view and occupancy grid panel.  The WebUI also provides a page for only the occupancy grid.  Configuration pages have been added allowing the user to configure various aspects of the Maivin platform. Currently, configuration is focused on the EdgeFirst Middleware services but future updates plan to add networking and other configuration options.

### EdgeFirst Models
- ModelPack for Detection and Segmentation
- RadarExp Fusion Model

### EdgeFirst Packages
- Camera
- Radarpub
- Model
- Fusion
- IMU
- NavSat
- Recorder
- Playback
- WebUI
- Web Server

### System Packages
- Torizon 6.8.1
- Linux 5.15.148
