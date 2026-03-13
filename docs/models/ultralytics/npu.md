# Deploying Models on the Target

This section will provide a demo for deploying a quantized ONNX and TFLite model from Ultralytics using the NPU in the i.MX 8M Plus EVK.

## Deploying Quantized ONNX

In this example, we have taken the pretrained quantized ONNX model from the [ONNX model zoo](https://github.com/onnx/models/tree/main/validated/vision/object_detection_segmentation/ssd-mobilenetv1).   In particular the SSD-MobilenetV1-12-int8 was downloaded.

!!! tip "ONNX Deployment"
    When deploying ONNX models on target, it is recommended to quantize the ONNX to deploy on the NPU using these providers `['NnapiExecutionProvider', 'VsiNpuExecutionProvider']` or convert it to FP16 to deploy on the GPU using this provider `["CUDAExecutionProvider"]`.

Download our [Python Script](assets/run-onnx.py){: download="run-onnx.py"} for running the example.

Lastly, you can try this sample image [000000000064.jpg](assets/000000000064.jpg){: download="000000000064.jpg" } taken from [COCO128](https://www.kaggle.com/datasets/ultralytics/coco128).

<figure markdown="span">
![Sample COCO Image](assets/000000000064.jpg){ align=center }
<figcaption>Sample COCO Image</figcaption>
</figure>

Once the files have been downloaded, [SCP](../../platforms/networking/ssh.md#secure-copy) the files into the embedded platform.

Run the script with the command `python3 run-onnx.py`.  The script should print the inference time in milliseconds and the model detections as follows.

```shell
2025-08-21 00:02:49.820540730 [W:onnxruntime:, transformer_memcpy.cc:83 ApplyImpl] 19 Memcpy nodes are added to the graph tf2onnx for CUDAExecutionProvider. It might have negative impact on performance (including unable to run CUDA graph). Set session_options.log_severity_level=1 to see the detail logs before this message.
2025-08-21 00:02:50.229739399 [W:onnxruntime:, transformer_memcpy.cc:83 ApplyImpl] 5 Memcpy nodes are added to the graph tf2onnx__44 for CUDAExecutionProvider. It might have negative impact on performance (including unable to run CUDA graph). Set session_options.log_severity_level=1 to see the detail logs before this message.
Time: 89 ms
Found objects:
   85 clock 0.9623478 [0.04242745 0.23638025 0.32066926 0.566869  ]
   3 car 0.6170904 [0.6252131  0.11427537 0.8362978  0.40256432]
   3 car 0.35680234 [0.60697377 0.10544738 0.8504381  0.52560043]
   3 car 0.34608585 [0.6352387  0.10221773 0.83975834 0.29047823]
```

A new image should be saved `img_vis.jpg` showing the model output visualizations.

<figure markdown="span">
![Model Inference](assets/img_vis-onnx.jpg){align=center}
<figcaption>Model Inference</figcaption>
</figure>

The following breakdown of the script describing the steps of the model inference is provided below.

1. Load the model specifying the execution provider using the device's inference engine.

    ```python
    model_path = "ssd_mobilenet_v1_12-int8.onnx"

    session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    ```

    !!! note "Execution Providers"
        The device NPU can be specified with `['NnapiExecutionProvider', 'VsiNpuExecutionProvider']`.  The NPU exeution providers are not seen in later BSPs such as 6.12.  However, these providers can be seen in lower BSPs like 5.15.

        The device GPU can be specified with `['CUDAExecutionProvider']`.

2. Preprocess input image by resizing to the input shape of the model and type-casting the values to the input data type requirements of the model.

    ```python
    image_path = "000000000064.jpg"
    input_name = session.get_inputs()[0].name
    input_shape = session.get_inputs()[0].shape
    dtype = session.get_inputs()[0].type
    input_dtype = np.uint8 if "uint8" in dtype else np.float32
    height, width = 640, 640

    image = Image.open(image_path)
    img = np.array(image.resize((width, height)))
    img = np.expand_dims(img, axis=0).astype(input_dtype)
    ```

3. Run model inference by calling the run() function.

    ```python
    outputs = session.run(None, {input_name: img})
    ```

4. Query model outputs and filter by score.

    ```python
    boxes, classes, scores, _ = outputs
    boxes = boxes.squeeze()
    classes = classes.squeeze()
    scores = scores.squeeze()

    mask = scores >= score_threshold
    boxes = boxes[mask]
    classes = classes[mask]
    scores = scores[mask]
    ```

These outputs can then be taken and visualized as shown in the Python script.

## Deploying Quantized TFLite

In this example, we have taken the [small PyTorch segmentation model](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s-seg.pt) from Ultralytics and [exported the model to a quantized TFLite](quantize.md).  Once the TFLite is exported, you can deploy it on target as shown below.

=== "i.MX 8M Plus"

    For i.MX 8M Plus, download this [Python Script](assets/run-tflite.py){: download="run-tflite.py"} for running the example.  

    Next, you can also download this [sample TFLite model](assets/yolov8s-seg_full_integer_quant.tflite){: download="yolov8s-seg_full_integer_quant.tflite"} for running the demo. Otherwise, update the path to your own YOLO segmentation TFLite model in the python script. 

    Lastly, you can try this sample image [000000000064.jpg](assets/000000000064.jpg){: download="000000000064.jpg" } taken from [COCO128](https://www.kaggle.com/datasets/ultralytics/coco128). 

    <figure markdown="span">
    ![Sample COCO Image](assets/000000000064.jpg){ align=center }
    <figcaption>Sample COCO Image</figcaption>
    </figure>

    Once the files have been downloaded, [SCP](../../platforms/networking/ssh.md#secure-copy) the files into the embedded platform.

    Run the script with the command `python3 run-tflite.py`.  The script should print the inference time in milliseconds and the model detections as follows.

    ```shell
    # python3 run-tflite.py
    INFO: Vx delegate: allowed_cache_mode set to 0.
    INFO: Vx delegate: device num set to 0.
    INFO: Vx delegate: allowed_builtin_code set to 0.
    INFO: Vx delegate: error_during_init set to 0.
    INFO: Vx delegate: error_during_prepare set to 0.
    INFO: Vx delegate: error_during_invoke set to 0.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    warning at CreateOutputsTensor, #90
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 56: default layout inference pass.
    W [HandleLayoutInfer:332]Op 56: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    W [HandleLayoutInfer:332]Op 162: default layout inference pass.
    Time: 203 ms
    Found objects:
    74 label 0.66109437 [0.22954665 0.06427306 0.5417301  0.30300158]
    2 label 0.33054718 [0.11018239 0.550912   0.25709224 0.58763945]
    2 label 0.25709227 [0.1101824  0.615185   0.47745705 0.8171861 ]
    ```

    A new image should be saved `img_vis.jpg` showing the model output visualizations.

    <figure markdown="span">
    ![Model Inference](assets/img_vis.jpg){align=center}
    <figcaption>Model Inference</figcaption>
    </figure>

=== "i.MX 95"

    For the i.MX 95, download this [Python Script](assets/run-tflite-neutron.py){: download="run-tflite.py"} for running the example.

    Next, you can also download this [sample TFLite model](assets/yolov8s-seg_full_integer_quant.tflite){: download="yolov8s-seg_full_integer_quant.tflite"} for running the demo. Otherwise, update the path to your own YOLO segmentation TFLite model in the python script. 

    Lastly, you can try this sample image [000000000064.jpg](assets/000000000064.jpg){: download="000000000064.jpg" } taken from [COCO128](https://www.kaggle.com/datasets/ultralytics/coco128). 

    <figure markdown="span">
    ![Sample COCO Image](assets/000000000064.jpg){ align=center }
    <figcaption>Sample COCO Image</figcaption>
    </figure>

    Once the files have been downloaded, [SCP](../../platforms/networking/ssh.md#secure-copy) the files into the embedded platform.

    Run the script with the command `python3 run-tflite.py`.  The script should print the inference time in milliseconds and the model detections as follows.

    ```shell
    # python3 run-tflite.py
    INFO: NeutronDelegate delegate: 1 nodes delegated out of 36 nodes with 1 partitions.

    INFO: Neutron delegate version: v1.0.0-a5d640e6, zerocp enabled.
    Error in cpuinfo: prctl(PR_SVE_GET_VL) failed
    INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
    Time: 73 ms
    Found objects:
    2 label 0.8302227 [0.09579493 0.5960573  0.4576869  0.8089349 ]
    74 label 0.76635945 [0.22352152 0.07450718 0.5428379  0.30867255]
    2 label 0.29802865 [0.1170827 0.5428379 0.266097  0.6067012]
    ```

    A new image should be saved `img_vis.jpg` showing the model output visualizations.

    <figure markdown="span">
    ![Model Inference](assets/img_vis.jpg){align=center}
    <figcaption>Model Inference</figcaption>
    </figure>

## Walkthrough of the Run Model script

The `run-tflite.py` script executes the following steps to run the TFLite model on the i.MX 95 Neutron NPU.

1. Load the model specifying the external delegate to use the device's NPU.

    ```python
    model_path = "yolov8s-seg_full_integer_quant_converted.tflite"
    delegate = "/usr/lib/libvx_delegate.so" # i.MX 8M Plus
    # delegate = "/usr/lib/libneutron_delegate.so" # i.MX 95

    ext_delegate = load_delegate(delegate, {})
    ip = Interpreter(model_path=model_path, experimental_delegates=[ext_delegate])
    ```

    !!! note "OpenVX Delegate"
        The OpenVX delegate is specified with `experimental_delegates=[ext_delegate]`.
        To use the CPU, remove this specification.

2. Allocate tensors to allocate memory and sets up input/output tensor bindings.

    ```python
    ip.allocate_tensors()
    ```

3. Call invoke() once at the start as a model warmup since the first call may take up to 9 seconds to run.

    ```python
    ip.invoke()
    ```

4. Preprocess input image by resizing to the input shape of the model and type-casting the values to the input data type requirements of the model.

    ```python
    image_path = "000000000064.jpg"

    input_det = ip.get_input_details()[0]
    _, height, width, _ = input_det.get("shape")
    image = Image.open(image_path)
    size = (image.height, image.width)
    img = np.array(image.resize((width, height)))

    # is TFLite quantized int8 model
    int8 = input_details["dtype"] == np.int8
    scale, zp = input_details["quantization"]
    if int8:
        zp = abs(zp)
        img = (img.astype(np.int16) - zp).astype(np.int8)
    img = np.array([img]) 
    ```

5. Query inputs from the model's input details and set the input tensor.

    ```python
    inp_id = ip.get_input_details()[0]["index"]
    ip.set_tensor(inp_id, img)
    ```

6. Run model inference by calling the invoke() function.

    ```python
    ip.invoke()
    ```

7. Query and dequantize the model outputs.

    ```python
    # Decode Boxes
    box_id, mask_id = None, None
    outputs = []
    for i, out in enumerate(out_det):
        x = ip.get_tensor(out["index"])
        if (int8 or uint8) and x.dtype != np.float32:
            scale, zero_point = out["quantization"]
            x = (x.astype(np.float32) - zero_point) * scale  # re-scale
        outputs.append(x)

        if len(out.get("shape")) > 3:
            mask_id = i
        else:
            box_id = i
    ```

8. Decode bounding box outputs and apply NMS.

    ```python
    score_threshold = 0.25
    iou_threshold = 0.70

    boxes, scores, classes, masks = decode_boxes(outputs[box_id], nc)
    
    # Filter By Score
    scores_masks = scores > score_threshold
    boxes = boxes[scores_masks]
    classes = classes[scores_masks]
    scores = scores[scores_masks]
    masks = masks[scores_masks]

    # Filter By NMS
    keep = numpy_nms(boxes, scores, thresh=iou_threshold)
    boxes = boxes[keep]
    classes = classes[keep]
    scores = scores[keep]
    masks = masks[keep]
    ```

9. Decode mask outputs.

    ```shell
    masks = decode_masks(masks, np.array(outputs[mask_id], dtype=np.float32))
    masks = resize_mask(masks, size)
    masks = crop_mask(masks, boxes)
    ```

The decoded outputs can then be taken and visualized as shown above.

!!! note "Output Decoding"
    For the decoding steps 8-9, see the python script provided above to see the functions `decode_boxes` and `decode_masks`.

## Next Steps

You can find more examples for deploying models in various platforms by following the [User Workflows](../../getting_started/workflows/index.md).
