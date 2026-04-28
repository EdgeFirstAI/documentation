# TensorRT Conversion

Once the model is trained in EdgeFirst Studio.  A Keras, ONNX, and TFLite model will be available for users to download.  

{{ figure("/models/assets/training/vision-session-artifacts.jpg", "Model Artifacts") }}

This tutorial will provide the steps for converting the ONNX model to TensorRT.  Although it is possible to deploy the ONNX model, we recommend converting this model to TensorRT when deploying in the Jetson to maximize the performance of the model.  We find that the converted TensorRT model is **~1.3x faster** than ONNX with the TensorRT execution provider. 

The common conversion for the EdgeFirst workflow is [ONNX to TensorRT](#convert-onnx-to-tensorrt).  However, [PyTorch to TensorRT](#convert-pytorch-to-tensorrt) is also possible when using the [Ultralytics framework](https://docs.ultralytics.com/modes/export/).  Since we focus on the Jetson Orin Nano in our examples, we recommend following through the [ONNX to TensorRT using the Jetson Orin](#jetson-orin).

## Convert ONNX to TensorRT

{% include-markdown "discrete/models/onnx_to_tensorrt.md" %}

## Convert PyTorch to TensorRT

This section converts a PyTorch model to TensorRT using the [Ultralytics Framework](https://docs.ultralytics.com/modes/export/). 

1. On a terminal, install the ultralytics framework using `pip install ultralytics`

2. Download a sample PyTorch model from Ultralytics 

    ```shell
    $ wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s-seg.pt
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

        Run this command to convert the PyTorch model to TensorRT with half precision 

        ```shell
        $ yolo export model=yolov8s-seg.pt format=engine device=dla:1 half=True
        ```

        !!! note "Device Specification"
            Depending on your hardware, specify the device to either of the following or none at all.
            
            * Use CUDA GPU `device=0`
            * Use DLA (Deep Learning Accelerator) - available in platforms such as the Jetson Orin `device=dla:X`

    === "To ONNX"

        Run this command to convert the model to ONNX with half precision.
        
        ```shell
        $ yolo export model=yolov8s-seg.pt format=onnx half=True
        ```

        Next take the converted ONNX model and follow the steps for [ONNX to TensorRT using the Jetson Orin](#jetson-orin).

## Inspect TensorRT Model

Once the conversion completes, you can inspect the I/O shapes and datatypes to verify that the resulting conversion is expected.

1. Create a python script named [inspect_engine.py](../../platforms/quickstart/jetson_orin/assets/inspect_engine.py){: download="inspect_engine.py"} and modify the path to the model in the script `/path/to/model.engine`

    ```python
    import tensorrt as trt
    import io
    import zipfile

    logger = trt.Logger(trt.Logger.WARNING)

    def find_zip_start(data: bytes):
        """Return the first local ZIP header offset if a ZIP is embedded."""
        if len(data) < 22:
            return None
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                infos = zf.infolist()
                if not infos:
                    return None
                return min(info.header_offset for info in infos)
        except zipfile.BadZipFile:
            return None

    def extract_engine_bytes(data: bytes) -> bytes:
        """Strip ZIP trailer or extract engine payload when input is a ZIP."""
        zip_start = find_zip_start(data)
        if zip_start is None:
            return data
        if zip_start > 0:
            return data[:zip_start]

        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = [
                info.filename for info in zf.infolist()
                if not info.is_dir()
            ]
            engine_names = [
                name for name in names
                if name.lower().endswith((".engine", ".trt", ".plan"))
            ]
            candidate = engine_names[0] if engine_names else max(
                names,
                key=lambda name: zf.getinfo(name).file_size,
            )
            return zf.read(candidate)

    with open("/path/to/model.engine", "rb") as f:
        runtime = trt.Runtime(logger)
        file = f.read()
        engine_blob = extract_engine_bytes(file)
        engine = runtime.deserialize_cuda_engine(engine_blob)

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
