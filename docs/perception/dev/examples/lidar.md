# LIDAR Schema Example

This example will go through how to connect to the lidar topic published on your EdgeFirst Platform and how to display the information on the command line as well as through the Rerun visualizer.


## Lidar Points
Topic: [/lidar/points](../../topics/lidar.md#lidarpoints)  
Message: [Image](../../api/sensor_msgs.md#pointcloud2)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `lidar/points` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/lidar/points"
    subscriber = session.declare_subscriber('rt/lidar/points')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/lidar/points"
    let subscriber = session
        .declare_subscriber("rt/lidar/points")
        .await
        .unwrap();
    ```

### Recieve a message

We can now recieve a message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import PointCloud2

    # Recieve a message
    msg = subscriber.recv()

    # deserialize message
    pcd = PointCloud2.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::PointCloud2;

    // Recieve a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let pcd: PointCloud2 = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode PCD Data

The next step is to decode the PCD data. Please see [examples/pcd](./pcd.md) for a guide on how to decode the PointCloud2 data.


=== "Python"

    ``` python
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
    x_vals = [p.x for p in points]
    y_vals = [p.y for p in points]
    z_vals = [p.z for p in points]
    reflect = [p.fields["reflect"] for p in points]
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
```
Recieved 24448 lidar points.
Recieved 24448 lidar points.
Recieved 24448 lidar points.
```

When displaying the results through Rerun you will see the pointcloud data gathered by the lidar.
![alt text](assets/lidar_points.png)

## Lidar Clusters
Topic: [/lidar/clusters](../../topics/lidar.md#lidarclusters)  
Message: [PointCloud2](../../api/sensor_msgs.md#pointcloud2)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `lidar/clusters` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/lidar/cluster"
    subscriber = session.declare_subscriber('rt/lidar/clusters')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/lidar/cluster"
    let subscriber = session
        .declare_subscriber("rt/lidar/clusters")
        .await
        .unwrap();
    ```

### Recieve a message

We can now recieve a message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import PointCloud2

    # Recieve a message
    msg = subscriber.recv()

    # deserialize message
    pcd = PointCloud2.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::PointCloud2;

    // Recieve a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let pcd: PointCloud2 = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode PCD Data

The next step is to decode the PCD data. Please see [examples/pcd](./pcd.md) for a guide on how to decode the PointCloud2 data.


=== "Python"

    ``` python
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
    clustered_points = [p for p in points if p.fields["cluster_id"] > 0]
    ```

=== "Rust"

    ``` rust
    let clustered_points: Vec<_> = points.iter().filter(|x| x.fields.get("cluster_id") > 0.0).collect();
    ```

### Results
The command line output will appear as the following
```
Recieved 24448 lidar points. 12193 are clustered
Recieved 24448 lidar points. 12219 are clustered
Recieved 24448 lidar points. 12237 are clustered
```

When displaying the results through Rerun you will see the pointcloud cluster data provided by the LiDAR.
![alt text](assets/lidar_clusters.png)

## Lidar Depth
Topic: [/lidar/depth](../../topics/lidar.md#lidardepth)  
Message: [Image](../../api/sensor_msgs.md#image)


### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `lidar/depth` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/lidar/depth"
    subscriber = session.declare_subscriber('rt/lidar/depth')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/lidar/depth"
    let subscriber = session
        .declare_subscriber("rt/lidar/depth")
        .await
        .unwrap();
    ```

### Recieve a message

We can now recieve a message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import Image

    # Recieve a message
    msg = subscriber.recv()

    # deserialize message
    depth = Image.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::Image;

    // Recieve a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let depth: Image = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode Image Data

Because the depth image is `mono16` encoded, we need to decode the byte array into an array of u16 integers.

=== "Python"

    ``` python
    # Process depth image
    import struct
    assert depth.encoding == "mono16"
    endian_format = ">" if depth.is_bigendian else "<"
    depth_vals = list(struct.unpack(
        f"{endian_format}{depth.width*depth.height}H", depth.data))
    ```

=== "Rust"

    ``` rust
    // Process depth image
    assert_eq!(depth.encoding, "mono16");
    let u16_from_bytes = if depth.is_bigendian > 0 {
        u16::from_be_bytes
    } else {
        u16::from_le_bytes
    };
    let depth_vals: Vec<u16> = depth
        .data
        .chunks_exact(2)
        .map(|a| u16_from_bytes([a[0], a[1]]))
        .collect();
    ```

### Process the Data
We can now process the data. In this example we will reshape the depth values into an image. The image will be in L8 format, so we need
to divide by 256.

=== "Python"

    ``` python
    data = (np.array(depth_vals).reshape((depth.height, depth.width)) / 256).astype(np.uint8)
    rerun.log("lidar/depth", rr.Image(data))
    ```

=== "Rust"

    ``` rust
    let img: Vec<_> = depth_vals.iter().map(|f| (f / 256) as u8).collect();
    let img = rerun::Image::from_l8(img, [depth.width, depth.height]);
    rerun_rec.log("lidar/depth", &img)?;
    ```

### Results
The command line output will appear as the following
```
Recieved 382x64 depth image.
Recieved 382x64 depth image.
Recieved 382x64 depth image.
```

When displaying the results through Rerun you will see a depth map of what the lidar can see.
![alt text](assets/lidar_depth.png)

## Lidar Reflect
Topic: [/lidar/reflect](../../topics/lidar.md#lidarreflect)  
Message: [Image](../../api/sensor_msgs.md#image)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `lidar/reflect` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/lidar/reflect"
    subscriber = session.declare_subscriber('rt/lidar/reflect')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/lidar/reflect"
    let subscriber = session
        .declare_subscriber("rt/lidar/reflect")
        .await
        .unwrap();
    ```

### Recieve a message

We can now recieve a message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import Image

    # Recieve a message
    msg = subscriber.recv()

    # deserialize message
    reflect = Image.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::Image;

    // Recieve a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let reflect: Image = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode Image Data

Because the reflect image is `mono8` encoded, we don't need to decode the byte array.

=== "Python"

    ``` python
    # Process reflect image
    assert reflect.encoding == "mono8"
    reflect_vals = reflect.data
    ```

=== "Rust"

    ``` rust
    // Process reflect image
    assert_eq!(reflect.encoding, "mono8");
    let reflect_vals = reflect.data.clone();
    ```

### Process the Data
We can now process the data. In this example we will find the maximum and minimum reflect values.

=== "Python"

    ``` python
    min_reflect_mm = min(reflect_vals)
    max_reflect_mm = max(reflect_vals)
    ```

=== "Rust"

    ``` rust
    let min_reflect_mm = *reflect_vals.iter().min().unwrap();
    let max_reflect_mm = *reflect_vals.iter().max().unwrap();
    ```

### Results
The command line output will appear as the following
```
Recieved 382x64 reflect image. reflect: [0, 175]
Recieved 382x64 reflect image. reflect: [0, 166]
Recieved 382x64 reflect image. reflect: [0, 181]
```

When displaying the results through Rerun you will see the reflection data gathered by the lidar.
![alt text](assets/lidar_reflect.png)

## Combined Example

This example will demonstrate how to combine the camera feed with the lidar messages to create a composite Rerun view. The main difference when using multiple messages in a script, is that we will change from waiting on the message to be received to having a callback function for when a message is received. Using the initial method, the script would hang while waiting for a message topic to be published, so if the messages are being published at different rates, the slowest message rate will limit the others.

Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/combined/camera_lidar.py) 

### Setting up the subscribers

After setting up the Zenoh session, we will create a subscriber to the three topics

=== "Python"

    ``` python
    # Create the necessary subscribers
    cam_subscriber = session.declare_subscriber('rt/camera/h264', h264_callback)
    boxes2d_subscriber = session.declare_subscriber('rt/model/boxes2d', boxes2d_callback)
    lidar_clusters_subscriber = session.declare_subscriber('rt/lidar/clusters', lidar_clusters_callback)
    ```

### Subscriber Callbacks
We will now go through the callback functions that are in use for this example. These callback functions will make use of a global variable frame size to allow the script to properly resize the boxes to overlap the camera feed correctly. Each callback will receive the Zenoh message as the argument.

=== "Python"

    ``` python
    raw_data = io.BytesIO() # Necessary for H264 decoding
    container = av.open(raw_data, format='h264', mode='r') # Necessary for H264 decoding
    frame_size = []
    ```

#### H264 Callback
The H264 callback will receive the CompressedVideo message and decode it, loop through each frame received and log those frames to Rerun in addition to updating frame size.

=== "Python"

    ``` python
    def h264_callback(msg):
        global frame_size
        raw_data.write(msg.payload.to_bytes())
        raw_data.seek(0)
        for packet in container.demux():
            try:
                if packet.size == 0:  # Skip empty packets
                    continue
                raw_data.seek(0)
                raw_data.truncate(0)
                for frame in packet.decode():  # Decode video frames
                    frame_array = frame.to_ndarray(format='rgb24')  # Convert frame to numpy array
                    frame_size = [frame_array.shape[1], frame_array.shape[0]]
                    rr.log('camera', rr.Image(frame_array))
            except Exception:  # Handle exceptions
                continue  # Continue processing next packets
    ```

#### Boxes2D Callback
The Boxes2D callback will receive the Detect message, loop through all detections found and then create lists of the centers and sizes received properly scaled by the frame size that was determined from the camera feed.

=== "Python"

    ``` python
    def boxes2d_callback(msg):
        detection = Detect.deserialize(msg.payload.to_bytes())    
        for box in detection.boxes:
            centers.append((int(box.center_x * frame_size[0]), int(box.center_y * frame_size[1])))
            sizes.append((int(box.width * frame_size[0]), int(box.height * frame_size[1])))
            print(centers)
            print(sizes)
            labels.append(box.label)
        rr.log("camera/boxes", rr.Boxes2D(centers=centers, sizes=sizes, labels=labels))
    ```

#### Lidar Callback
The Lidar callback will receive the pointcloud message, perform post-processing on the resultant data and then be sent to Rerun.

=== "Python"

    ``` python
    def lidar_clusters_callback(msg):
        from edgefirst.schemas.sensor_msgs import PointCloud2
        from edgefirst.schemas import decode_pcd, colormap, turbo_colormap
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
        clusters = [p for p in points if p.id > 0]
        max_id = max(max([p.id for p in clusters]), 1)
        pos = [[p.x, p.y, p.z] for p in clusters]
        colors = [colormap(turbo_colormap, p.id/max_id) for p in clusters]
        rr.log("/pointcloud/lidar/clusters", rr.Points3D(pos, colors=colors))
    ```

### Results
When displaying the results through Rerun you will see the combined image of the camera feed with boxes and the lidar pointcloud.
![alt text](assets/camera_radar.png)