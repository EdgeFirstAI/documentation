# Fusion Schema Examples

These examples demonstrate how to connect to various fusion topics published on your EdgeFirst Platform and how to display the information through the command line.

## /fusion/occupancy

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/occupancy` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/occupancy"
    subscriber = session.declare_subscriber('rt/fusion/occupancy')
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

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.fusion_msgs import Occupancy

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    occupancy = Occupancy.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::fusion_msgs::Occupancy;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let occupancy: Occupancy = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Occupancy message contains occupancy grid data. You can access various fields like:

=== "Python"

    ``` python
    # Access occupancy parameters
    width = occupancy.width
    height = occupancy.height
    resolution = occupancy.resolution
    data = occupancy.data  # Occupancy grid data
    ```

=== "Rust"

    ``` rust
    // Access occupancy parameters
    let width = occupancy.width;
    let height = occupancy.height;
    let resolution = occupancy.resolution;
    let data = occupancy.data;  // Occupancy grid data
    ```

## /fusion/model_output

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/model_output` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/model_output"
    subscriber = session.declare_subscriber('rt/fusion/model_output')
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

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.fusion_msgs import ModelOutput

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    output = ModelOutput.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::fusion_msgs::ModelOutput;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let output: ModelOutput = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The ModelOutput message contains fused model output data. You can access various fields like:

=== "Python"

    ``` python
    # Access model output parameters
    timestamp = output.timestamp
    boxes = output.boxes  # 2D bounding boxes
    masks = output.masks  # Segmentation masks
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
    subscriber = session.declare_subscriber('rt/fusion/mask_output/tracked')
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

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.fusion_msgs import MaskOutputTracked

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    tracked = MaskOutputTracked.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::fusion_msgs::MaskOutputTracked;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let tracked: MaskOutputTracked = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The MaskOutputTracked message contains tracked segmentation mask data. You can access various fields like:

=== "Python"

    ``` python
    # Access tracked mask parameters
    timestamp = tracked.timestamp
    track_id = tracked.track_id
    mask = tracked.mask  # Segmentation mask
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
    subscriber = session.declare_subscriber('rt/fusion/radar')
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

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import PointCloud2

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    pcd = PointCloud2.deserialize(msg.payload.to_bytes())
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
    from edgefirst.schemas import decode_pcd
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
    points = [p for p in points if p.fields["vision_class"] != 0]

    min_x = min([p.x for p in points], default=float("inf"))
    max_x = max([p.x for p in points], default=float("-inf"))

    min_y = min([p.y for p in points], default=float("inf"))
    max_y = max([p.y for p in points], default=float("-inf"))

    min_z = min([p.z for p in points], default=float("inf"))
    max_z = max([p.z for p in points], default=float("-inf"))
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
    subscriber = session.declare_subscriber('rt/fusion/lidar')
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
    from edgefirst.schemas.sensor_msgs import PointCloud2

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    pcd = PointCloud2.deserialize(msg.payload.to_bytes())
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
    from edgefirst.schemas import decode_pcd
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
    points = [p for p in points if p.fields["vision_class"] != 0]

    min_x = min([p.x for p in points], default=float("inf"))
    max_x = max([p.x for p in points], default=float("-inf"))

    min_y = min([p.y for p in points], default=float("inf"))
    max_y = max([p.y for p in points], default=float("-inf"))

    min_z = min([p.z for p in points], default=float("inf"))
    max_z = max([p.z for p in points], default=float("-inf"))
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
    subscriber = session.declare_subscriber('rt/fusion/boxes3d')
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
    from edgefirst.schemas.edgefirst_msgs import Detect

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    boxes = Detect.deserialize(msg.payload.to_bytes())
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
    # Access box parameters
    for b in boxes.boxes:
        right = b.center_x
        down = b.center_y
        width = b.width
        height = b.height
        label = b.label
        distance = b.distance
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