# Camera Topics

The camera topics are managed by the `maivin-camera` service and handles interfacing with a local camera to produce camera frames which can be shared to multiple consumers with low overhead by leveraging zero-copy through DMA buffers.  The service can also produce encoded frames in H.264 or JPEG suitable for recording or streaming to a remote device.  The following is a list of key features provided by the camera service.

- Video4Linux2 Cameras
- i.MX 8M Plus ISP
  - Using the VSI ISP driver
  - Publishes camera intrinsic parameters from ISP configuration
- Zero-Copy frame publishing using Linux [dma-buf](https://docs.kernel.org/driver-api/dma-buf.html)
- Hardware H.264 Encoder
  - VSI Hantro (i.MX 8M Plus)
  - 1080 @ 60FPS
  - 4K @ 30FPS (special extension)
- Software JPEG Encoder

The camera topic is published under the `/camera` namespace and offers the following sub-topics.  Some topics are optional and might not be available on the current system, refer to the camera service configuration documentation for details.

## /camera/info

The `/camera/info` topic publishes information about the camera using the [CameraInfo](../api/sensor_msgs.md#camerainfo) schema.  The schema provides the specifications for the camera resolution and optical parameters.

## /camera/dma

The `/camera/dma` topic uses the custom [DmaBuffer](../api/edgefirst_msgs.md#dmabuffer) EdgeFirst schema for transmitting Linux [dma-buf](https://docs.kernel.org/driver-api/dma-buf.html) descriptors.  This enables high-performance zero-copy of camera buffers between applications with trivial overhead.  A DmaBuffer provides the frame file descriptor and parent process descriptor along with the buffer resolution and format described using a [FOURCC](https://fourcc.org) code.

The mechanism for sharing buffers is for the camera service to publish its own `pid` along with the file descriptor (`fd`) of the buffer along with the buffer parameters (width, height, stride, fourcc).  When a subscriber receives the message it must first duplicate the file descriptor into its own process space, this is done using the [pidfd_getfd](https://man7.org/linux/man-pages/man2/pidfd_getfd.2.html) system call.  Once the file descriptor has been duplicated it can be used normally, either used as-is with an API which can consume a `dma-buf` or by using [mmap](https://man7.org/linux/man-pages/man2/mmap.2.html) to map the contents of the buffer into user-space.

``` mermaid
sequenceDiagram
    loop
    autonumber
    Camera Service->>Client Application: DmaBuffer(pid, fd, ...)
    Client Application-->>Linux Kernel: pidfd_open(pid, fd)
    Client Application-->>Linux Kernel: pidfd_getfd(pidfd, fd)
    Linux Kernel->>Client Application: fd duplicate
    Client Application-->>Linux Kernel: mmap(fd)
    Linux Kernel->>Client Application: ptr to camera pixels
    Client Application-->Linux Kernel: Client Application Processing
    Client Application-->>Linux Kernel: munmap(ptr)
    Client Application-->>Linux Kernel: close(fd)
    Client Application-->>Linux Kernel: close(pidfd)
    end
```

1. Camera service publishes a DmaBuffer for each frame received from the camera.
2. Client application calls `pidfd_open(pid, 0)` to acquire a file descriptor that refers to the camera service process.
3. Client application calls `pidfd_getfd(pidfd, fd, 0)` to acquire a local duplicate of the camera buffer file descriptor.
4. A new file descriptor is returned, to release the `dma-buf` object we will need to call `close(fd)` later.
5. Client application calls `mmap(fd, ...)` to acquire a local pointer to the camera buffer's pixel data.
6. A read-only pointer is returned to the client application, it will need to be released using `munmap(ptr)` later.
7. Client application processes the pixel data.
8. Client application calls `munmap(ptr)` to free the mapped buffer.
9. Client application calls `close(fd)` to release the `dma-buf` object.
10. Client application calls `close(pidfd)` to release file descriptor for the camera service process.

!!! tip "Permission Denied Errors"

    The client application will not be able to call pidfd_getfd if the client application runs at a lower permission level than the camera service. If this error occurs, try running the client application as `sudo` or as a service.

!!! tip "Mapping DMA Buffers"

    Mapping DMA buffers into user-space requires additional synchronization primitives around accesses.  We cover these details in our camera sample application.  Further details are documented in the Linux Kernel Manual under [CPU Access to DMA Buffer Objects](https://docs.kernel.org/driver-api/dma-buf.html#cpu-access-to-dma-buffer-objects).

## /camera/h264

The `/camera/h264` topic uses Foxglove's [CompressedVideo](../api/foxglove_msgs.md#compressedvideo) schema to publish h.264 encoded video frames.  The h.264 encoder uses key-frames, I-Frames, at a typical rate of 1Hz with the frames in-between encoded as P/B-Frames.  The decoder requires an initial I-Frame before it can decode additional frames.  This is typically handled transparently but means when sending `CompressedVideo` data to the h.264 decoder it could take up to a second until valid output is produced.

**Usage** | **Link**
:------------------:|:------------------:
Web UI | []()
Foxglove | [CompressedVideo Example](../data_collection/foxglove.md#viewing-detection-messages)
SDK | [H264 Example](../dev/examples/camera.md#h264-camera-feed)

## /camera/jpeg

The `/camera/jpeg` topic uses ROS2's [CompressedImage](../api/sensor_msgs.md#compressedimage) schema to publish JPEG encoded camera frames.  Each frame is a complete JPEG image and can be decoded using any standard JPEG decoder. The JPEG topic will not be enabled by default. In order to enable the JPEG topic, please follow the guide noted in [configuration](../../platforms/configuration/camera.md#h264-streaming)

**Usage** | **Link**
:------------------:|:------------------:
Web UI | []()
Foxglove | [Compressed Image Example]()
SDK | [JPEG Example](../dev/examples/camera.md#jpeg-camera-feed)
