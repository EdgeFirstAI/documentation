# GPS Schema Example

This example will go through how to connect to the IMU topic published on your EdgeFirst Platform and how to display the information through the Rerun visualizer.

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `rt/imu` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/imu"
    subscriber = session.declare_subscriber('rt/imu', imu_listener)
    ```

### Decode IMU Data

We can now recieve message on the subcriber. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import Imu
    msg = subscriber.recv()
    imu = Imu.deserialize(msg.payload.to_bytes())
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