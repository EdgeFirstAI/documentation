
# Bridge In API

This interface allows applications to publish data directly  to a dataset data. The application requires an access token as follows:

In Dataset Management page, select the dropdown on the top-right of a dataset, then select “Generate API Token“. This token will be used with every bridge API to upload or access samples. This token does not expire and can be reused.

![alt text](image.png)

## Generating Token

1. Select dataset
2. Select one annotation set from the dataset above
3. Enter a device name
4. Click “Generate“, a Java Web Token (Access Token) will be created for all API usage

![alt text](image-1.png)

## Generating Bridge Token via API call
 
```
auth.generate_bridge_token
Mandatory Arguments: username,dataset_id
Optional    Arguments: annotation_set_id
Returns:    New bridge token
Description:
      Generate Bridge in-out API token. 
      The login authentication token is required in the authorization header.
```

## Sending Request
Each request will have a different endpoint. The url starts with http://dveml.com and followed with a path unique to each API. Each request body must contain a form-data. The form-data must contain a “uuid“ key with value type string and “code“ key with value type string (this is the Access Token).

#### Note: 
“uuid“ and “code“ must always be at the top of all requests

 
Upload Sequence / Images
Sequence is a series of images (like a video). The steps are as follows:

To upload a sequence call the POST endpoint

```
https://test.dveml.com/samples/upload
```

 The arguments are in a JSON format:  for example

```
[
    {
        "name": "code",
        "value":"---- code ----"
    },
    {
        "name": "uuid",
        "value":"ABC2"
    },
     {
        "name": "image",
        "value":"xyz.jpg",
        "type":"file"
    },
    {
   "name": "frame_no",
   "value":"2"
    }
]
```

The argument name are as follows:

- code: access code as above
- sequence_uuid:  User supplied sequence ID  - if sequence with this sequence_uuid does not exist, a new sequence is generated in database with the following parameters. NOTE: omit sequence_uuid to upload separate images. The images will be tied into sequence only if sequence_uuid is provided. 
sequence_name: the name to create sequence if the sequence does not exist
- description: sequence description - optional
- sequence_height: sequence image height - optional - only used if uploading sequence
- sequence_width: sequence image width- optional - only used if uploading sequence
- image_height: image height - optional - only used if uploading non-sequence
- image_width: image width - optional - only used if uploading non-sequence
- date: time string in ISO format
- source: device name in string
- longitude: float64 - optional, will use longitude value from gps topic if not explicitly provided
- latitude: float64 - optional, will use latitude value from gps topic if not explicitly provided
- metadata: image EXIF in json format
- uuid: user supplied sample uuid for this image - all annotation are tied to image using this uuid
- image: image key derived from Create Sequence
- frame_no: order of frames, starting from 1
- pcd: pcd annotation filename
- gps: paramers in json format
- imu: paramers in json format
- polygon: segmentation mask as polygon in json format
Example: 
```
[{"label_index": 1,"label_name": "obj","polgyon": [[0.1, 0.2],[0.3, 0.4]...]}]
```
- box: parameters in json format
Example: 
```
[{"x": 0.1257633,"y": 0.41944844,"dx": 0.5000347,"dy": 0.50003463,"label_index": 1,"label_name":"obj"}]
```
- 3dbox:paramers in json format
Example: 
```
[{"x": 1.1257633,"y": 0.41944844,"z": -0.109848246,"dx": 0.5000347,"dy": 0.50003463,"dz": 0.5990741,"label_index": 1,"label_name":"obj"}]
```
- radar: radar binary filename
- depthmap: depth data filename
- cube: filename
- scales: filename
 

This will return an array of s3 keys and pre-signed url as follows:

```
{
    "result": [
        {
            "key": "s3::auzone-dve-test::/dvedata/mm_s_Organization_2/COCO_80/datasets/coco128_440/abc.pcd",
            "url": "https://auzone-dve-test.s3.us-west-2.amazonaws.com/dvedata/mm_s_Organization_2/COCO_80/datasets/coco128_440/abc.pcd?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASUMHIDCORZY72ELV%2F20240619%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240619T224954Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=c912a3d9bea10713e950cd2a78230c9293a187b5d2f4b43fc4297a03b32cd5a0",
            "filename": "abc.pcd"
        },
        {
            "key": "s3::auzone-dve-test::/dvedata/mm_s_Organization_2/COCO_80/datasets/coco128_440/xyz.jpg",
            "url": "https://auzone-dve-test.s3.us-west-2.amazonaws.com/dvedata/mm_s_Organization_2/COCO_80/datasets/coco128_440/xyz.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASUMHIDCORZY72ELV%2F20240619%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240619T224954Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=ca9abacff340f082a32db70331a68c76621d9e01d2cde3d1bbd2dc88d45a1077",
            "filename": "xyz.jpg"
        }
    ],
    "status": "SUCCESS"
}

```

Upload Image and annotation files
API for this is: (PUT)

pre-signed-url   as the url and image as payload

return: http 200 

# Bridge Out API

This interface allows applications to retrieve data from a dataset. The application requires an access token as follows:

In Dataset Management page, select the dropdown on the top-right of a dataset, then select “Generate API Token“. This token will be used with every bridge API to upload or access samples. This token does not expire and can be reused.

![alt text](image-2.png)

## Generating Token
- Select dataset
- Select one annotation set from the dataset above
- Enter a device name
- Click “Generate“, a Java Web Token (Access Token) will be created for all API usage.

[alt text](image-3.png)

## Get List of Samples with Pre Signed URLs

Endpoint: https://dveml.com/samples/export

Method: HTTP GET

Payload:

```
[{
 'name': 'code',
 'value': abc,
},
{
'name': 'sequence_uuid',
'value': abc,
}]
```

Return:

- JSON list of samples, where each key is the uuid of the sample
- If sample has an image, an S3 presigned URL is provided.
- If sample has file type annotations, an S3 presigned URL is provided for each file. 
- Error message if an error occurred
 

Get List of Samples Without File URLs

Endpoint: https://dveml.com/samples/list

Method: HTTP GET

Payload:
```
{
 'sequence_uuid': 'abc',
 'code': 'abc',
}
```
Return:

- JSON list of samples, where each key is the uuid of the sample.
- No of S3 Presigned Urls for images or file-type annotations.
- Error message if an error occurred.
- Get Detailed Info for Samples
- Endpoint: https://dveml.com/samples/get

Method: HTTP GET

Payload:
```
{
 'samples_uuids': '[abcd-1234, abcde-123]',
 'code': 'abc',
}
```

Return:

- JSON list of topics for the given samples UUID
- If sample has an image, an S3 presigned URL is provided.
- If sample has file type annotations, an S3 presigned URL is provided for each file. 
- Error message if an error occurred
 