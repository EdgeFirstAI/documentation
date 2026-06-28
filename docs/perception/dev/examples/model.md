# Model Schema Examples

These examples demonstrate how to connect to various model topics published on your EdgeFirst Platform and how to display the information through the command line.

## Model Info

Topic: [/model/info](../../topics/model.md#modelinfo)  
Message: [ModelInfo](../../api/edgefirst_msgs.md#modelinfo)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/model/model_info.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/model/model_info.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/info` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/info"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/model/info', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/model/info"
    let subscriber = session
        .declare_subscriber("rt/model/info")
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
    use edgefirst_schemas::edgefirst_msgs::ModelInfo;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let info: ModelInfo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The ModelInfo message contains information about the model configuration. You can access various fields like:

=== "Python"

    ``` python
    def info_worker(msg):
        info = ModelInfo.deserialize(msg.payload.to_bytes())
        m_type = info.model_type
        m_name = info.model_name
        rr.log("ModelInfo", rr.TextLog("Model Name: %s Model Type: %s" % (m_name, m_type)))
    ```

=== "Rust"

    ``` rust
    let m_type = info.model_type;
    let m_name = info.model_name;
    let text = "Model Name: ".to_owned() + &m_name + " Model Type: " + &m_type;
    let _ = rr.log("ModelInfo", &rerun::TextLog::new(text));
    ```

### Results

When displaying the results through Rerun you will see the model info.

{{ figure("assets/model_info.png", "Model Info") }}

## Boxes2D

Topic: [/model/boxes2d](../../topics/model.md#modelboxes2d)  
Message: [ModelInfo](../../api/edgefirst_msgs.md#detect)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/model/boxes2d.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/model/boxes2d.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/boxes2d` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/boxes2d"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/model/boxes2d', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/model/boxes2d"
    let subscriber = session
        .declare_subscriber("rt/model/boxes2d")
        .await
        .unwrap();
    ```

### Receive a message

We can now await a message from that subscriber. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages.

=== "Python"

    ``` python
    async def boxes2d_handler(drain):
    while True:
        msg = await drain.get_latest()

        thread = threading.Thread(target=boxes2d_worker, args=[msg])
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
    let detection: Detect = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Boxes2D message contains 2D bounding box detections. The message will be sent to be processed, deserializing the message, accessing the required information and logging the boxes to Rerun.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import Detect

    def boxes2d_worker(msg):
        detection = Detect.deserialize(msg.payload.to_bytes())
        centers = []
        sizes = []
        labels = []
        for box in detection.boxes:
            centers.append((box.center_x, box.center_y))
            sizes.append((box.width, box.height))
            labels.append(box.label)
        rr.log("boxes", rr.Boxes2D(centers=centers, sizes=sizes, labels=labels))
    ```

=== "Rust"

    ``` rust
    let mut centers = Vec::new();
    let mut sizes = Vec::new();
    let mut labels = Vec::new();

    for b in detection.boxes {
        centers.push([b.center_x, b.center_y]);
        sizes.push([b.width, b.height]);
        labels.push(b.label);
    }

    let _ = rr.log("boxes", &rerun::Boxes2D::from_centers_and_sizes(centers, sizes).with_labels(labels))?;
    ``` 

### Results

When displaying the results through Rerun you will see the boxes without any camera, to see the combined example please see the[Combined Example](#combined-example).

{{ figure("assets/model_boxes2d.png", "Model 2D Boxes") }}

### Box Tracking

On your EdgeFirst Platform you can also allow tracking of the boxes and this can then be logged during the publishing of the boxes. The documentation for the settings to turn on tracking can be found [here](../../../platforms/configuration/model.md#track-settings). You can update your code to match the [Python example](https://github.com/EdgeFirstAI/samples/blob/main/python/model/boxes2d_tracked.py) or [Rust example](https://github.com/EdgeFirstAI/samples/blob/main/rust/model/boxes2d_tracked.rs) from the regular boxes2d example by changing the boxes2d_worker to the following.

=== "Python"

    ``` python
    def boxes2d_worker(msg, boxes_tracked):
        detection = Detect.deserialize(msg.payload.to_bytes())
        centers = []
        sizes = []
        labels = []
        colors = []
        for box in detection.boxes:
            if box.track.id and box.track.id not in boxes_tracked:
                boxes_tracked[box.track.id] = [box.label + ": " + box.track.id[:6], list(np.random.choice(range(256), size=3))]
            if box.track.id:
                colors.append(boxes_tracked[box.track.id][1])
                labels.append(boxes_tracked[box.track.id][0])
            else:
                colors.append([0,255,0])
                labels.append(box.label)
            centers.append((box.center_x, box.center_y))
            sizes.append((box.width, box.height))
        rr.log("boxes", rr.Boxes2D(centers=centers, sizes=sizes, labels=labels, colors=colors))
    ```

=== "Rust"

    ``` rust
    let detection: Detect = cdr::deserialize(&msg.payload().to_bytes())?;
    let mut centers = Vec::new();
    let mut sizes = Vec::new();
    let mut labels = Vec::new();
    let mut colors = Vec::new();

    for b in detection.boxes {
        if !b.track.id.is_empty() {
            // Insert into map if not already present
            let entry = boxes_tracked.entry(b.track.id.clone()).or_insert_with(|| {
                let mut rng_maker = rng();
                let random_color = [
                    rng_maker.random_range(0..=255),
                    rng_maker.random_range(0..=255),
                    rng_maker.random_range(0..=255),
                ];
                let short_id = &b.track.id[..6.min(b.track.id.len())];
                let label = format!("{}: {}", b.label, short_id);
                (label, random_color)
            });

            labels.push(entry.0.clone());
            colors.push(entry.1);
        } else {
            labels.push(b.label.clone());
            colors.push([0, 255, 0]);
        }

        centers.push([b.center_x, b.center_y]);
        sizes.push([b.width, b.height]);
    }

    let boxes = Boxes2D::from_centers_and_sizes(centers, sizes)
        .with_labels(labels)
        .with_colors(colors);

    rr.log("boxes", &boxes)?;
    ```

The main adjustments are that a color will be specified and each tracked box will have its own color as well as that we will add in the unique ID for the box into the label. All of this is contingent on tracking being enabled. The following image is taken when applied to a combined example.

{{ video("assets/boxes2d_tracking.mp4", "Boxes2D Tracking") }}

## Model Mask

Topic: [/model/mask](../../topics/model.md#modelmask)  
Message: [Mask](../../api/edgefirst_msgs.md#mask)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/model/mask.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/model/mask.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/mask` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/mask"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/model/mask', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/model/mask"
    let subscriber = session
        .declare_subscriber("rt/model/mask")
        .await
        .unwrap();
    ```

### Receive a message

We can now await a message from that subscriber. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages. In addition we will log the annotations so Rerun knows what colors to use for each class.

=== "Python"

    ``` python
    async def mask_handler(drain):
        rr.log("/", rr.AnnotationContext([(0, "background", (0,0,0)), (1, "person", (0,255,0))]))
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=mask_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::Mask;

    // Log annotation context
    rr.log(
        "/",
        &AnnotationContext::new([
            (0, "background", rerun::Rgba32::from_rgb(0, 0, 0)),
            (1, "person", rerun::Rgba32::from_rgb(0, 255, 0))])
    )?;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let mask: Mask = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Mask message contains segmentation mask data. The worker will perform argmax on the result to get the resultant class for each pixel to be logged.

=== "Python"

    ``` python
    def mask_worker(msg):
        mask = Mask.deserialize(msg.payload.to_bytes())
        np_arr = np.asarray(mask.mask, dtype=np.uint8)
        np_arr = np.reshape(np_arr, [mask.height, mask.width, -1])
        np_arr = np.argmax(np_arr, axis=2)
        rr.log("mask", rr.SegmentationImage(np_arr))
    ```

=== "Rust"

    ``` rust
    let h = mask.height as usize;
    let w = mask.width as usize;
    let total_len = mask.mask.len() as u32;
    let c = (total_len / (h as u32 * w as u32)) as usize;

    let arr3 = Array::from_shape_vec((h, w, c), mask.mask.clone())?;
    
    // Compute argmax along the last axis (class channel)
    let array2: Array2<u8> = arr3
        .map_axis(ndarray::Axis(2), |class_scores| {
            class_scores
                .iter()
                .enumerate()
                .max_by_key(|(_, val)| *val)
                .map(|(idx, _)| idx as u8)
                .unwrap_or(0)
        });

    // Log segmentation mask
    let _ = rr.log("mask", &SegmentationImage::try_from(array2)?)?;
    ```

### Results

When displaying the results through Rerun you will see the segmentation without any camera, to see the combined example please see the[Combined Example](#combined-example).

{{ figure("assets/model_mask.png", "Model Mask") }}

## Model Mask Compressed

Topic: [/model/mask](../../topics/model.md#modelmask_compressed)  
Message: [Mask](../../api/edgefirst_msgs.md#mask)  
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/model/compressed_mask.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/model/compressed_mask.rs)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/mask_compressed` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/mask_compressed"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('rt/model/mask_compressed', drain.callback)
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/model/compressed_mask"
    let subscriber = session.declare_subscriber("rt/model/mask_compressed")
    .await
    .unwrap();
    ```

### Receive a message

We can now await a message from that subscriber from an asynchronous function. After receiving the message, we will pass that message along to our processing function in a new thread to avoid missing messages. In addition we will log the annotations so Rerun knows what colors to use for each class.

=== "Python"

    ``` python
    async def mask_handler(drain):
        rr.log("/", rr.AnnotationContext([(0, "background", (0,0,0)), (1, "person", (0,255,0))]))
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=mask_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::Mask;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let mask: Mask = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Mask message contains segmentation mask data. The worker will decompress the data and then perform argmax on the result to get the resultant class for each pixel to be logged.

=== "Python"

    ``` python
    def mask_worker(msg):
        mask = Mask.deserialize(msg.payload.to_bytes())
        decoded_array = zstd.decompress(bytes(mask.mask))
        np_arr = np.frombuffer(decoded_array, np.uint8)
        np_arr = np.reshape(np_arr, [mask.height, mask.width, -1])
        np_arr = np.argmax(np_arr, axis=2)
        
        rr.log("mask", rr.SegmentationImage(np_arr))
    ```

=== "Rust"

    ``` rust
    let decompressed_bytes = decode_all(Cursor::new(&mask.mask))?;
        
    let h = mask.height as usize;
    let w = mask.width as usize;
    let total_len = mask.mask.len() as u32;
    let c = (total_len / (h as u32 * w as u32)) as usize;

    let arr3 = Array::from_shape_vec([h, w, c], decompressed_bytes.clone())?;
    
    // Compute argmax along the last axis (class channel)
    let array2: Array2<u8> = arr3
        .map_axis(ndarray::Axis(2), |class_scores| {
            class_scores
                .iter()
                .enumerate()
                .max_by_key(|(_, val)| *val)
                .map(|(idx, _)| idx as u8)
                .unwrap_or(0)
        });

    // Log annotation context
    rr.log(
        "/",
        &AnnotationContext::new([
            (0, "background", rerun::Rgba32::from_rgb(0, 0, 0)),
            (1, "person", rerun::Rgba32::from_rgb(0, 255, 0))])
    )?;

    // Log segmentation mask
    let _ = rr.log("mask", &SegmentationImage::try_from(array2)?)?;
    ``` 

### Results

When displaying the results through Rerun you will see the segmentation without any camera, to see the combined example please see the[Combined Example](#combined-example).

{{ figure("assets/model_mask.png", "Model Mask") }}

## Combined Example

This example will demonstrate how to combine the camera feed with the model messages to create a composite Rerun view. The main difference when using multiple messages in a script, is that we will change from waiting on the message to be received to having a callback function for when a message is received. Using the initial method, the script would hang while waiting for a message topic to be published, so if the messages are being published at different rates, the slowest message rate will limit the others.

Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/combined/camera_model.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/combined/mega_sample.rs)

### Setting up the subscribers

After setting up the Zenoh session, we will create a subscriber to the three topics, camera, boxes and segmentation. A FrameSize is additionally created to pass the stream size from the camera to the boxes and segmentation mask so they can be resized appropriately.

=== "Python"

    ``` python
    # Create the necessary subscribers
    loop = asyncio.get_running_loop()
    h264_drain = MessageDrain(loop)
    boxes_drain = MessageDrain(loop)
    mask_drain = MessageDrain(loop)
    frame_size_storage = FrameSize()
    session.declare_subscriber('rt/camera/h264', h264_drain.callback)
    session.declare_subscriber('rt/model/boxes2d', boxes_drain.callback)
    if args.remote:
        session.declare_subscriber('rt/model/mask_compressed', mask_drain.callback)
    else:
        session.declare_subscriber('rt/model/mask', mask_drain.callback)
    ```

### Subscriber Callbacks

We will now go through the handler functions that are in use for this example. These handler functions will independently handle each of the messages received through the MessageDrain. Additionally, we will make use of a FrameSize object to communicate the frame size of the camera to the boxes and segmentation mask so they can be resized appropriately.

=== "Python"

    ``` python
    await asyncio.gather(h264_handler(h264_drain, frame_size_storage), 
                         boxes2d_handler(boxes_drain, frame_size_storage),
                         mask_handler(mask_drain, frame_size_storage, args.remote))
    ```

#### H264 Handler

The H264 handler will receive the CompressedVideo message from the MessageDrain and after initializing the required containers will pass that message to the worker, where the message will be processed and logged to Rerun.

=== "Python"

    ``` python
    async def h264_handler(drain, frame_storage):
        raw_data = io.BytesIO()
        container = av.open(raw_data, format='h264', mode='r')

        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=h264_worker, args=[msg, frame_storage, raw_data, container])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    
    def h264_worker(msg, frame_storage, raw_data, container):
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
                    frame_storage.set(frame_array.shape[1], frame_array.shape[0])
                    rr.log('/camera', rr.Image(frame_array))
            except Exception:
                continue
    ```

#### Boxes2D Handler

The Boxes2D callback will wait for a Detect message from the MessageDrain and will pass that message to the worker, where the message will be processed and logged to Rerun. The boxes logged will use tracking when available. Additionally, this handler will wait until the camera has started and logged a frame size so it knows what the height and width will be to resize the boxes.

=== "Python"

    ``` python
    async def boxes2d_handler(drain, frame_storage):
        boxes_tracked = {}
        _ = await frame_storage.get()
        while True:
            msg = await drain.get_latest()
            frame_size = await frame_storage.get()
            thread = threading.Thread(target=boxes2d_worker, args=[msg, boxes_tracked, frame_size])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()

    def boxes2d_worker(msg, boxes_tracked, frame_size):
        detection = Detect.deserialize(msg.payload.to_bytes())
        centers, sizes, labels, colors = [], [], [], []
        for box in detection.boxes:
            if box.track.id and box.track.id not in boxes_tracked:
                boxes_tracked[box.track.id] = [box.label + ": " + box.track.id[:6], list(np.random.choice(range(256), size=3))]
            if box.track.id:
                colors.append(boxes_tracked[box.track.id][1])
                labels.append(boxes_tracked[box.track.id][0])
            else:
                colors.append([0,255,0])
                labels.append(box.label)
            centers.append((int(box.center_x * frame_size[0]), int(box.center_y * frame_size[1])))
            sizes.append((int(box.width * frame_size[0]), int(box.height * frame_size[1])))
        rr.log("/camera/boxes", rr.Boxes2D(centers=centers, sizes=sizes, labels=labels, colors=colors))
    ```

#### Mask Handler

The Mask callback will wait for a Mask message from the MessageDrain and will pass that message to the worker, where the message will be processed and logged to Rerun. The mask_handler requires the remote field to be passed so it knows whether to decompress the mask data or not. Additionally, this handler will wait until the camera has started and logged a frame size so it knows what the height and width will be to resize the mask.

=== "Python"

    ``` python
    async def mask_handler(drain, frame_storage, remote):
        _ = await frame_storage.get()
        rr.log("/", rr.AnnotationContext([(0, "background", (0, 0, 0, 0)), (1, "person", (0, 255, 0))]))
        while True:
            msg = await drain.get_latest()
            frame_size = await frame_storage.get()
            thread = threading.Thread(target=mask_worker, args=[msg, frame_size, remote])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()

    def mask_worker(msg, frame_size, remote):
        mask = Mask.deserialize(msg.payload.to_bytes())
        if remote:
            decoded_array = zstd.decompress(bytes(mask.mask))
            np_arr = np.frombuffer(decoded_array, np.uint8).reshape(mask.height, mask.width, -1)
        else:
            np_arr = np.asarray(mask.mask, dtype=np.uint8)
            np_arr = np.reshape(np_arr, [mask.height, mask.width, -1])
        np_arr = cv2.resize(np_arr, frame_size)
        np_arr = np.argmax(np_arr, axis=2)
        
        rr.log("/camera/mask", rr.SegmentationImage(np_arr))
    ```

### Results

When displaying the results through Rerun you will see the combined image of the camera feed, segmentation image and boxes.

{{ figure("assets/camera_model_combined.png", "Camera + Segmentation + Boxes") }}
