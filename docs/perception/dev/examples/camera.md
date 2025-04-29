# Camera Schema Examples

These examples demonstrate how to connect to various camera topics published on your EdgeFirst Platform and how to display the information through the command line.

## /camera/info

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/info` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/camera/info"
    subscriber = session.declare_subscriber('rt/camera/info')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/camera/info"
    let subscriber = session
        .declare_subscriber("rt/camera/info")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import CameraInfo

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    info = CameraInfo.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::CameraInfo;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let info: CameraInfo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The CameraInfo message contains camera calibration and configuration information. You can access various fields like:

=== "Python"

    ``` python
    # Access camera parameters
    width = info.width
    height = info.height
    distortion_model = info.distortion_model
    D = info.D  # Distortion parameters
    K = info.K  # Intrinsic camera matrix
    R = info.R  # Rectification matrix
    P = info.P  # Projection matrix
    ```

=== "Rust"

    ``` rust
    // Access camera parameters
    let width = info.width;
    let height = info.height;
    let distortion_model = info.distortion_model;
    let D = info.D;  // Distortion parameters
    let K = info.K;  // Intrinsic camera matrix
    let R = info.R;  // Rectification matrix
    let P = info.P;  // Projection matrix
    ```

## /camera/h264

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/h264` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/camera/h264"
    subscriber = session.declare_subscriber('rt/camera/h264')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/camera/h264"
    let subscriber = session
        .declare_subscriber("rt/camera/h264")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.foxglove_msgs import CompressedVideo

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    video = CompressedVideo.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::foxglove_msgs::CompressedVideo;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let video: CompressedVideo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The CompressedVideo message contains H.264 encoded video data. You can access various fields like:

=== "Python"

    ``` python
    # Access video parameters
    width = video.width
    height = video.height
    data = video.data  # H.264 encoded video data
    ```

=== "Rust"

    ``` rust
    // Access video parameters
    let width = video.width;
    let height = video.height;
    let data = video.data;  // H.264 encoded video data
    ```

## /camera/jpeg

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/jpeg` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/camera/jpeg"
    subscriber = session.declare_subscriber('rt/camera/jpeg')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/camera/jpeg"
    let subscriber = session
        .declare_subscriber("rt/camera/jpeg")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import CompressedImage

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    image = CompressedImage.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::CompressedImage;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let image: CompressedImage = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The CompressedImage message contains JPEG encoded image data. You can access various fields like:

=== "Python"

    ``` python
    # Access image parameters
    width = image.width
    height = image.height
    format = image.format  # Should be "jpeg"
    data = image.data  # JPEG encoded image data
    ```

=== "Rust"

    ``` rust
    // Access image parameters
    let width = image.width;
    let height = image.height;
    let format = image.format;  // Should be "jpeg"
    let data = image.data;  // JPEG encoded image data
    ``` 