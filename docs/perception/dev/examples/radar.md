# Radar Schema Example

This example will go through how to connect to the radar topic published on your EdgeFirst Platform and how to display the information on the command line as well as through the Rerun visualizer.


## Radar Targets
Topic: [/radar/targets](../../topics/radar.md#radartargets)  
Message: [PointCloud2](../../api/sensor_msgs.md#pointcloud2)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `radar/targets` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/radar/targets"
    subscriber = session.declare_subscriber('rt/radar/targets')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/radar/targets"
    let subscriber = session
        .declare_subscriber("rt/radar/targets")
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

    // Create a subscriber for "rt/radar/cluster"
    let msg = subscriber.recv().unwrap()

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

We can now process the data. In this example we will find the maximum and minimum values for x, y, z, speed, power, and rcs

=== "Python"

    ``` python
    min_x = min([p.x for p in points])
    max_x = max([p.x for p in points])

    min_y = min([p.y for p in points])
    max_y = max([p.y for p in points])

    min_z = min([p.z for p in points])
    max_z = max([p.z for p in points])

    min_speed = min([p.fields["speed"] for p in points])
    max_speed = max([p.fields["speed"] for p in points])

    min_power = min([p.fields["power"] for p in points])
    max_power = max([p.fields["power"] for p in points])

    min_rcs = min([p.fields["rcs"] for p in points])
    max_rcs = max([p.fields["rcs"] for p in points])
    ```

=== "Rust"

    ``` rust
    let min_x = points.iter().map(|p| p.x).fold(f64::INFINITY, f64::min);
    let max_x = points.iter().map(|p| p.x).fold(f64::NEG_INFINITY, f64::max);

    let min_y = points.iter().map(|p| p.y).fold(f64::INFINITY, f64::min);
    let max_y = points.iter().map(|p| p.y).fold(f64::NEG_INFINITY, f64::max);

    let min_z = points.iter().map(|p| p.z).fold(f64::INFINITY, f64::min);
    let max_z = points.iter().map(|p| p.z).fold(f64::NEG_INFINITY, f64::max);

    let min_speed = points
        .iter()
        .map(|p| *p.fields.get("speed").unwrap())
        .fold(f64::INFINITY, f64::min);
    let max_speed = points
        .iter()
        .map(|p| *p.fields.get("speed").unwrap())
        .fold(f64::NEG_INFINITY, f64::max);

    let min_power = points
        .iter()
        .map(|p| *p.fields.get("power").unwrap())
        .fold(f64::INFINITY, f64::min);
    let max_power = points
        .iter()
        .map(|p| *p.fields.get("power").unwrap())
        .fold(f64::NEG_INFINITY, f64::max);

    let min_rcs = points
        .iter()
        .map(|p| *p.fields.get("rcs").unwrap())
        .fold(f64::INFINITY, f64::min);
    let max_rcs = points
        .iter()
        .map(|p| *p.fields.get("rcs").unwrap())
        .fold(f64::NEG_INFINITY, f64::max);
    ```

### Results
The command line output will appear as the following
```
Recieved 23 radar points. Values: x: [2.04, 9.48]       y: [-2.99, 4.74]        z: [-2.07, 2.09]        rcs: [-13.80, 17.60]
Recieved 23 radar points. Values: x: [2.04, 9.47]       y: [-2.99, 4.21]        z: [-2.11, 2.09]        rcs: [-13.80, 17.60]
Recieved 23 radar points. Values: x: [2.04, 9.47]       y: [-2.97, 4.22]        z: [-2.09, 2.07]        rcs: [-14.00, 17.60]
```

When displaying the results through Rerun you will see the pointcloud radar data.
![alt text](assets/radar_targets.png)


## Radar Clusters
Topic: [/radar/clusters](../../topics/radar.md#radarclusters)  
Message: [PointCloud2](../../api/sensor_msgs.md#pointcloud2)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `radar/clusters` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/radar/cluster"
    subscriber = session.declare_subscriber('rt/radar/clusters')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/radar/cluster"
    let subscriber = session
        .declare_subscriber("rt/radar/clusters")
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

    // Create a subscriber for "rt/radar/cluster"
    let msg = subscriber.recv().unwrap()

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
Recieved 137 radar points. 134 are clustered
Recieved 136 radar points. 133 are clustered
Recieved 138 radar points. 135 are clustered
```

When displaying the results through Rerun you will see the cluster data.
![alt text](assets/radar_clusters.png)

## Radar Info
Topic: [/radar/info](../../topics/radar.md#radarinfo)  
Message: [RadarInfo](../../api/edgefirst_msgs.md#radarinfo)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `radar/info` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/radar/info"
    subscriber = session.declare_subscriber('rt/radar/info')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/radar/info"
    let subscriber = session
        .declare_subscriber("rt/radar/info")
        .await
        .unwrap();
    ```

### Recieve a message

We can now recieve a message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import RadarInfo

    # Recieve a message
    msg = subscriber.recv()

    # deserialize message
    radar_info = RadarInfo.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::RadarInfo;

    // Recieve a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let radar_info: RadarInfo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The RadarInfo message contains information about the radar configuration. Various fields can be accessed to view the radar's configuration.


=== "Python"

    ``` python
    # Access radar configuration
    center_frequency = radar_info.center_frequency
    frequency_sweep = radar_info.frequency_sweep
    range_toggle = radar_info.range_toggle
    detection_sensitivity = radar_info.detection_sensitivity
    cube = radar_info.cube
    ```

=== "Rust"

    ``` rust
    // Access radar configuration
    let center_frequency = radar_info.center_frequency;
    let frequency_sweep = radar_info.frequency_sweep;
    let range_toggle = radar_info.range_toggle;
    let detection_sensitivity = radar_info.detection_sensitivity;
    let cube = radar_info.cube;
    ```

### Results
The command line output will appear as the following
```
The radar configuration is: center frequency: low   frequency sweep: ultra-short   range toggle: off   detection sensitivity: high   sending cube: true
The radar configuration is: center frequency: low   frequency sweep: ultra-short   range toggle: off   detection sensitivity: high   sending cube: true
The radar configuration is: center frequency: low   frequency sweep: ultra-short   range toggle: off   detection sensitivity: high   sending cube: true
```

When displaying the results through Rerun you will see a log of the radar configuration.
![alt text](assets/radar_info.png)

## Radar Cube
Topic: [/radar/cube](../../topics/radar.md#radarcube)  
Message: [RadarCube](../../api/edgefirst_msgs.md#radarcube)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `radar/cube` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/radar/cube"
    subscriber = session.declare_subscriber('rt/radar/cube')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/radar/cube"
    let subscriber = session
        .declare_subscriber("rt/radar/cube")
        .await
        .unwrap();
    ```

### Recieve a message

We can now recieve a message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import RadarCube

    # Recieve a message
    msg = subscriber.recv()

    # deserialize message
    radar_cube = RadarCube.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::RadarCube;

    // Recieve a message
    let msg = subscriber.recv().unwrap()

    // Deserialize message
    let radar_cube: RadarCube = cdr::deserialize(&msg.payload().to_bytes())?;
    ```
### Process the Data

The RadarCube message contains data from the RadarCube.

=== "Python"

    ``` python
    # Access radar cube information
    shape = radar_cube.shape
    cube = radar_cube.cube
    ```

=== "Rust"

    ``` rust
    // Access radar cube information
    let shape = radar_cube.shape;
    let cube = radar_cube.cube;
    ```

### Results
The command line output will appear as the following
```
The radar cube has shape: [2, 200, 4, 256]
The radar cube has shape: [2, 200, 4, 256]
The radar cube has shape: [2, 200, 4, 256]
```

When displaying the results through Rerun you will see the radar cube displayed.
![alt text](assets/radar_cube.png)

## Combined Example

This example will demonstrate how to combine the camera feed with the radar messages to create a composite Rerun view. The main difference when using multiple messages in a script, is that we will change from waiting on the message to be received to having a callback function for when a message is received. Using the initial method, the script would hang while waiting for a message topic to be published, so if the messages are being published at different rates, the slowest message rate will limit the others.

Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/combined/camera_radar.py) 

### Setting up the subscribers

After setting up the Zenoh session, we will create a subscriber to the three topics

=== "Python"

    ``` python
    # Create the necessary subscribers
    cam_subscriber = session.declare_subscriber('rt/camera/h264', h264_callback)
    boxes2d_subscriber = session.declare_subscriber('rt/model/boxes2d', boxes2d_callback)
    radar_clusters_subscriber = session.declare_subscriber('rt/radar/clusters', radar_clusters_callback)
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

#### Radar Callback
The Radar callback will receive the pointcloud message, perform post-processing on the resultant data and then be sent to Rerun.

=== "Python"

    ``` python
    def radar_clusters_callback(msg):
        from edgefirst.schemas.sensor_msgs import PointCloud2
        from edgefirst.schemas import decode_pcd, colormap, turbo_colormap
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
        clusters = [p for p in points if p.id > 0]
        max_id = max(max([p.id for p in clusters]), 1)
        pos = [[p.x, p.y, p.z] for p in clusters]
        colors = [colormap(turbo_colormap, p.id/max_id) for p in clusters]
        rr.log("/pointcloud/radar/clusters", rr.Points3D(pos, colors=colors))
    ```

### Results
When displaying the results through Rerun you will see the combined image of the camera feed with boxes and the radar pointcloud.
![alt text](assets/camera_radar.png)