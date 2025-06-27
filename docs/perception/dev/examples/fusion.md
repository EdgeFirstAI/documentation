# Fusion Schema Examples

These examples demonstrate how to connect to various fusion topics published on your EdgeFirst Platform and how to display the information through the command line.

## /fusion/occupancy

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/occupancy` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/occupancy"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/fusion/occupancy', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/occupancy"
    let subscriber = session
        .declare_subscriber("rt/fusion/occupancy")
        .await
        .unwrap();
    ```

### Receive a message

We can now await a message from that subscriber. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages.

=== "Python"

    ``` python
    async def occupancy_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=occupancy_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::fusion_msgs::Occupancy;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let occupancy: Occupancy = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Occupancy message contains occupancy grid data. You can log the data through the following

=== "Python"

    ``` python
    def occupancy_worker(msg):
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
        if not points:
            rr.log("fusion/occupancy", rr.Points3D(positions=[], colors=[])) 
            return
        max_class = max(max([p.vision_class for p in points]), 1)
        pos = [[p.x, p.y, p.z] for p in points]
        colors = [
            colormap(turbo_colormap, p.vision_class/max_class) for p in points]
        rr.log("fusion/occupancy", rr.Points3D(positions=pos, colors=colors))
    ```

=== "Rust"

    ``` rust
    // Access occupancy parameters
    let width = occupancy.width;
    let height = occupancy.height;
    let resolution = occupancy.resolution;
    let data = occupancy.data;  // Occupancy grid data
    ```

### Results
When displaying the results through Rerun you will see the Occupancy pointcloud.
![alt text](assets/fusion_occupancy.png)

## /fusion/model_output

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/model_output` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/model_output"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)

    session.declare_subscriber('rt/fusion/model_output', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/model_output"
    let subscriber = session
        .declare_subscriber("rt/fusion/model_output")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will set it up for processing.

=== "Python"

    ``` python
    async def model_output_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=model_output_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::fusion_msgs::ModelOutput;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let output: ModelOutput = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The ModelOutput message contains fused model output data. You can log the data through the following

=== "Python"

    ``` python
    def model_output_worker(msg):
        mask = Mask.deserialize(msg.payload.to_bytes())
        np_arr = np.asarray(mask.mask, dtype=np.uint8)
        np_arr = np.reshape(np_arr, [mask.height, mask.width, -1])
        np_arr = np.argmax(np_arr, axis=2)
        rr.log(
            "/", rr.AnnotationContext([
                (0, "background", (0, 0, 0)),
                (1, "person", (255, 0, 0))]))
        rr.log("mask", rr.SegmentationImage(np_arr))
    ```

=== "Rust"

    ``` rust
    // Access model output parameters
    let timestamp = output.timestamp;
    let boxes = output.boxes;  // 2D bounding boxes
    let masks = output.masks;  // Segmentation masks
    ```

## /fusion/mask_output/tracked

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/mask_output/tracked` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/mask_output/tracked"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/fusion/model_output/tracked', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/mask_output/tracked"
    let subscriber = session
        .declare_subscriber("rt/fusion/mask_output/tracked")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will set it up for processing.

=== "Python"

    ``` python
    async def model_output_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=model_output_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::fusion_msgs::MaskOutputTracked;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let tracked: MaskOutputTracked = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The MaskOutputTracked message contains fused model output data. You can log the data through the following

=== "Python"

    ``` python
    def model_output_worker(msg):
        mask = Mask.deserialize(msg.payload.to_bytes())
        np_arr = np.asarray(mask.mask, dtype=np.uint8)
        np_arr = np.reshape(np_arr, [mask.height, mask.width, -1])
        np_arr = np.argmax(np_arr, axis=2)
        rr.log(
            "/", rr.AnnotationContext([
                (0, "background", (0, 0, 0)),
                (1, "person", (255, 0, 0))]))
        rr.log("mask", rr.SegmentationImage(np_arr))
    ```

=== "Rust"

    ``` rust
    // Access tracked mask parameters
    let timestamp = tracked.timestamp;
    let track_id = tracked.track_id;
    let mask = tracked.mask;  // Segmentation mask
    ```

## /fusion/radar

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/radar` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/radar"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/fusion/radar', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/radar"
    let subscriber = session
        .declare_subscriber("rt/fusion/radar")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will set it up for processing.

=== "Python"

    ``` python
    async def radar_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=radar_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    edgefirst_schemas::sensor_msgs::PointCloud2;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let pcd: PointCloud2 = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode PCD Data

The next step is to decode the PCD data. Please see [examples/pcd](./pcd.md) for a guide on how to decode the PointCloud2 data.


=== "Python"

    ``` python
    def radar_worker(msg):
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::decode_pcd;
    let points = decode_pcd(pcd);
    ```

### Process the Data

We can now process the data. In this example we will find the maximum and minimum values for x, y, z, of points with non-zero vision_class 

=== "Python"

    ``` python
    clusters = [p for p in points if p.cluster_id > 0]
    if not clusters:
        rr.log("fusion/radar", rr.Points3D([], colors=[]))  
        return
    max_id = max(p.cluster_id for p in clusters)
    pos = [[p.x, p.y, p.z] for p in clusters]
    colors = [colormap(turbo_colormap, p.cluster_id / max_id)
            for p in clusters]
    rr.log("fusion/radar", rr.Points3D(pos, colors=colors))
    ```

=== "Rust"

    ``` rust
    let points: Vec<_> = points.iter().filter(|p| p.fields["vision_class"] != 0).collect();

    let min_x = points.iter().map(|p| p.x).fold(f64::INFINITY, f64::min);
    let max_x = points.iter().map(|p| p.x).fold(f64::NEG_INFINITY, f64::max);

    let min_y = points.iter().map(|p| p.y).fold(f64::INFINITY, f64::min);
    let max_y = points.iter().map(|p| p.y).fold(f64::NEG_INFINITY, f64::max);

    let min_z = points.iter().map(|p| p.z).fold(f64::INFINITY, f64::min);
    let max_z = points.iter().map(|p| p.z).fold(f64::NEG_INFINITY, f64::max);
    ```

### Results
=== "Python"

    ``` python
    print(f"Recieved {len(points)} radar points with non-background vision_class. Values: x: [{min_x:.2f}, {max_x:.2f}]\ty: [{min_y:.2f}, {max_y:.2f}]\tz: [{min_z:.2f}, {max_z:.2f}]")
    ```

=== "Rust"

    ``` rust
    println!(
        "Recieved {} radar points with non-background vision_class. Values: x: [{:.2f}, {:.2f}]\ty: [{:.2f}, {:.2f}]\tz: [{:.2f}, {:.2f}]",
        points.len(),
        min_x,
        max_x,
        min_y,
        max_y,
        min_z,
        max_z,
    );
    ```

The command line output will appear as the following
```
Recieved 12 radar points with non-background vision_class. Values: x: [1.15, 1.53]      y: [0.24, 0.75] z: [-0.31, 0.26]
Recieved 11 radar points with non-background vision_class. Values: x: [1.15, 1.49]      y: [0.29, 0.75] z: [-0.31, 0.19]
Recieved 10 radar points with non-background vision_class. Values: x: [1.15, 1.46]      y: [0.52, 0.75] z: [-0.31, 0.19]
```

When displaying the results through Rerun you will see the pointcloud radar data.
![alt text](assets/fusion_radar.png)

## /fusion/lidar

This demo requires lidar output to be enabled on `fusion` to work.
By default the rt/fusion/lidar output is not enabled for `fusion`.
To enable it, configure the env LIDAR_OUTPUT_TOPIC="rt/fusion/lidar"
or set command line argument --lidar-output-topic=rt/fusion/lidar

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/lidar` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/lidar"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/fusion/lidar', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/lidar"
    let subscriber = session
        .declare_subscriber("rt/fusion/lidar")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    async def lidar_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=lidar_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    edgefirst_schemas::sensor_msgs::PointCloud2;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let pcd: PointCloud2 = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Decode PCD Data

The next step is to decode the PCD data. Please see [examples/pcd](./pcd.md) for a guide on how to decode the PointCloud2 data.


=== "Python"

    ``` python
    def lidar_worker(msg):
        pcd = PointCloud2.deserialize(msg.payload.to_bytes())
        points = decode_pcd(pcd)
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::decode_pcd;
    let points = decode_pcd(pcd);
    ```

### Process the Data

We can now process the data. In this example we will find the maximum and minimum values for x, y, z, of points with non-zero vision_class 

=== "Python"

    ``` python
    clusters = [p for p in points if p.cluster_id > 0]
    if not clusters:
        rr.log("fusion/lidar", rr.Points3D([], colors=[]))  
        return
    max_id = max(p.cluster_id for p in clusters)
    pos = [[p.x, p.y, p.z] for p in clusters]
    colors = [colormap(turbo_colormap, p.cluster_id / max_id)
            for p in clusters]
    rr.log("fusion/lidar", rr.Points3D(pos, colors=colors))
    ```

=== "Rust"

    ``` rust
    let points: Vec<_> = points.iter().filter(|p| p.fields["vision_class"] != 0).collect();

    let min_x = points.iter().map(|p| p.x).fold(f64::INFINITY, f64::min);
    let max_x = points.iter().map(|p| p.x).fold(f64::NEG_INFINITY, f64::max);

    let min_y = points.iter().map(|p| p.y).fold(f64::INFINITY, f64::min);
    let max_y = points.iter().map(|p| p.y).fold(f64::NEG_INFINITY, f64::max);

    let min_z = points.iter().map(|p| p.z).fold(f64::INFINITY, f64::min);
    let max_z = points.iter().map(|p| p.z).fold(f64::NEG_INFINITY, f64::max);
    ```

### Results
=== "Python"

    ``` python
    print(f"Recieved {len(points)} lidar points with non-background vision_class. Values: x: [{min_x:.2f}, {max_x:.2f}]\ty: [{min_y:.2f}, {max_y:.2f}]\tz: [{min_z:.2f}, {max_z:.2f}]")
    ```

=== "Rust"

    ``` rust
    println!(
        "Recieved {} lidar points with non-background vision_class. Values: x: [{:.2f}, {:.2f}]\ty: [{:.2f}, {:.2f}]\tz: [{:.2f}, {:.2f}]",
        points.len(),
        min_x,
        max_x,
        min_y,
        max_y,
        min_z,
        max_z,
    );
    ```

The command line output will appear as the following
```
Recieved 503 lidar points with non-background vision_class. Values: x: [3.40, 3.81]     y: [0.48, 1.06] z: [-0.93, 0.65]
Recieved 507 lidar points with non-background vision_class. Values: x: [3.41, 3.81]     y: [0.49, 1.07] z: [-0.93, 0.64]
Recieved 523 lidar points with non-background vision_class. Values: x: [3.39, 3.77]     y: [0.47, 1.07] z: [-0.96, 0.69]
```

When displaying the results through Rerun you will see the pointcloud lidar data.
![alt text](assets/fusion_lidar.png)

## /fusion/boxes3d

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/boxes3d` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/boxes3d"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/fusion/boxes3d', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/boxes3d"
    let subscriber = session
        .declare_subscriber("rt/fusion/boxes3d")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    async def boxes3d_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=boxes3d_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::Detect;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let boxes: Detect = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The message contains a 2D bounding box with distances. Following the optical frame standard, the `center_x` and `width` fields measure the left-right position and size of the box. The `center_y` and `height` measure the up-down position and size of the box. The distance measures how far forward the box is.

=== "Python"

    ``` python
    def boxes3d_worker(msg):
        detection = Detect.deserialize(msg.payload.to_bytes())
        # The 3D boxes are in an _optical frame of reference, where x is right, y is down, and z (distance) is forward
        # We will convert them to a normal frame of reference, where x is forward, y is left, and z is up
        centers = [(x.distance, -x.center_x, -x.center_y)
                    for x in detection.boxes]
        sizes = [(x.width, x.width, x.height)
                    for x in detection.boxes]

        rr.log("/pointcloud/fusion/boxes", rr.Boxes3D(centers=centers, sizes=sizes))
    ```

=== "Rust"

    ``` rust
    // Access box parameters
    for b in boxes.boxes {
        let x = b.center_x;
        let y = b.center_y;
        let width = b.width;
        let height = b.height;
        let label = b.label;
        let distance = b.distance;
    }
    ```