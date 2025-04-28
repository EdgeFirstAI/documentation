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

## /fusion/mask_output_tracked

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/mask_output_tracked` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/mask_output_tracked"
    subscriber = session.declare_subscriber('rt/fusion/mask_output_tracked')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/mask_output_tracked"
    let subscriber = session
        .declare_subscriber("rt/fusion/mask_output_tracked")
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

## /fusion/target

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `fusion/target` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/fusion/target"
    subscriber = session.declare_subscriber('rt/fusion/target')
    ```

=== "Rust"

    ``` rust
    // Create a subscriber for "rt/fusion/target"
    let subscriber = session
        .declare_subscriber("rt/fusion/target")
        .await
        .unwrap();
    ```

### Receive a message

We can now receive a message on the subscriber. After receiving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.fusion_msgs import Target

    # Receive a message
    msg = subscriber.recv()

    # deserialize message
    target = Target.deserialize(msg.payload.to_bytes())
    ```

=== "Rust"

    ``` rust
    use edgefirst_schemas::fusion_msgs::Target;

    // Receive a message
    let msg = subscriber.recv().unwrap();

    let target: Target = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

### Process the Data

The Target message contains target tracking data. You can access various fields like:

=== "Python"

    ``` python
    # Access target parameters
    timestamp = target.timestamp
    track_id = target.track_id
    position = target.position
    velocity = target.velocity
    ```

=== "Rust"

    ``` rust
    // Access target parameters
    let timestamp = target.timestamp;
    let track_id = target.track_id;
    let position = target.position;
    let velocity = target.velocity;
    ``` 