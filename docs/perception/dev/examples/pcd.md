# PointCloud2 Decoding Example

This example will go through how to decode PointCloud2 data.  The Python sample below hand-decodes
the message into an array of `Point`s which will contain the `x`, `y`, `z` values of each point, as
well a dictionary/hashmap with all the other fields.  If only a specific field is needed, that
field can be added directly, similar to the `x`, `y`, `z` fields, and the dictionary/hashmap can be
removed to increase performance.  The Rust sample instead uses the `DynPointCloud` helper built
into `edgefirst-schemas`, which reads any named field without a hand-rolled decoder.

=== "Python"

``` python
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.fields = dict()


SIZE_OF_DATATYPE = [
    0,
    1,  # pub const INT8: u8= 1
    1,  # pub const UINT8: u8= 2
    2,  # pub const INT16: u8= 3
    2,  # pub const UINT16: u8= 4
    4,  # pub const INT32: u8= 5
    4,  # pub const UINT32: u8= 6
    4,  # pub const FLOAT32: u8= 7
    8,  # pub const FLOAT64: u8 = 8
]

STRUCT_LETTER_OF_DATATYPE = [
    "",
    "b",  # pub const INT8: u8= 1
    "B",  # pub const UINT8: u8= 2
    "h",  # pub const INT16: u8= 3
    "H",  # pub const UINT16: u8= 4
    "i",  # pub const INT32: u8= 5
    "I",  # pub const UINT32: u8= 6
    "f",  # pub const FLOAT32: u8= 7
    "d",  # pub const FLOAT64: u8 = 8
]


def decode_pcd(pcd: PointCloud2) -> list[Point]:
    points = []
    endian_format = ">" if pcd.is_bigendian else "<"
    for i in range(pcd.height):
        for j in range(pcd.width):
            point = Point()
            point_start = (i * pcd.width + j) * pcd.point_step
            # Loop through the provided Fields for each Point (x, y, z, speed,
            # power, rcs)
            for f in pcd.fields:
                val = 0
                # Decode the data according to the datatype and endian format stated
                # in the message, location in the array block determined
                # through the offset
                arr = bytearray(
                    pcd.data[(point_start + f.offset):(point_start + f.offset + SIZE_OF_DATATYPE[f.datatype])])
                val = struct.unpack(
                    f'{endian_format}{STRUCT_LETTER_OF_DATATYPE[f.datatype]}', arr)[0]
                if f.name == "x":
                    point.x = val
                elif f.name == "y":
                    point.y = val
                elif f.name == "z":
                    point.z = val
                else:
                    point.fields[f.name] = val
            points.append(point)
    return points
```

=== "Rust"

    The `edgefirst-schemas` crate provides a built-in `DynPointCloud` helper that reads the
    `PointCloud2` field layout for you, so there's no need to hand-roll a decoder as shown in the
    Python tab.  Build it once from the message with `from_pointcloud2`, then `iter()` it to read
    any named field (`x`, `y`, `z`, `speed`, `power`, `rcs`, `cluster_id`, `vision_class`, ...)
    with automatic datatype conversion and endian handling.

    ``` rust
    use edgefirst_schemas::sensor_msgs::{PointCloud2, pointcloud::DynPointCloud};

    let pcd = PointCloud2::from_cdr(msg.payload().to_bytes())?;
    let cloud = DynPointCloud::from_pointcloud2(&pcd)?;

    for point in cloud.iter() {
        let x = point.read_f32("x").unwrap_or(0.0);
        let y = point.read_f32("y").unwrap_or(0.0);
        let z = point.read_f32("z").unwrap_or(0.0);

        // Any other field is read the same way; `read_as_f32`/`read_as_f64`
        // convert automatically regardless of the field's wire datatype.
        let speed = point.read_as_f32("speed").unwrap_or(0.0);
    }
    ```
