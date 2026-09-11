# GPS Schema Example

Topic: [/gps](../../topics/navsat.md#gps)  
Message: [NavSatFix](../../api/sensor_msgs.md#navsatfix)
Sample Code: [Python](https://github.com/EdgeFirstAI/samples/blob/main/python/gps.py) / [Rust](https://github.com/EdgeFirstAI/samples/blob/main/rust/gps.rs)

!!! tip "Topic Names"

    The topics below are subscribed with their bare names, which requires the Zenoh session to be opened with the namespace set to the device hostname as shown in the [Developer Guide](../index.md#subscriber).  Subscribe with a `**/` prefix, for example `**/camera/h264`, to match the topics from a session without a namespace or from a remote device.

This example will go through how to connect to the GPS topic published on your EdgeFirst Platform and how to display the information through the Rerun visualizer.

## Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `gps` topic

=== "Python"

    ``` python
    # Create a subscriber for "gps"
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)
    session.declare_subscriber('gps', drain.callback)
    ```
=== "Rust"

    ``` rust
    let subscriber = session
        .declare_subscriber("gps")
        .await
        .unwrap();
    ```

## Receive the Message

We can now receive a message on the subscriber. After receiving the message, we will set it up for processing.

=== "Python"

    ``` python
    async def gps_handler(drain):
        while True:
            msg = await drain.get_latest()
            thread = threading.Thread(target=gps_worker, args=[msg])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
    ```
=== "Rust"

    ``` rust
    use edgefirst_schemas::sensor_msgs::{NavSatFix};
    msg = subscriber.recv()
    let gps: NavSatFix = cdr::deserialize(&msg.payload().to_bytes())?;
    ```

## Process the GPS Data

We will now pull out the latitude/longitude data from the decoded NavSatFix message and log the data to Rerun.

=== "Python"

    ``` python
    def gps_worker(msg):
        gps = NavSatFix.deserialize(msg.payload.to_bytes())
        rr.log("CurrentLoc",
                rr.GeoPoints(lat_lon=[gps.latitude, gps.longitude]))
    ```
=== "Rust"

    ``` rust
    let lat = gps.latitude;
    let long = gps.longitude;
    // println!("Latitude: {} Longitude: {}",lat, long);
    let _ = rec.log("CurrentLoc", &rerun::GeoPoints::from_lat_lon([(lat, long)]));
    ```

## Results

The command line output will appear as the following

```text
Latitude: 51.036506 Longitude: -114.034886
Latitude: 51.036506 Longitude: -114.034886
Latitude: 51.036506 Longitude: -114.034886
```

When displaying the results through Rerun you will see a map with the location of your EdgeFirst Platform marked.

{{ figure("assets/gps.png", "GPS") }}
