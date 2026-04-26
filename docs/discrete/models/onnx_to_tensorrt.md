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