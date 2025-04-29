# LIDAR Schema Example

This example will go through how to connect to the radar topic published on your EdgeFirst Platform and how to display the information on the command line as well as through the Rerun visualizer.


## /radar/targets

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

    // Create a subscriber for "rt/lidar/cluster"
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


## /radar/clusters

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `radar/clusters` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/radar/cluster"
    subscriber = session.declare_subscriber('rt/radar/cluster')
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

    // Create a subscriber for "rt/lidar/cluster"
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

## /radar/info

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

## /radar/cube

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
