# Model Schema Examples

These examples demonstrate how to connect to various model topics published on your EdgeFirst Platform and how to display the information through the command line.

## /model/info

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
    from edgefirst.schemas.model_msgs import ModelInfo

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    info = ModelInfo.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::model_msgs::ModelInfo;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let info: ModelInfo = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The ModelInfo message contains information about the model configuration. You can access various fields like:

=== "Python"

    ``` python
    # Access model parameters
    model_name = info.model_name
    input_shape = info.input_shape
    output_shape = info.output_shape
    classes = info.classes
    ```

=== "Rust"

    ``` rust
    // Access model parameters
    let model_name = info.model_name;
    let input_shape = info.input_shape;
    let output_shape = info.output_shape;
    let classes = info.classes;
    ```

## /model/boxes2d

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
    from edgefirst.schemas.model_msgs import Boxes2D

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    boxes = Boxes2D.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::model_msgs::Boxes2D;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let boxes: Boxes2D = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Boxes2D message contains 2D bounding box detections. You can access various fields like:

=== "Python"

    ``` python
    # Access box parameters
    for box in boxes.boxes:
        x = box.x
        y = box.y
        width = box.width
        height = box.height
        class_id = box.class_id
        confidence = box.confidence
    ```

=== "Rust"

    ``` rust
    // Access box parameters
    for box in boxes.boxes {
        let x = box.x;
        let y = box.y;
        let width = box.width;
        let height = box.height;
        let class_id = box.class_id;
        let confidence = box.confidence;
    }
    ```

## /model/mask

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
    from edgefirst.schemas.model_msgs import Mask

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    mask = Mask.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::model_msgs::Mask;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let mask: Mask = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Mask message contains segmentation mask data. You can access various fields like:

=== "Python"

    ``` python
    # Access mask parameters
    width = mask.width
    height = mask.height
    data = mask.data  # Binary mask data
    class_id = mask.class_id
    ```

=== "Rust"

    ``` rust
    // Access mask parameters
    let width = mask.width;
    let height = mask.height;
    let data = mask.data;  // Binary mask data
    let class_id = mask.class_id;
    ```

## /model/compressed_mask

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `model/compressed_mask` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/model/compressed_mask"
    subscriber = session.declare_subscriber('rt/model/compressed_mask')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/model/compressed_mask"
    let subscriber = session
        .declare_subscriber("rt/model/compressed_mask")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.model_msgs import CompressedMask

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    mask = CompressedMask.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::model_msgs::CompressedMask;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let mask: CompressedMask = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The CompressedMask message contains compressed segmentation mask data. You can access various fields like:

=== "Python"

    ``` python
    # Access compressed mask parameters
    width = mask.width
    height = mask.height
    data = mask.data  # Compressed mask data
    class_id = mask.class_id
    ```

=== "Rust"

    ``` rust
    // Access compressed mask parameters
    let width = mask.width;
    let height = mask.height;
    let data = mask.data;  // Compressed mask data
    let class_id = mask.class_id;
    ``` 