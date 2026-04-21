# Camera Settings

This page configures the camera service that interacts with the Raivin's [OmniVision OS08A20 image sensor][os08a20]. With the exception of the H.264 Bitrate, camera and stream sizes, it is not recommended that you change these settings.

{{ figure("../assets/configuration/configuration-camera.png", "Camera Settings page") }}

!!! tip
    These values are stored in the `/etc/default/camera` file on the device and can be hand-edited. This is not recommended.

## Camera Device

This configures what camera device the camera service will use, which on Raivin will be `/dev/video3`.

## Camera Size

This sets the camera resolution which is used for the camera capture and separate from the streaming resolution. The camera resolution can be set to any resolution supported by the camera. If the camera size is set to "3840 2160", it will put the camera service into [4K Mode](../../perception/4k/index.md).

## Stream Size

This configures the streaming resolution for the H.264 and JPEG streaming. The H.264 stream supports up to HD resolution (1920x1080). The JPEG stream supports all resolutions but is encoded on the CPU so the practical limit is around 960x540 or 640x360 to maintain 16:9 aspect ratio.

## Mirror

The camera mirror setting can flip the camera image to match the orientation of the camera. The camera can also be mirrored horizontally to provide a mirror image. Accepted values are "none", "horizontal", "vertical", and "both". This is set to "both" as the image sensor is both upside-down and inverted.

## H.264 Bitrate

Controls the H.264 streaming compression level. The higher the bitrate, the better the quality of the image. The actual bitrate remains variable based on the scene but this value sets the cap. Possible values are "auto", "mbps5", "mbps25", "mbps50", and "mbps100". The "auto" setting is about 10 Mbps on the Raivin. This also impacts MCAP recording size.

## H.264 Streaming

This setting enables or disables the `/camera/h264` topic. This is enabled by default.

## JPEG Streaming

This setting enables or disables the `/camera/jpeg` topic. This is disabled by default. Enabling this will result in higher system utilization and larger MCAP files but will provide JPEG screen captures from the camera service.

[os08a20]: https://www.ovt.com/products/os08a20/
