# TensorRT Conversion

Once the model is trained in EdgeFirst Studio.  A Keras, ONNX, and TFLite model will be available for users to download.  

{{ figure("/models/assets/training/vision-session-artifacts.jpg", "Model Artifacts") }}

This tutorial will provide the steps for converting the ONNX model to TensorRT.  Although it is possible to deploy the ONNX model, we recommend converting this model to TensorRT when deploying in the Jetson to maximize the performance of the model.  We find that the converted TensorRT model is **~1.3x faster** than ONNX with the TensorRT execution provider. 

The common conversion for the EdgeFirst workflow is [ONNX to TensorRT](#convert-onnx-to-tensorrt).  However, [PyTorch to TensorRT](#convert-pytorch-to-tensorrt) is also possible when using the [Ultralytics framework](https://docs.ultralytics.com/modes/export/).  Since we focus on the Jetson Orin Nano in our examples, we recommend following through the [ONNX to TensorRT using the Jetson Orin](#jetson-orin).

## Convert ONNX to TensorRT

=== "EdgeFirst Studio"

    !!! note "Feature Coming Soon"
        This feature is currently unavailable in EdgeFirst Studio.  We recommend following through the [ONNX to TensorRT using the Jetson Orin](#jetson-orin) instead.

    This section converts ONNX to TensorRT using EdgeFirst Studio. 

    1. Click on the completed training session

        {{ figure("/models/assets/training/vision-view-train-details.jpg", "Completed Training Session") }}

    2. Navigate to the "Artifacts" tab and click on the "TensorRT Converter" button under "Converters" on the right

        {{ figure("/models/assets/conversion/tensorrt-converter-button.jpg", "TensorRT Converter") }}

    3. Select the target device for deploying the model.  Then click on "Start App" to start the conversion process

        {{ figure("/models/assets/conversion/tensorrt-converter-options.jpg", "TensorRT Converter Options") }}

=== "Jetson Orin"

    <h2 id="jetson-orin" style="display: none;"></h2>

    This section converts ONNX to TensorRT in the NVIDIA Jetson Orin using the built in `trtexec` program.  We recommend following this section if you plan to deploy the converted TensorRT model in the Jetson Orin.  This tutorial expects the ONNX to be already stored inside the Jetson Orin. 

    1. Access the Jetson's terminal which can be done through [SSH](../../platforms/networking/ssh.md)
    2. Run the conversion command.  We recommend converting the model to FP16 precision for faster inference and negligible degradation in accuracy.  Though if you prefer to keep the model's current precision, then only pass `--onnx` and `--saveEngine` specifiers

        ```shell
        /usr/src/tensorrt/bin/trtexec --onnx=/path/to/mymodel.onnx --saveEngine=/path/to/mymodel.engine --fp16 --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw
        ```
    3. If you converted the model with half precision, you can inspect the size of the files and verify that the converted model is approximately half the size of the model with full precision.  The following is an example output on the Jetson Orin
    
        ```shell
        $ ls -lh *.engine
        -rw-rw-r-- 1 jetson jetson  15M Mar 20 15:29 yolov8n-seg-t-2584_fp32.engine
        -rw-rw-r-- 1 jetson jetson 9.3M Mar 20 15:43 yolov8n-seg-t-2584_full_fp16.engine
        ```

## Convert PyTorch to TensorRT

This section converts a PyTorch model to TensorRT using the [Ultralytics Framework](https://docs.ultralytics.com/modes/export/). 

1. On a terminal, install the ultralytics framework using `pip install ultralytics`

2. Download a sample PyTorch model from Ultralytics 

    ```shell
    wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s-seg.pt
    ```

    !!! note "List of Models"
        Here is a list of models that can be fetched from Ultralytics.

        **Detection**
        
        * Nano: "yolov8n.pt"
        * Small: "yolov8s.pt"
        * Medium: "yolov8m.pt"
        * Large: "yolov8l.pt"
        * X: "yolov8x.pt"

        **Segmentation**

        * Nano: "yolov8n-seg.pt"
        * Small: "yolov8s-seg.pt"
        * Medium: "yolov8m-seg.pt"
        * Large: "yolov8l-seg.pt"
        * X: "yolov8x-seg.pt"

3. You can either export the PyTorch model directly to TensorRT or export the model to ONNX first and then use the `trtexec` program in the Jetson Orin to convert the ONNX to TensorRT

    !!! warning "Target-Specific Conversion"
        If you plan to deploy a TensorRT model on the Jetson Orin, it must be generated on the target device.  TensorRT optimizes the model for the specific hardware architecture, so engines built on one platform may not be compatible with another.

        The same principle applies to all platforms — always perform conversion on the device where the model will be deployed.

    === "To TensorRT"

        Run this command to convert the model to TensorRT `yolo export model=yolov8s-seg.pt format=engine device=dla:1 half=True`

        !!! note "Device Specification"
            Depending on your hardware, specify the device to either of the following or none at all.
            
            * Use CUDA GPU `device=0`
            * Use DLA (Deep Learning Accelerator) - available in platforms such as the Jetson Orin `device=dla:X`

    === "To ONNX"

        Run this command to convert the model to ONNX `yolo export model=yolov8s-seg.pt format=onnx batch=1 half=True`

        Next take the converted ONNX model and follow the steps for [ONNX to TensorRT using the Jetson Orin](#jetson-orin).

## Inspect TensorRT Model

Once the conversion completes, you can inspect the I/O shapes and datatypes to verify that the resulting conversion is expected.

1. Create a python script named "inspect_engine.py" and modify the path to the model in the script `/path/to/model.engine`

    ```shell
    import tensorrt as trt

    logger = trt.Logger(trt.Logger.WARNING)

    with open("/path/to/model.engine", "rb") as f:
        runtime = trt.Runtime(logger)
        engine = runtime.deserialize_cuda_engine(f.read())

    num_tensors = engine.num_io_tensors

    for i in range(num_tensors):
        name = engine.get_tensor_name(i)
        dtype = engine.get_tensor_dtype(name)
        shape = engine.get_tensor_shape(name)
        mode = engine.get_tensor_mode(name)  # INPUT or OUTPUT

        print(f"{i}: {name}")
        print(f"   mode: {mode}")
        print(f"   dtype: {dtype}")
        print(f"   shape: {shape}")

    fp16 = False

    for i in range(engine.num_io_tensors):
        name = engine.get_tensor_name(i)
        if engine.get_tensor_dtype(name) == trt.DataType.HALF:
            fp16 = True

    print("Engine uses FP16 I/O:", fp16)
    ```

2. Run the script using `python inspect_engine.py`.  For example, a model converted with half precision will print the following output using the script

    ```shell
    0: images
        mode: TensorIOMode.INPUT
        dtype: DataType.HALF
        shape: (1, 3, 640, 640)
    1: output0
        mode: TensorIOMode.OUTPUT
        dtype: DataType.HALF
        shape: (1, 116, 8400)
    2: output1
        mode: TensorIOMode.OUTPUT
        dtype: DataType.HALF
        shape: (1, 32, 160, 160)
    Engine uses FP16 I/O: True
    ```
