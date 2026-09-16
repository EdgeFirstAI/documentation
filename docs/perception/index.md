# The EdgeFirst Perception Middleware

The EdgeFirst Perception Middleware is a collection of applications and libraries used in the implementation of the modular perception stack.  The perception stack is built on [Zenoh][zenoh] and uses ROS 2 compatible CDR message formats to publish and subscribe messages on topics accessible in the stack over the network.  The middleware is open source under the Apache 2.0 license and published from the [EdgeFirstAI GitHub organization][github], the [Torizon for Maivin](../platforms/quickstart/maivin/index.md) platform ships the middleware preinstalled and preconfigured.

## Middleware Services

The Perception Middleware is modular and split into various application services, each focused on a general task.  For example the camera service is charged with interfacing with the camera and ISP (Image Signal Processor) to efficiently deliver camera frames to other services who need access to the camera.  The camera service is also responsible for encoding camera frames using the hardware video codec into H.264 video for efficient recording or remote streaming, this feature of the camera service can be configured or disabled if recording or streaming are not required.

The middleware services communicate with each other using the Zenoh networking middleware which provides a highly efficient publisher/subscriber communications stack.  This architecture is similar to ROS 2 and the services encode their messages using the ROS 2 CDR (Common Data Representation), described under [Message Schemas](#message-schemas) below.  The [Recorder](data_collection/recording.md) and [Foxglove](data_collection/foxglove.md) chapters go into more detail on how this allows efficient streaming and recording of messages and interoperability with industry standard tools.

![EdgeFirst Perception Middleware Diagram](assets/edgefirst-zenoh-diagram-light.png#only-light)
![EdgeFirst Perception Middleware Diagram](assets/edgefirst-zenoh-diagram-dark.png#only-dark)

There is no message broker in the middle.  Each service opens its own Zenoh session and the peers discover one another through multicast scouting, so what distinguishes a service is which side of the topic space it touches: some only produce topics, some consume topics and publish derived ones, and some only consume.  The `zenohd` router is the exception, it is a gateway rather than a participant and exists so applications off the device can reach the same topics, refer to the [Developer Guide](dev/index.md#remote-connections).

## Architecture

Each service handles a specific task and publishes its results on a set of [topics](topics/index.md).  The services are independent processes, a service can be stopped, reconfigured, and restarted without affecting the others, and several instances of a service can run to support multiple cameras or multiple models.

| Service | Binary | Description |
|---------|--------|-------------|
| [Camera](topics/camera.md) | `edgefirst-camera` | Interfaces with the camera and ISP to publish zero-copy camera frames along with H.264 and optional JPEG streams.  Publishes the camera intrinsics and the camera transform. |
| [Model](topics/model.md) | `edgefirst-model` | Runs a vision model on the camera frames using the NPU and publishes detection boxes, segmentation masks, tracks, and timing in a unified message. |
| [Fusion](topics/fusion.md) | `edgefirst-fusion` | Projects the radar and LiDAR point clouds onto the vision model output to classify targets, builds 3D bounding boxes and an occupancy grid, and optionally runs a RadarExp fusion model on the radar cube. |
| [Radar](topics/radar.md) | `edgefirst-radarpub` | Interfaces with the smartmicro radar over CAN and Ethernet to publish the radar point cloud, clusters, and radar cube. |
| [LiDAR](topics/lidar.md) | `edgefirst-lidarpub` | Interfaces with Robosense and Ouster LiDAR sensors to publish point clouds and clusters, along with the sensor IMU where the LiDAR provides one. |
| [IMU](topics/imu.md) | `edgefirst-imu` | Publishes the device orientation, angular velocity, and linear acceleration. |
| [NavSat](topics/navsat.md) | `edgefirst-navsat` | Publishes the GPS position from `gpsd`. |
| [Recorder](data_collection/recording.md) | `edgefirst-recorder` | Records topics into MCAP files with the schemas embedded for playback and dataset creation. |
| [Replay](data_collection/replay.md) | `edgefirst-replay` | Replays MCAP recordings onto the topics in place of the live sensors. |
| Web Server | `edgefirst-websrv` | Serves the [Web UI](../platforms/quickstart/maivin/webui.md), bridges topics to the browser over WebSockets, and provides the configuration, recording, and EdgeFirst Studio upload APIs. |
| Zenoh Router | `zenohd` | Optional gateway allowing [remote applications](dev/index.md#remote-connections) to reach the device topics from another machine.  Disabled by default. |

The services are built on a set of shared libraries which are also published from the EdgeFirst GitHub organization with Rust, C, and Python bindings.

- **[EdgeFirst Schemas][schemas]** provide the message definitions and the zero-copy CDR encoding for the ROS 2 common interfaces, the Foxglove messages, and the EdgeFirst custom messages, refer to the [API Reference](api/index.md).
- **EdgeFirst HAL** provides the tensor, image processing, decoder, and tracker building blocks used by the model and fusion services.
- **VideoStream** provides zero-copy camera frame sharing across processes along with the hardware codec interfaces.

On Torizon for Maivin the services run as systemd units under the `maivin.target` target with their configuration under `/etc/default/`, refer to the platform [Configuration](../platforms/configuration/index.md) section.  On other platforms the services can be launched in user-mode with the [EdgeFirst Launcher](launcher.md).

The services carry timing instrumentation which can be enabled at runtime to see where time goes inside each one, refer to [Profiling the Middleware](profiling.md).

## Message Schemas

Every message on every topic is encoded with the ROS 2 CDR (Common Data Representation) using the schemas published at [github.com/EdgeFirstAI/schemas][schemas].  The middleware uses the ROS 2 common interfaces and the Foxglove schemas where they apply and adds custom EdgeFirst schemas where they do not, which is what lets a recording open in Foxglove Studio and a topic reach a ROS 2 system through the [Zenoh ROS 2 DDS bridge](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds) without EdgeFirst depending on a ROS 2 installation.  Bindings are published for Rust, C, and Python.

The schemas decode by borrowing rather than by copying.  Where a conventional CDR codec walks the whole buffer and materializes every field into a new structure, `from_cdr` scans the buffer once to record a small offset table and then stops.  Field accessors read at those known offsets on demand, strings come back as slices into the original buffer, and typed numeric arrays are reinterpreted from the wire bytes in place.  The buffer is never copied or reallocated.

The practical consequence is that decode cost tracks the number of variable-length fields in a message rather than its size, so it stays flat as payloads grow.  These are decode times for the largest variant of each schema our services publish, measured on a Raspberry Pi 5 against the codecs behind the two major ROS 2 middleware vendors.

| Topic | Schema | EdgeFirst | Fast-CDR | Cyclone DDS |
|-------|--------|-----------|----------|-------------|
| `camera/h264` | [CompressedVideo](api/foxglove_msgs.md#compressedvideo), 1 MB payload | 53 ns | 122 µs | 134 µs |
| `radar/cube` | [RadarCube](api/edgefirst_msgs.md#radarcube), DRVEGRD-171 extra long | 58 ns | 3.4 ms | 3.4 ms |
| `lidar/points` | [PointCloud2](api/sensor_msgs.md#pointcloud2), Ouster 2048x10 128 beam | 123 ns | 784 µs | 819 µs |
| `fusion/lidar` | [PointCloud2](api/sensor_msgs.md#pointcloud2), Ouster points with vision classes | 124 ns | 415 µs | 437 µs |
| `model/output` | [Mask](api/edgefirst_msgs.md#mask) carried in the [Model](api/edgefirst_msgs.md#model) message, 640x640 over 8 classes | 53 ns | 28.1 µs | 26.8 µs |

A subscriber that reads a handful of fields, which is the common case, pays close to the decode cost alone.  A subscriber that walks an entire bulk payload pays for the walk either way and the advantage narrows.  The full methodology, the access and workflow patterns, and the per-schema results are in [BENCHMARKS.md][benchmarks] in the schemas repository.

## Communication

Each service opens its Zenoh session inside a namespace equal to the device hostname, so the topics are published on bare keys such as `camera/h264` and reach the network as `verdin-imx8mp-XXXXXXXX/camera/h264`.  This keeps the topics of several devices on the same network apart and lets recordings from multiple devices be merged.  Refer to [Middleware Topics](topics/index.md#hostname-namespaces) for the details and to the [Developer Guide](dev/index.md) for subscribing from your own applications.

Services run as Zenoh peers and find each other through multicast scouting, so the topics of a device are reachable on that device without any additional configuration.  Reaching them from another machine needs the `zenohd` router, which is covered under [Remote Connections](dev/index.md#remote-connections).

See the [Recording](data_collection/recording.md) and [Foxglove](data_collection/foxglove.md) sections for details on streaming, recording, and tool interoperability.

For programmatic access to EdgeFirst Studio (dataset upload, snapshots, training artifacts), see the [EdgeFirst Client](../client/index.md) documentation.

[zenoh]: https://zenoh.io/
[github]: https://github.com/EdgeFirstAI
[schemas]: https://github.com/EdgeFirstAI/schemas
[benchmarks]: https://github.com/EdgeFirstAI/schemas/blob/main/BENCHMARKS.md
