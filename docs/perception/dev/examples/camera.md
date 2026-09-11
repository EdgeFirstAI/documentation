# Camera Schema Examples

These examples demonstrate how to connect to various camera topics published on your EdgeFirst Platform and how to display the information through the command line.

!!! tip "Topic Names"

    The topics below are subscribed with their bare names, which requires the Zenoh session to be opened with the namespace set to the device hostname as shown in the [Developer Guide](../index.md#subscriber).  Subscribe with a `**/` prefix, for example `**/camera/h264`, to match the topics from a session without a namespace or from a remote device.

!!! warning

    If the Rerun live feed appears to lag, your computer may lack the processing necessary for that stream size, either reduce the [stream size](../../../platforms/configuration/camera.md#stream-size) or use the --save argument to save it as a .rrd file which you can replay afterwards

## Camera Info

Topic: [/camera/info](../../topics/camera.md#camerainfo)  
Message: [Image](../../api/sensor_msgs.md#camerainfo)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/camera/camera_info.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/camera/camera_info.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/info` topic

=== "Python"

    ``` python
    # Create a subscriber for "camera/info"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('camera/info', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "camera/info"
    let subscriber = session
        .declare_subscriber("camera/info")
        .await
        .unwrap();
    ```

### Receive a message

We can now await a message from that subscriber. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages.

=== "Python"

    ``` python
    async def info_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=info_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
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
    def info_worker(msg):
        info = CameraInfo.deserialize(msg.payload.to_bytes())
        width = info.width
        height = info.height
        rr.log("CameraInfo", rr.TextLog("Camera Width: %d Camera Height: %d" % (width, height)))
    ```

### Results

When displaying the results through Rerun you will see a log of the camera width and height.

{{ figure("assets/camera_info.png", "Camera Information") }}

=== "Rust"

    ``` rust
    // Access camera parameters
    let width = info.width;
    let height = info.height;
    let text = "Camera Width: ".to_owned() + &width.to_string() + " Camera Height: " + &height.to_string();
    let _ = rr.log("CameraInfo", &rerun::TextLog::new(text));
    ```

## Camera Frame

Topic: [/camera/frame](../../topics/camera.md#cameraframe)  
Message: [CameraFrame](../../api/edgefirst_msgs.md#cameraframe)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/camera/dma.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/camera/dma.rs)  
!!! warning  
    The Camera Frame example is only functional when run directly on the EdgeFirst Platform as it references DMA buffers that are only accessible on the EdgeFirst Platform.  The example must run with the same permissions as the camera service, use `sudo`.

!!! note "Migrating from DmaBuffer"

    The `camera/frame` topic and its `CameraFrame` message replace the `camera/dma` topic and `DmaBuffer` message of earlier releases.  The published sample code predates this change, the snippets below show the equivalent processing with the `CameraFrame` message from EdgeFirst Schemas 4.0.

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/frame` topic

=== "Python"

    ``` python
    # Create a subscriber for "camera/frame"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('camera/frame', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "camera/frame"
    let subscriber = session
        .declare_subscriber("camera/frame")
        .await
        .unwrap();
    ```

### Receive a message

We can now await a message from that subscriber. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages.

=== "Python"

    ``` python
    async def frame_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=frame_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::CameraFrame;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let frame = CameraFrame::from_cdr(&msg.payload().to_bytes()).unwrap();
    ```

### Process the Data

The `CameraFrame` message carries a stamped `Tensor`.  The tensor contains the process ID of the camera service, the image `format` as a FOURCC such as `NV12`, the `shape` as `[height, width]`, and one `TensorPlane` per plane with the file descriptor `handle`, `offset`, `stride`, and `size` of the DMA buffer.  The process ID and the plane handle are necessary to access the image, the file descriptor is duplicated into our process with `pidfd_getfd` and mapped with `mmap`.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import CameraFrame

    def frame_worker(msg):
        frame = CameraFrame.from_cdr(msg.payload.to_bytes())
        tensor = frame.tensor
        plane = tensor.planes[0]
        height, width = tensor.shape[0], tensor.shape[1]

        pidfd = pidfd_open(tensor.pid)
        if pidfd < 0:
            return

        fd = pidfd_getfd(pidfd, plane.handle, GETFD_FLAGS)
        if fd < 0:
            return

        # Now fd can be used as a file descriptor, the ISP produces NV12 frames
        mm = mmap.mmap(fd, plane.size, offset=plane.offset)
        rr.log("/camera", rr.Image(bytes=mm[:plane.used],
                                    width=width,
                                    height=height,
                                    pixel_format=rr.PixelFormat.NV12))
        mm.close()
        os.close(fd)
        os.close(pidfd)
    ```

=== "Rust"

    ``` rust
    let tensor = frame.tensor();
    let plane = tensor.planes().next().unwrap();
    let (height, width) = (tensor.shape()[0] as u32, tensor.shape()[1] as u32);

    let pidfd: PidFd = match PidFd::from_pid(tensor.pid() as i32)
    let fd = match get_file_from_pidfd(pidfd.as_raw_fd(), plane.handle() as i32, GetFdFlags::empty())

    let image_size = plane.size() as usize;
    let mmap = unsafe {
        from_raw_parts_mut(
            mmap(
                null_mut(),
                image_size,
                PROT_READ,
                MAP_SHARED,
                fd.as_raw_fd(),
                plane.offset() as i64,
            ) as *mut u8,
            image_size,
        )
    };
    let rr_image = rerun::Image::from_pixel_format(
        [width, height],
        rerun::PixelFormat::NV12,
        mmap[..plane.used() as usize].to_vec(),
    );
    let _ = rec.log("camera/frame", &rr_image);

    unsafe {
        munmap(mmap.as_mut_ptr() as *mut c_void, image_size);
    }
    ```

### Results

When displaying the results through Rerun you will see the live camera feed from your EdgeFirst Platform.

{{ figure("assets/dma.png", "Live Camera Feed DMA") }}

## H264 Camera Feed

Topic: [/camera/h264](../../topics/camera.md#camerah264)  
Message: [CompressedVideo](../../api/foxglove_msgs.md#compressedvideo)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/camera/h264.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/camera/h264.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/h264` topic.

=== "Python"

    ``` python
    # Create a subscriber for "camera/h264"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('camera/h264', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "camera/h264"
    use openh264::decoder::Decoder;
    let subscriber = session
        .declare_subscriber("camera/h264")
        .await
        .unwrap();
    let mut decoder = Decoder::new()?;
    ```

### Receive a message

We can now await a message from that subscriber. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages.

=== "Python"

    ``` python
    async def h264_handler(drain):
        raw_data = io.BytesIO()
        container = av.open(raw_data, format='h264', mode='r')
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=h264_worker, args=[msg, raw_data, container])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::foxglove_msgs::FoxgloveCompressedVideo;
    // Receive a message
    let msg = subscriber.recv().unwrap();
    let video: FoxgloveCompressedVideo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process and Log the Data

The CompressedVideo message contains H.264 encoded video data. This data can be logged by the following

=== "Python"

    ``` python
    def h264_worker(msg, raw_data, container):
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
                    rr.log('/camera', rr.Image(frame_array))
            except Exception:
                continue
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

{{ figure("assets/h264.png", "Live Camera Feed") }}

## JPEG Camera Feed

Topic: [/camera/jpeg](../../topics/camera.md#camerajpeg)  
Message: [CompressedImage](../../api/sensor_msgs.md#compressedimage)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/camera/jpeg.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/camera/)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `camera/jpeg` topic

=== "Python"

    ``` python
    # Create a subscriber for "camera/jpeg"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('camera/jpeg', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "camera/jpeg"
    let subscriber = session
        .declare_subscriber("camera/jpeg")
        .await
        .unwrap();
    ```

### Receive a message

We can now await a message from that subscriber. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages.

=== "Python"

    ``` python
    async def jpeg_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=jpeg_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::CompressedImage;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    ```

### Process the Data

The CompressedImage message contains JPEG encoded image data. You can process the data with the following

=== "Python"

    ``` python
    def jpeg_worker(msg):
        image = CompressedImage.deserialize(msg.payload.to_bytes())
        np_arr = np.frombuffer(bytearray(image.data), np.uint8)
        im = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        rr.log('/camera', rr.Image(im))
    ```

=== "Rust"

    ``` rust
    let im: CompressedImage = cdr::deserialize(&msg.payload().to_bytes())?;
    let image = EncodedImage::from_file_contents(im.data);
    rr.log("image", &image)?;  
    ``` 

### Results

When displaying the results through Rerun you will see the JPEG image feed.

{{ figure("assets/jpeg.png", "JPEG Image Feed") }}
