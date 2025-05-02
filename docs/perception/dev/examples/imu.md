# IMU Schema Example

This example will go through how to connect to the IMU topic published on your EdgeFirst Platform and how to display the information through the Rerun visualizer.

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `rt/imu` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/imu"
    subscriber = session.declare_subscriber('rt/imu', imu_listener)
    ```
=== "Rust"

    ``` rust
    let subscriber = session
        .declare_subscriber("rt/imu")
        .await
        .unwrap();
    ```

### Decode IMU Data

We can now recieve message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import Imu
    msg = subscriber.recv()
    imu = Imu.deserialize(msg.payload.to_bytes())
    ```
=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::{IMU};
    while let Ok(msg) = subscriber.recv() {
        let imu: IMU = cdr::deserialize(&msg.payload().to_bytes())?;
    }
    ```

### Get IMU Values and Post to Rerun

We will now pull out the IMU data from the decoded Imu message and send the quaternion to Rerun.

=== "Python"

    ``` python
    x = imu.orientation.x
    y = imu.orientation.y
    z = imu.orientation.z
    w = imu.orientation.w
    # print("X: %.4f Y: %.4f Z: %.4f W: %.4f" % (x, y, z, w))
    rr.log("box", rr.Transform3D(clear=False, quaternion=Quaternion(xyzw=[x,y,z,w])))
    ```
=== "Rust"

    ``` rust
    let x = imu.orientation.x as f32;
    let y = imu.orientation.y as f32;
    let z = imu.orientation.z as f32;
    let w = imu.orientation.w as f32;
    // println!("X: {} Y: {} Z: {} W: {}", x, y, z, w);
    let my_quat = rerun::Quaternion([x,y,z,w]);
    let _ = rec.log("box", &rerun::Transform3D::default().with_quaternion(my_quat));
    ```

### Results
The command line output will appear as the following
```
X: -0.0125 Y: 0.0383 Z: 0.0698 W: 0.9968
X: -0.0125 Y: 0.0383 Z: 0.0698 W: 0.9968
X: -0.0125 Y: 0.0383 Z: 0.0698 W: 0.9968
```

When displaying the results through Rerun you will see a solid cube that is matching the orientation of your EdgeFirst Platform
![alt text](assets/imu.png)