# Camera Schema Examples

These examples demonstrate how to connect to various camera topics published on your EdgeFirst Platform and how to display the information through the command line.

## Camera Info 
Topic: [/camera/info](../../topics/camera.md#camerainfo)  
Message: [Image](../../api/sensor_msgs.md#camerainfo)

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
    msg = subscriber.recv()
    info = CameraInfo.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::CameraInfo;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let info: CameraInfo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process and Log the Data

The CameraInfo message contains camera calibration and configuration information. You can access various fields like:

=== "Python"

    ``` python
    # Access camera parameters
    width = info.width
    height = info.height
    rr.log("CameraInfo", rr.TextLog("Camera Width: %d Camera Height: %d" % (width, height)))
    ```

### Results
When displaying the results through Rerun you will see a log of the camera width and height.
![alt text](assets/camera_info.png)

=== "Rust"

    ``` rust
    // Access camera parameters
    let width = info.width;
    let height = info.height;
    let text = "Camera Width: ".to_owned() + &width.to_string() + " Camera Height: " + &height.to_string();
    let _ = rr.log("CameraInfo", &rerun::TextLog::new(text));
    ```

## H264 Camera Feed
Topic: [/camera/h264](../../topics/camera.md#camerah264)  
Message: [CompressedVideo](../../api/foxglove_msgs.md#compressedvideo)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/h264` topic and initialize a container for the H264 feed

=== "Python"

    ``` python
    # Create a subscriber for "rt/camera/h264"
    subscriber = session.declare_subscriber('rt/camera/h264')
    raw_data = io.BytesIO()
    container = av.open(raw_data, format='h264', mode='r')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/camera/h264"
    use openh264::decoder::Decoder;
    let subscriber = session
        .declare_subscriber("rt/camera/h264")
        .await
        .unwrap();
    let mut decoder = Decoder::new()?;
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.foxglove_msgs import CompressedVideo
    # Receive a message
    msg = subscriber.recv()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::foxglove_msgs::FoxgloveCompressedVideo;
    // Receive a message
    let msg = subscriber.recv().unwrap();
    let video: FoxgloveCompressedVideo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process and Log the Data

The CompressedVideo message contains H.264 encoded video data. You can convert 

=== "Python"

    ``` python
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
                rr.log('image', rr.Image(frame_array))
    ```

=== "Rust"

    ``` rust
    use openh264::nal_units;
    use openh264::formats::YUVSource;

    for packet in nal_units(&video.data) {
        let Ok(Some(yuv)) = decoder.decode(packet) else { continue };
        let rgb_len = yuv.rgb8_len();
        let mut rgb_raw = vec![0; rgb_len];
        yuv.write_rgb8(&mut rgb_raw);
        let width = yuv.dimensions().0;
        let height = yuv.dimensions().1;
        
        let image = Image::from_rgb24(rgb_raw, [width as u32, height as u32]);
        rr.log("image", &image)?;            
    }
    ```

### Results
When displaying the results through Rerun you will see the live camera feed from your EdgeFirst Platform.
![alt text](assets/h264.png)

## JPEG Camera Feed
Topic: [/camera/jpeg](../../topics/camera.md#camerajpeg)  
Message: [CompressedImage](../../api/sensor_msgs.md#compressedimage)

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
    ```

### Process and Log the Data

The CompressedImage message contains JPEG encoded image data. You can process the data with the following

=== "Python"

    ``` python
    np_arr = np.frombuffer(bytearray(image.data), np.uint8)
    im = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    rr.log('image', rr.Image(im))
    ```

=== "Rust"

    ``` rust
    let im: CompressedImage = cdr::deserialize(&msg.payload().to_bytes())?;
    let image = EncodedImage::from_file_contents(im.data);
    rr.log("image", &image)?;  
    ``` 

### Results
When displaying the results through Rerun you will see the JPEG image feed.
![alt text](assets/h264.png)