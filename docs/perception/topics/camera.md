# Camera Topics

The camera topics are managed by the `camera` service and handles interfacing with a local camera to produce camera frames which can be shared to multiple consumers with low overhead by leveraging zero-copy through DMA buffers.  The service can also produce encoded frames in H.264 or JPEG suitable for recording or streaming to a remote device.  The following is a list of key features provided by the camera service.

- Video4Linux2 Cameras
- i.MX 8M Plus ISP
    - Using the VSI ISP driver
    - Publishes camera intrinsic parameters from ISP configuration
- Zero-Copy frame publishing using Linux [dma-buf](https://docs.kernel.org/driver-api/dma-buf.html)
- Hardware H.264 Encoder
    - VSI Hantro (i.MX 8M Plus)
    - 1080p @ 60FPS
    - 4K @ 30FPS through [tiling](../4k/index.md)
- Software JPEG Encoder
- Recording and replay of the H.264 stream for reproducible testing

The camera topics are published under the `camera` namespace and offer the following sub-topics.  Some topics are optional and might not be available on the current system, refer to the [camera service configuration](../../platforms/configuration/camera.md) documentation for details.  Topic names are relative to the device [hostname namespace](index.md#hostname-namespaces).

## camera/info

The `camera/info` topic publishes information about the camera using the [CameraInfo](../api/sensor_msgs.md#camerainfo) schema.  The schema provides the specifications for the camera resolution and optical parameters.  On the Maivin the intrinsic parameters come from the ISP calibration matching the configured [camera mode](../../platforms/configuration/camera.md#camera-mode).  The camera service also publishes the static transform from the `base_link` frame to the `camera_optical` frame on the `tf_static` topic.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | Used by the Camera page overlays
Foxglove | [Image Panel Calibration](https://docs.foxglove.dev/docs/visualization/panels/image)
SDK | [Camera Info Example](../dev/examples/camera.md#camera-info)

## camera/frame

The `camera/frame` topic uses the custom [CameraFrame](../api/edgefirst_msgs.md#cameraframe) EdgeFirst schema for transmitting camera frames as Linux [dma-buf](https://docs.kernel.org/driver-api/dma-buf.html) descriptors.  This enables high-performance zero-copy of camera buffers between applications with trivial overhead.  A `CameraFrame` is a stamped [Tensor](../api/edgefirst_msgs.md#tensor): the header carries the timestamp and the camera frame ID, `seq` carries the V4L2 frame sequence for drop detection, and the tensor carries the producer process ID, the image format described as a FOURCC such as `NV12`, the colorimetry, the shape as `[height, width]`, and one [TensorPlane](../api/edgefirst_msgs.md#tensorplane) per plane with the dma-buf file descriptor handle, offset, stride, and size.

!!! note "Migrating from camera/dma"

    `camera/frame` replaces the `camera/dma` topic and its `DmaBuffer` schema from earlier releases, which were removed in EdgeFirst Schemas 4.0.  Consumers must decode the `CameraFrame` message with schemas 4.0 or later, the model and fusion services included in Torizon for Maivin 2026.08 consume `camera/frame`.

The mechanism for sharing buffers is for the camera service to publish its own `pid` along with the file descriptor `handle` of each plane along with the buffer parameters (shape, stride, format).  When a subscriber receives the message it must first duplicate the file descriptor into its own process space, this is done using the [pidfd_getfd](https://man7.org/linux/man-pages/man2/pidfd_getfd.2.html) system call.  Once the file descriptor has been duplicated it can be used normally, either used as-is with an API which can consume a `dma-buf` or by using [mmap](https://man7.org/linux/man-pages/man2/mmap.2.html) to map the contents of the buffer into user-space.

``` mermaid
sequenceDiagram
    loop
    autonumber
    Camera Service->>Client Application: CameraFrame(tensor.pid, planes[0].handle, ...)
    Client Application-->>Linux Kernel: pidfd_open(pid, fd)
    Client Application-->>Linux Kernel: pidfd_getfd(pidfd, handle)
    Linux Kernel->>Client Application: fd duplicate
    Client Application-->>Linux Kernel: mmap(fd)
    Linux Kernel->>Client Application: ptr to camera pixels
    Client Application-->Linux Kernel: Client Application Processing
    Client Application-->>Linux Kernel: munmap(ptr)
    Client Application-->>Linux Kernel: close(fd)
    Client Application-->>Linux Kernel: close(pidfd)
    end
```

1. Camera service publishes a CameraFrame for each frame received from the camera.
2. Client application calls `pidfd_open(pid, 0)` to acquire a file descriptor that refers to the camera service process.
3. Client application calls `pidfd_getfd(pidfd, handle, 0)` to acquire a local duplicate of the camera buffer file descriptor.
4. A new file descriptor is returned, to release the `dma-buf` object we will need to call `close(fd)` later.
5. Client application calls `mmap(fd, ...)` to acquire a local pointer to the camera buffer's pixel data.
6. A read-only pointer is returned to the client application, it will need to be released using `munmap(ptr)` later.
7. Client application processes the pixel data.
8. Client application calls `munmap(ptr)` to free the mapped buffer.
9. Client application calls `close(fd)` to release the `dma-buf` object.
10. Client application calls `close(pidfd)` to release file descriptor for the camera service process.

The tensor also carries a `fence_fd` which, when not `-1`, is a DMA fence the consumer must wait on before reading the planes.  The camera service publishes frames with the fence already signaled.

!!! tip "Permission Denied Errors"

    The client application will not be able to call pidfd_getfd if the client application runs at a lower permission level than the camera service. If this error occurs, try running the client application as `sudo` or as a service.

!!! tip "Mapping DMA Buffers"

    Mapping DMA buffers into user-space requires additional synchronization primitives around accesses.  We cover these details in our camera sample application.  Further details are documented in the Linux Kernel Manual under [CPU Access to DMA Buffer Objects](https://docs.kernel.org/driver-api/dma-buf.html#cpu-access-to-dma-buffer-objects).

This topic can only be consumed by applications running on the same device as the camera service, remote applications should use the compressed topics below.  The `camera/frame` topic is not recorded by the [Recorder](../data_collection/recording.md).

## camera/h264

The `camera/h264` topic uses Foxglove's [CompressedVideo](../api/foxglove_msgs.md#compressedvideo) schema to publish H.264 encoded video frames.  The H.264 encoder uses key-frames, I-Frames, at a typical rate of 1Hz with the frames in-between encoded as P/B-Frames.  The decoder requires an initial I-Frame before it can decode additional frames.  This is typically handled transparently but means when sending `CompressedVideo` data to the H.264 decoder it could take up to a second until valid output is produced.  The stream is enabled by default and is used by the Web UI camera page and the recorder, the encoder runs at the frame rate the camera is configured for.

When the camera captures at 4K with [tiling](../4k/camera_4k.md) enabled the frame is encoded as four 1080p tiles on the `camera/h264/tl`, `camera/h264/tr`, `camera/h264/bl`, and `camera/h264/br` topics instead.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | [Camera Page](../../platforms/quickstart/maivin/webui.md#the-camera-page)
Foxglove | [CompressedVideo Example](../data_collection/foxglove.md#viewing-detection-messages)
SDK | [H264 Example](../dev/examples/camera.md#h264-camera-feed)

## camera/jpeg

The `camera/jpeg` topic uses ROS 2's [CompressedImage](../api/sensor_msgs.md#compressedimage) schema to publish JPEG encoded camera frames.  Each frame is a complete JPEG image and can be decoded using any standard JPEG decoder.  The JPEG topic is not enabled by default as the encoder runs on the CPU, refer to the [camera configuration](../../platforms/configuration/camera.md#jpeg-streaming) to enable it and adjust the quality.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | JPEG page
Foxglove | [Compressed Image Example](https://docs.foxglove.dev/docs/visualization/panels/image)
SDK | [JPEG Example](../dev/examples/camera.md#jpeg-camera-feed)
