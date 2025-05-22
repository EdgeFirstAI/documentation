# Model Schema Examples

These examples demonstrate how to connect to various model topics published on your EdgeFirst Platform and how to display the information through the command line.

## Model Info
Topic: [/model/info](../../topics/model.md#modelinfo)  
Message: [ModelInfo](../../api/edgefirst_msgs.md#modelinfo)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/info` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/info"
    subscriber = session.declare_subscriber('rt/model/info')
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

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import ModelInfo

    # Receive a message
    msg = subscriber.recv()
    # deserialize message
    info = ModelInfo.deserialize(msg.payload.to_bytes())
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
    # Access model parameters
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

## Boxes2D
Topic: [/model/boxes2d](../../topics/model.md#modelboxes2d)  
Message: [ModelInfo](../../api/edgefirst_msgs.md#detect)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/boxes2d` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/boxes2d"
    subscriber = session.declare_subscriber('rt/model/boxes2d')
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

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import Detect

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    detection = Detect.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::Detect;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let detection: Detect = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Boxes2D message contains 2D bounding box detections. You can access various fields like:

=== "Python"

    ``` python
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

## Model Mask
Topic: [/model/mask](../../topics/model.md#modelmask)  
Message: [Mask](../../api/edgefirst_msgs.md#mask)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/mask` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/mask"
    subscriber = session.declare_subscriber('rt/model/mask')
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

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import Mask

    msg = subscriber.recv()
    mask = Mask.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::Mask;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let mask: Mask = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Mask message contains segmentation mask data. You can access various fields like:

=== "Python"

    ``` python
    np_arr = np.asarray(mask.mask, dtype=np.uint8)
    np_arr = np.reshape(np_arr, [mask.height, mask.width, -1])
    np_arr = np.argmax(np_arr, axis=2)
    rr.log("/", rr.AnnotationContext([(0, "background", (0,0,0)), (1, "person", (0,255,0))]))
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

## Model Mask Compressed
Topic: [/model/mask](../../topics/model.md#modelmask_compressed)  
Message: [Mask](../../api/edgefirst_msgs.md#mask)

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/compressed_mask` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/mask_compressed"
    subscriber = session.declare_subscriber('rt/model/mask_compressed')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/model/compressed_mask"
    let subscriber = session.declare_subscriber("rt/model/mask_compressed")
    .await
    .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.edgefirst_msgs import Mask

    msg = subscriber.recv()
    mask = Mask.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::edgefirst_msgs::Mask;

    // Receive a message
    let msg = subscriber.recv().unwrap();
    let mask: Mask = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The CompressedMask message contains compressed segmentation mask data. You can access various fields like:

=== "Python"

    ``` python
    decoded_array = zstd.decompress(bytes(mask.mask))
    np_arr = np.frombuffer(decoded_array, np.uint8)
    np_arr = np.reshape(np_arr, [mask.height, mask.width, -1])
    np_arr = np.argmax(np_arr, axis=2)
    rr.log("/", rr.AnnotationContext([(0, "background", (0,0,0)), (1, "person", (0,255,0))]))
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