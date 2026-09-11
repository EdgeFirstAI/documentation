# Developer Guide

This is the EdgeFirst Developer's Guide.  In this guide we will walk you through the API behind the EdgeFirst Middleware, before reading this guide you should be familiar with the general architecture of the middleware so you can understand how the services fit together and the topics that bind them.

The EdgeFirst Middleware examples are provided in Python and Rust (C/C++ Coming Soon!) and you can toggle the documentation for your preferred language throughout the tutorial.

!!! note Running Remotely

    Some of the examples, such as those using the zero-copy camera frames, cannot be run remotely; these will be called out with a note.

## Connecting to Zenoh

The EdgeFirst Middleware services communicate over [Zenoh](https://zenoh.io), and every example in this guide can be run either directly on a device running the EdgeFirst Middleware or remotely from a PC running Windows, Mac, or Linux.

### Local Connections

When an example runs on the same device as the EdgeFirst Middleware, Zenoh's peer-to-peer multicast scouting automatically discovers the other services running on that device.  There's nothing to configure, just run the example and its topics are found automatically, this is why the samples "just work" when run on-target.

### Remote Connections

To connect from a separate PC you need a `zenohd` router running on the target device to bridge the connection, since multicast scouting does not typically cross networks.  Every sample accepts a `--remote` argument (or `--connect` for the [Listing Topics](#listing-topics) example) where you provide the target device's address, for example `--remote 10.1.1.10:7447` to connect over TCP using the default Zenoh port.

!!! tip "Enable the Zenohd Router"

    The `zenohd` router allows remote connections to the device so you can follow these tutorials from a PC.
    Enable it on the target device with `sudo systemctl enable --now zenohd`.

!!! warning "Security Warning"

    The default configuration for the `zenohd` service does not enable any authentication or encryption.
    Make sure you follow the [Zenoh TLS Guide](https://zenoh.io/docs/manual/tls/) if you're running the
    `zenohd` on an untrusted network.

!!! tip "Hostname Namespaces"

    The EdgeFirst services publish inside a Zenoh namespace equal to the device hostname, so the topic `camera/h264` is `verdin-imx8mp-XXXXXXXX/camera/h264` on the wire.  The examples open their session with the namespace set to the hostname when running on the device and use the bare topic names.  When running remotely, set the namespace to the hostname of the target device or subscribe with a `**/` wildcard prefix.  Refer to [Middleware Topics](../topics/index.md#hostname-namespaces).  The samples repository is being updated for the namespaces, samples still subscribing to `rt/...` topics need the prefix removed.

## Installation

Whether running the examples on the target running the EdgeFirst Middleware or a PC connected to one you'll need to download the [EdgeFirst Samples](https://github.com/EdgeFirstAI/samples) to follow along with this guide.  This provides sample code in Python and Rust as well as the appropriate setup scripts to install the required dependencies.

```bash
git clone https://github.com/EdgeFirstAI/samples.git
```

You'll now have all the samples cloned locally (or remotely) and can now move onto the various sections outlining the specific services and samples demonstrating how to interface with them.

## Listing Topics

This is the closest to the "Hello, World!" example, discovering and printing out the available topics.  We'll cover the highlights from the full samples available at the [EdgeFirst Samples](https://github.com/EdgeFirstAI/samples.git) repository.

=== "Python"

    !!! tip "Complete Python Sample"

        [https://github.com/EdgeFirstAI/samples/blob/main/edgefirst/samples/list-topics.py](https://github.com/EdgeFirstAI/samples/blob/main/edgefirst/samples/list-topics.py)

=== "Rust"

    !!! tip "Complete Rust Sample"
    
        [https://github.com/EdgeFirstAI/samples/blob/main/src/list-topics.rs](https://github.com/EdgeFirstAI/samples/blob/main/src/list-topics.rs)

### Imports

For this example the `zenoh` import is key as we are simply going to be listing the available topics.  The other imports in the full sample are for argument parsing and handling timeouts.

=== "Python"

    ```python
    import zenoh
    ```

=== "Rust"

    !!! note

        The Rust sample doesn't use any explicit imports for Zenoh.

### Subscriber

Open a Zenoh session then declare a subscriber for the `**` key expression which matches every available topic.  Without a session namespace the keys received include the hostname namespace of the publishing device, which makes this example useful for discovering the devices on the network as well as their topics.

=== "Python"

    ```python
    # Create the default Zenoh configuration and if the connect argument is
    # provided set the mode to client and add the target to the endpoints.
    config = zenoh.Config()
    if args.connect is not None:
        config.insert_json5("mode", "'client'")
        config.insert_json5("connect", '{"endpoints": ["%s"]}' % args.connect)
    session = zenoh.open(config)

    # Create a subscriber for all topics matching the pattern "**"
    subscriber = session.declare_subscriber('**')
    ```

=== "Rust"

    ```rust
    // Create the default Zenoh configuration and if the connect argument is
    // provided set the mode to client and add the target to the endpoints.
    let mut config = Config::default();
    if let Some(connect) = args.connect {
        config.insert_json5("mode", "client").unwrap();
        config.insert_json5("connect/endpoints", &connect).unwrap();
    }
    let session = zenoh::open(config).await.unwrap();

    // Create a subscriber for all topics matching the pattern "**"
    let subscriber = session.declare_subscriber("**").await.unwrap();
    ```

The other examples subscribe to specific topics.  They set the session namespace to the hostname so that the bare topic names match the services running on the same device, exactly as the services themselves do.

=== "Python"

    ```python
    import socket

    config = zenoh.Config()
    config.insert_json5("namespace", '"%s"' % socket.gethostname())
    session = zenoh.open(config)
    ```

=== "Rust"

    ```rust
    let hostname = gethostname::gethostname().to_string_lossy().into_owned();
    let mut config = Config::default();
    config.insert_json5("namespace", &format!("\"{hostname}\"")).unwrap();
    let session = zenoh::open(config).await.unwrap();
    ```

### Receive Messages

In a loop we now receive messages and print the topic name and schema.  The complete example includes some noise filtering and an optional timeout.

=== "Python"

    ```python
    while True:
        # Receive the next available message.
        msg = subscriber.recv()
        
        # Capture the message encoding MIME type then split on the first ';'
        # to get the schema.
        schema = str(msg.encoding).split(';', maxsplit=1)[-1]
        print("topic: %s → %s" % (topic, schema))
    ```

=== "Rust"

    ```rust
    while let Ok(msg) = subscriber.recv() {        
        // Capture the message encoding MIME type then split on the first ';' to get the schema
        let schema = msg.encoding().to_string();
        let schema = schema.splitn(2, ';').last().unwrap_or_default();
        println!("topic: {} → {}", msg.key_expr(), schema);
    }
    ```

### Results

Running this sample on the target will list the available topics.  The example can list topics on a remote device by providing the address of a device with an available zenohd router.

!!! tip "Remote Targets"

    If running these examples remotely you will need to provide the remote endpoint, for example if your target device has the address 10.1.1.10 then you would use `--remote tcp/10.1.1.10:7447` to connect using TCP on the default Zenoh port.

=== "Python"

    ```bash
    $ python -m edgefirst.samples.list-topics
    topic: verdin-imx8mp-15141091/imu → sensor_msgs/msg/Imu
    topic: verdin-imx8mp-15141091/camera/h264 → foxglove_msgs/msg/CompressedVideo
    topic: verdin-imx8mp-15141091/camera/frame → edgefirst_msgs/msg/CameraFrame
    topic: verdin-imx8mp-15141091/camera/info → sensor_msgs/msg/CameraInfo
    topic: verdin-imx8mp-15141091/model/output → edgefirst_msgs/msg/Model
    topic: verdin-imx8mp-15141091/model/info → edgefirst_msgs/msg/ModelInfo
    topic: verdin-imx8mp-15141091/radar/cube → edgefirst_msgs/msg/RadarCube
    topic: verdin-imx8mp-15141091/radar/targets → sensor_msgs/msg/PointCloud2
    topic: verdin-imx8mp-15141091/radar/clusters → sensor_msgs/msg/PointCloud2
    topic: verdin-imx8mp-15141091/tf_static → geometry_msgs/msg/TransformStamped
    topic: verdin-imx8mp-15141091/gps → sensor_msgs/msg/NavSatFix
    topic: verdin-imx8mp-15141091/radar/info → edgefirst_msgs/msg/RadarInfo
    ```

=== "Rust"

    ```bash
    $ cargo run --bin list-topics
    topic: verdin-imx8mp-15141091/imu → sensor_msgs/msg/Imu
    topic: verdin-imx8mp-15141091/camera/h264 → foxglove_msgs/msg/CompressedVideo
    topic: verdin-imx8mp-15141091/camera/frame → edgefirst_msgs/msg/CameraFrame
    topic: verdin-imx8mp-15141091/camera/info → sensor_msgs/msg/CameraInfo
    topic: verdin-imx8mp-15141091/model/output → edgefirst_msgs/msg/Model
    topic: verdin-imx8mp-15141091/model/info → edgefirst_msgs/msg/ModelInfo
    topic: verdin-imx8mp-15141091/radar/cube → edgefirst_msgs/msg/RadarCube
    topic: verdin-imx8mp-15141091/radar/targets → sensor_msgs/msg/PointCloud2
    topic: verdin-imx8mp-15141091/radar/clusters → sensor_msgs/msg/PointCloud2
    topic: verdin-imx8mp-15141091/tf_static → geometry_msgs/msg/TransformStamped
    topic: verdin-imx8mp-15141091/gps → sensor_msgs/msg/NavSatFix
    topic: verdin-imx8mp-15141091/radar/info → edgefirst_msgs/msg/RadarInfo
    ```

That's it!  The next examples will dive into the topic schemas and how to parse the message contents and provide examples on visualizing the results using the [Rerun](https://rerun.io) tool.
