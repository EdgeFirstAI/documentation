# PointCloud2 Decoding Example

This example will go through how to decode PointCloud2 data. This will give an array of `Point`s which will contain the `x`, `y`, `z` values of each point, as well a dictionary/hashmap with all the other fields. If only a specific field is needed, that field can be added directly, similar to the `x`, `y`, `z` fields, and the dictionary/hashmap can be removed to increase performance.

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
``` rust

use edgefirst_schemas::sensor_msgs::{PointCloud2, PointField, point_field};
use std::collections::HashMap;

const SIZE_OF_DATATYPE: [usize; 9] = [
    0,
    1, // pub const INT8: u8 = 1;
    1, // pub const UINT8: u8 = 2;
    2, // pub const INT16: u8 = 3;
    2, // pub const UINT16: u8 = 4;
    4, // pub const INT32: u8 = 5;
    4, // pub const UINT32: u8 = 6;
    4, // pub const FLOAT32: u8 = 7;
    8, //pub const FLOAT64: u8 = 8;
];

struct ParsedPoint {
    x: f64,
    y: f64,
    z: f64,
    fields: HashMap<String, f64>,
}

fn decode_pcd(pcd: &PointCloud2) -> Vec<ParsedPoint> {
    let mut points = Vec::new();
    for i in 0..pcd.height {
        for j in 0..pcd.width {
            let start = (i * pcd.row_step + j * pcd.point_step) as usize;
            let end = start + pcd.point_step as usize;
            let p = if pcd.is_bigendian {
                parse_point_be(&pcd.fields, &pcd.data[start..end])
            } else {
                parse_point_le(&pcd.fields, &pcd.data[start..end])
            };
            points.push(p);
        }
    }
    points
}

fn parse_point_le(fields: &[PointField], data: &[u8]) -> ParsedPoint {
    let mut p = ParsedPoint {
        x: 0.0,
        y: 0.0,
        z: 0.0,
        fields: HashMap::new()
    };
    for f in fields {
        let start = f.offset as usize;
        let val = match f.datatype {
            point_field::INT8 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::INT8 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                i8::from_le_bytes(bytes) as f64
            }
            point_field::UINT8 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::UINT8 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                u8::from_le_bytes(bytes) as f64
            }
            point_field::INT16 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::INT16 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                i16::from_le_bytes(bytes) as f64
            }
            point_field::UINT16 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::UINT16 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                u16::from_le_bytes(bytes) as f64
            }
            point_field::INT32 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::INT32 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                i32::from_le_bytes(bytes) as f64
            }
            point_field::UINT32 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::UINT32 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                u32::from_le_bytes(bytes) as f64
            }
            point_field::FLOAT32 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::FLOAT32 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                f32::from_le_bytes(bytes) as f64
            }
            point_field::FLOAT64 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::FLOAT64 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                f64::from_le_bytes(bytes)
            }
            _ => {
                // Unknown datatype in PointField
                continue;
            }
        };
        match f.name.as_str() {
            "x" => p.x = val,
            "y" => p.y = val,
            "z" => p.z = val,
           _ => { p.fields.insert(f.name.clone(), val); },
        }
    }
    p
}

fn parse_point_be(fields: &[PointField], data: &[u8]) -> ParsedPoint {
    let mut p = ParsedPoint {
        x: 0.0,
        y: 0.0,
        z: 0.0,
        fields: HashMap::new(),
    };
    for f in fields {
        let start = f.offset as usize;

        let val = match f.datatype {
            point_field::INT8 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::INT8 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                i8::from_be_bytes(bytes) as f64
            }
            point_field::UINT8 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::UINT8 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                u8::from_be_bytes(bytes) as f64
            }
            point_field::INT16 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::INT16 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                i16::from_be_bytes(bytes) as f64
            }
            point_field::UINT16 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::UINT16 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                u16::from_be_bytes(bytes) as f64
            }
            point_field::INT32 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::INT32 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                i32::from_be_bytes(bytes) as f64
            }
            point_field::UINT32 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::UINT32 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                u32::from_be_bytes(bytes) as f64
            }
            point_field::FLOAT32 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::FLOAT32 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                f32::from_be_bytes(bytes) as f64
            }
            point_field::FLOAT64 => {
                let bytes = data[start..start + SIZE_OF_DATATYPE[point_field::FLOAT64 as usize]]
                    .try_into()
                    .unwrap_or_else(|e| panic!("Expected slice with 1 element: {:?}", e));
                f64::from_be_bytes(bytes)
            }
            _ => {
                // "Unknown datatype in PointField
                continue;
            }
        };
        match f.name.as_str() {
            "x" => p.x = val,
            "y" => p.y = val,
            "z" => p.z = val,
            _ => { p.fields.insert(f.name.clone(), val); },
        }
    }

    p
}
```