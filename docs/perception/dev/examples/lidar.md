# LiDAR Schema Example

This example will go through how to connect to the lidar topic published on your EdgeFirst Platform and how to display the information on the command line as well as through the Rerun visualizer.

!!! tip "Topic Names"

    The topics below are subscribed with their bare names, which requires the Zenoh session to be opened with the namespace set to the device hostname as shown in the [Developer Guide](../index.md#subscriber).  Subscribe with a `**/` prefix, for example `**/camera/h264`, to match the topics from a session without a namespace or from a remote device.

## LiDAR Points

Topic: [/lidar/points](../../topics/lidar.md#lidarpoints)  
Message: [Image](../../api/sensor_msgs.md#pointcloud2)
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/lidar/points.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/lidar/points.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `lidar/points` topic

=== "Python"

    ``` python
    # Create a subscriber for "lidar/points"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('lidar/points', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "lidar/points"
    let subscriber = session
        .declare_subscriber("lidar/points")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    async def points_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=points_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::PointCloud2;

    // Receive a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let pcd: PointCloud2 = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode PCD Data

The next step is to decode the PCD data. Please see [examples/pcd](pcd.md) for a guide on how to decode the PointCloud2 data.

=== "Python"

    ``` python
    def points_worker(msg):
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
    ```

=== "Rust"

    ``` rust
    let points = decode_pcd(pcd);
    ```

### Process the Data

We can now process the data. In this example we will find the values for x, y, z, and reflect.
The PCD contains x, y, z, and reflect values. The x, y, z are float32 and represent the point's location, in meters. The reflect is uint8 and represents the intensity of the reflected light.

=== "Python"

    ``` python
    pos = [[p.x, p.y, p.z] for p in points]
        rr.log("lidar/points", rr.Points3D(pos))
    ```

=== "Rust"

    ``` rust
    let x_vals: Vec<_> = points.iter().map(|p| p.x).collect();
    let y_vals: Vec<_> = points.iter().map(|p| p.y).collect();
    let z_vals: Vec<_> = points.iter().map(|p| p.z).collect();
    let reflect = points
        .iter()
        .map(|p| *p.fields.get("reflect").unwrap())
        .collect();
    ```

### Results

The command line output will appear as the following

```text
Received 24448 lidar points.
Received 24448 lidar points.
Received 24448 lidar points.
```

When displaying the results through Rerun you will see the pointcloud data gathered by the lidar.

{{ figure("assets/lidar_points.png", "LiDAR Pointcloud") }}

## LiDAR Clusters

Topic: [/lidar/clusters](../../topics/lidar.md#lidarclusters)  
Message: [PointCloud2](../../api/sensor_msgs.md#pointcloud2)
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/lidar/clusters.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/lidar/clusters.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `lidar/clusters` topic

=== "Python"

    ``` python
    # Create a subscriber for "lidar/cluster"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('lidar/clusters', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "lidar/cluster"
    let subscriber = session
        .declare_subscriber("lidar/clusters")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    async def clusters_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=clusters_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::PointCloud2;

    // Receive a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let pcd: PointCloud2 = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode PCD Data

The next step is to decode the PCD data. Please see [examples/pcd](pcd.md) for a guide on how to decode the PointCloud2 data.

=== "Python"

    ``` python
    def clusters_worker(msg):
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
    ```

=== "Rust"

    ``` rust
    let points = decode_pcd(pcd);
    ```

### Collect the Clustered Points

We will now collect all the clustered points, which are all the points with `cluster_id` above 0.

=== "Python"

    ``` python
    clusters = [p for p in points if p.cluster_id > 0]
    if not clusters:
        rr.log("lidar/clusters", rr.Points3D([], colors=[]))  
        return
    max_id = max(p.cluster_id for p in clusters)
    pos = [[p.x, p.y, p.z] for p in clusters]
    colors = [colormap(turbo_colormap, p.cluster_id / max_id)
            for p in clusters]
    rr.log("lidar/clusters", rr.Points3D(pos, colors=colors))
    ```

=== "Rust"

    ``` rust
    let clustered_points: Vec<_> = points.iter().filter(|x| x.fields.get("cluster_id") > 0.0).collect();
    ```

### Results

The command line output will appear as the following

```text
Received 24448 lidar points. 12193 are clustered
Received 24448 lidar points. 12219 are clustered
Received 24448 lidar points. 12237 are clustered
```

When displaying the results through Rerun you will see the pointcloud cluster data provided by the LiDAR.

{{ figure("assets/lidar_clusters.png", "LiDAR Clusters") }}

## Combined Example

!!! warning "Legacy Topics"

    This example subscribes to `model/boxes2d`, a legacy topic which is disabled by default on Torizon for Maivin 2026.08.  Set `DETECT_TOPIC="model/boxes2d"` in `/etc/default/model` as described in the [Model Settings](../../../platforms/configuration/model.md#topics) before running it, or adapt the boxes callback to the [`model/output`](../../topics/model.md#modeloutput) topic which carries the same `Box` entries.

This example will demonstrate how to combine the camera feed with the lidar messages to create a composite Rerun view. The main difference when using multiple messages in a script, is that we will change from waiting on the message to be received to having a callback function for when a message is received. Using the initial method, the script would hang while waiting for a message topic to be published, so if the messages are being published at different rates, the slowest message rate will limit the others.

Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/combined/camera_lidar.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/combined/mega_sample.rs)

### Setting up the subscribers

After setting up the Zenoh session, we will create a subscriber to the three topics

=== "Python"

    ``` python
    # Create the necessary subscribers
    loop = asyncio.get_running_loop()
    h264_drain = MessageDrain(loop)
    boxes2d_drain = MessageDrain(loop)
    lidar_drain = MessageDrain(loop)
    frame_size_storage = FrameSize()

    # Declare subscribers
    session.declare_subscriber('camera/h264', h264_drain.callback)
    session.declare_subscriber('model/boxes2d', boxes2d_drain.callback)
    session.declare_subscriber('lidar/clusters', lidar_drain.callback)
    ```

### Subscriber Callbacks

We will now go through the handler functions that are in use for this example. These handler functions will independently handle each of the messages received through the MessageDrain. Additionally, we will make use of a FrameSize object to communicate the frame size of the camera to the boxes and segmentation mask so they can be resized appropriately.

=== "Python"

    ``` python
    await asyncio.gather(h264_handler(h264_drain, frame_size_storage), 
                         boxes2d_handler(boxes_drain, frame_size_storage),
                         mask_handler(mask_drain, frame_size_storage, args.remote))
    ```

#### H264 Handler

The H264 handler will receive the CompressedVideo message from the MessageDrain and after initializing the required containers will pass that message to the worker, where the message will be processed and logged to Rerun.

=== "Python"

    ``` python
    async def h264_handler(drain, frame_storage):
        raw_data = io.BytesIO()
        container = av.open(raw_data, format='h264', mode='r')

        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=h264_worker, args=[msg, frame_storage, raw_data, container])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    
    def h264_worker(msg, frame_storage, raw_data, container):
        raw_data.write(msg.payload.to_bytes())
        raw_data.seek(0)
        for packet in container.demux():
            try:
                if packet.size == 0:
                    continue
                raw_data.seek(0)
                raw_data.truncate(0)
                for frame in packet.decode():
                    frame_array = frame.to_ndarray(format='rgb24')
                    frame_storage.set(frame_array.shape[1], frame_array.shape[0])
                    rr.log('/camera', rr.Image(frame_array))
            except Exception:
                continue
    ```

#### Boxes2D Handler

The Boxes2D callback will wait for a Detect message from the MessageDrain and will pass that message to the worker, where the message will be processed and logged to Rerun. The boxes logged will use tracking when available. Additionally, this handler will wait until the camera has started and logged a frame size so it knows what the height and width will be to resize the boxes.

=== "Python"

    ``` python
    async def boxes2d_handler(drain, frame_storage):
        boxes_tracked = {}
        _ = await frame_storage.get()
        while True:
            msg = await drain.get_latest()
            frame_size = await frame_storage.get()
            thread = threading.Thread(target=boxes2d_worker, args=[msg, boxes_tracked, frame_size])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()

    def boxes2d_worker(msg, boxes_tracked, frame_size):
        detection = Detect.deserialize(msg.payload.to_bytes())
        centers, sizes, labels, colors = [], [], [], []
        for box in detection.boxes:
            if box.track.id and box.track.id not in boxes_tracked:
                boxes_tracked[box.track.id] = [box.label + ": " + box.track.id[:6], list(np.random.choice(range(256), size=3))]
            if box.track.id:
                colors.append(boxes_tracked[box.track.id][1])
                labels.append(boxes_tracked[box.track.id][0])
            else:
                colors.append([0,255,0])
                labels.append(box.label)
            centers.append((int(box.center_x * frame_size[0]), int(box.center_y * frame_size[1])))
            sizes.append((int(box.width * frame_size[0]), int(box.height * frame_size[1])))
        rr.log("/camera/boxes", rr.Boxes2D(centers=centers, sizes=sizes, labels=labels, colors=colors))
    ```

#### LiDAR Handler

The LiDAR callback will receive the pointcloud message, perform post-processing on the resultant data and then be sent to Rerun.

=== "Python"

    ``` python
    async def clusters_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=clusters_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()

    def clusters_worker(msg):
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
        clusters = [p for p in points if p.cluster_id > 0]
        if not clusters:
            rr.log("/pointcloud/clusters", rr.Points3D([], colors=[]))  
            return
        max_id = max(p.cluster_id for p in clusters)
        pos = [[p.x, p.y, p.z] for p in clusters]
        colors = [colormap(turbo_colormap, p.cluster_id / max_id)
                for p in clusters]
        rr.log("/pointcloud/clusters", rr.Points3D(pos, colors=colors))
    ```

### Results

When displaying the results through Rerun you will see the combined image of the camera feed with boxes and the lidar pointcloud.

{{ figure("assets/camera_radar.png", "Camera + Radar") }}
