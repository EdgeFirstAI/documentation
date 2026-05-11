# Deploy on Target

If you have a quantized ModelPack in TFLite format, you can follow the instructions below for running the model on target such as an [i.MX 8M Plus EVK](../../platforms/quickstart/imx8mplus/index.md) using a simple Python script.

You can download this [Python script](assets/run-tflite.py){: download="run-tflite.py"} script, this sample image [IMG_9004.png](assets/IMG_9004.png){: download="IMG_9004.png" }, and this [sample TFLite model](assets/coffeecup-modelpack-multitask-t-1f54.tflite){: download="coffeecup-modelpack-multitask-t-1f54.tflite"} for running the example on the target using the command below.

!!! tip "Specify model and image paths"

    If you have a specific model and a specific image, modify the paths to these files in the script.

    ```python
    model_path = "coffeecup-modelpack-multitask-t-1f54.tflite"
    image_path = "IMG_9004.png"
    ```

```shell
# python3 run-tflite.py
INFO: Vx delegate: allowed_cache_mode set to 0.
INFO: Vx delegate: device num set to 0.
INFO: Vx delegate: allowed_builtin_code set to 0.
INFO: Vx delegate: error_during_init set to 0.
INFO: Vx delegate: error_during_prepare set to 0.
INFO: Vx delegate: error_during_invoke set to 0.
ERROR: Int64 output is not supported
ERROR: Int64 input is not supported
Error in cpuinfo: prctl(PR_SVE_GET_VL) failed
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
warning at CreateOutputsTensor, #90
W [HandleLayoutInfer:332]Op 162: default layout inference pass.
Time: 37 ms
Found objects:
   1 label 0.6562237 [0.46047086 0.19032796 0.6446592  0.4359124 ]
```

A new image should be saved `img_vis.jpg` showing the model output visualizations.

{{ figure("assets/img_vis.jpg", "Model Inference") }}

## Walkthrough of the Run Model script

The `run-tflite.py` script executes the following steps to run the TFLite model on the i.MX 8M Plus OpenVX NPU.

1. Load the model specifying the external delegate to use the device's NPU.

    ```python
    model_path = "coffeecup-modelpack-multitask-t-1f54.tflite"
    delegate = "/usr/lib/libvx_delegate.so"

    ext_delegate = load_delegate(delegate, {})
    ip = Interpreter(model_path=model_path, experimental_delegates=[ext_delegate])
    ```

    !!! note "OpenVX delegate"
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
    image_path = "IMG_9004.png"

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
    box_id, score_id, mask_id = None, None, None
    outputs = []
    for i, out in enumerate(out_det):
        x = ip.get_tensor(out["index"])

        # Output Dequantization
        scale, zero_point = out["quantization"]
        if x.dtype != np.float32 and scale > 0:
            x = (x.astype(np.float32) - zero_point) * scale  # re-scale
        outputs.append(x)

        shape = out.get("shape")
        if len(shape) == 4 and shape[-1] == 4:
            box_id = i
        elif len(shape) == 3:
            if shape[-1] == nc:
                score_id = i
            else:
                mask_id = i
    ```

8. Postprocess outputs and apply NMS.

    ```python
    boxes = outputs[box_id][0]  # shape (n, 4)
    scores = outputs[score_id][0]  # shape (n, num_classes)
    masks = outputs[mask_id][0]  # shape (h, w)
    
    boxes = np.reshape(boxes, (-1, 4))
    scores = np.reshape(scores, (boxes.shape[0], -1))
    classes = np.argmax(scores, axis=1).astype(np.int32)

    # Prefilter boxes and scores by minimum score
    max_scores = np.max(scores, axis=1)
    filt = max_scores >= score_threshold

    # Prefilter the boxes, scores and classes IDs.
    scores = max_scores[filt]
    boxes = boxes[filt]
    classes = classes[filt]

    keep = numpy_nms(boxes, scores, iou_threshold=iou_threshold)
    boxes = boxes[keep]
    classes = classes[keep]
    scores = scores[keep]
    masks = resize_mask(masks, size)
    ```

## Next Steps

In this section you have seen how you can utilize a simple python script to run model inference on a single input image.  For an example on deploying the model on target on a live camera feed, proceed to [Deploying to Embedded Targets](../deployment/launcher.md).
