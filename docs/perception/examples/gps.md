# GPS Schema Example

This example will go through how to connect to the GPS topic published on your EdgeFirst Platform and how to display the information through the Rerun visualizer.

### Setting up subscriber

After setting up the Zenoh session, we will create a subscriber to the `rt/gps` topic

=== "Python"

    ``` python
    # Create a subscriber for "rt/gps"
    subscriber = session.declare_subscriber('rt/gps')
    ```

### Decode GPS Data

We can now recieve message on the subcriber that will be handled by the gps_listener function. After recieving the message, we will need to deserialize it.

=== "Python"

    ``` python
    from edgefirst.schemas.sensor_msgs import NavSatFix
    gps = NavSatFix.deserialize(msg.payload.to_bytes())
    ```

### Get Latitude/Longitude Values and Post to Rerun

We will now pull out the latitude/longitude data from the decoded NavSatFix message and log the data to Rerun.

=== "Python"

    ``` python
    lat = gps.latitude
    long = gps.longitude
    print("Latitude: %.6f Longitude: %.6f" % (lat, long))
    rr.log("Current Location", rr.GeoPoints(lat_lon=[lat, long]))
    ```