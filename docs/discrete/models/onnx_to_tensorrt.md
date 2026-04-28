=== "EdgeFirst Studio"

    This section describes how to convert an ONNX model into a TensorRT model using EdgeFirst Studio. The process has two stages.

    In the first stage, EdgeFirst Studio packages the ONNX model into a ".tensorrt.zip" bundle.  This bundle includes the original ONNX file, a "build.sh" script, and supporting files such as "edgefirst.json" and "labels.txt".  The script is used later to compile the model into a TensorRT engine.  The conversion process is handled by the [tensorrt-converter](https://github.com/EdgeFirstAI/tensorrt-converter) package.

    In the second stage, you run the build.sh script on the target device (for example, a Jetson Orin).  This step compiles the model into a .engine file optimized specifically for that hardware.

    The .tensorrt.zip bundle is portable and can be moved between systems.  However, the generated TensorRT engine is hardware-specific and must be built on (or for) the platform where it will be used for inference.  Once compiled, the optimized model can be deployed on the device or uploaded back to EdgeFirst Studio.

    1. Click on the completed training session

        {{ figure("/models/assets/training/vision-view-train-details.jpg", "Completed Training Session") }}

    2. Navigate to the "Artifacts" tab and click on the "TensorRT Converter" button under "Converters" on the right

        {{ figure("/models/assets/conversion/tensorrt-converter-button.jpg", "TensorRT Converter") }}

    3. Click on "Start App" to start the conversion process

        {{ figure("/models/assets/conversion/tensorrt-converter-options.jpg", "TensorRT Converter Options") }}

    4. This will publish an artifact to the session with the extension "<model>.tensorrt.zip" bundle.  Go ahead and download this artifact to your PC

        {{ figure("/models/assets/conversion/tensorrt-converter-bundle.jpg", "TensorRT Converter Bundle") }}

    5. [SCP](https://en.wikipedia.org/wiki/Secure_copy_protocol) the downloaded .tensorrt.zip file into the Jetson Orin to execute the second stage of the conversion process

        ```shell
        $ scp <model>.tensorrt.zip username@hostname:~/
        ```

    6. Unzip the model into a folder

        ```shell
        $ unzip -d <model>/ <model>.tensorrt.zip
        ```

    7. Navigate to the extracted folder `cd <model>/`

    8. Compile the model bundle into TensorRT

        !!! note "Required Actions"
            Prior to running the script below, these initialization steps are needed.

            1. The script requires the tensorrt executable to be available in your `PATH`

                ```shell
                $ export PATH=$PATH:/usr/src/tensorrt/bin
                ```

            2. The script requires the `jq` library which is installed 

                ```shell
                $ sudo apt install -y jq
                ```

            3. The `--publish` flag requires the [edgefirst-client](../../perception/studio.md) package which is installed 

                ```shell            
                $ pip3 install edgefirst-client
                ```

            4. If using the `--publish` flag, ensure you are logged in to EdgeFirst Studio

                ```shell
                $ edgefirst-client login
                ```

        ```shell
        $ ./build.sh fp16 --publish
        ```

        The script verifies trtexec, jq, and python3 are in PATH (all default on JetPack 6.2), then:

        1. Calls `trtexec --onnx=model.onnx --fp16 --saveEngine=<name>.fp16.engine`
        2. Updates "edgefirst.json" with on-target build values via `jq` (precision, engine sha256, build timestamp, on-device TRT version, builder flags)
        3. ZIP-appends "edgefirst.json" + "labels.txt" to the engine using Python's zipfile
        4. (If `--publish`) Uploads the sealed engine to Studio via `edgefirst-client upload-artifact`.  More information on [edgefirst-client](../../perception/studio.md) can be found on the link provided

        The output is a sealed `.fp16.engine` with metadata readable by any ZIP reader; the TRT deserializer ignores trailing bytes.

    9. Once converted, a model file "<model>.fp16.engine" should have been generated and published to EdgeFirst Studio as an artifact

        You can verify the model loaded succesfully with the command `trtexec --loadEngine=<model>.fp16.engine --iterations=100`

=== "Jetson Orin"

    <h2 id="jetson-orin" style="display: none;"></h2>

    This section converts ONNX to TensorRT in the NVIDIA Jetson Orin using the built in `trtexec` program.  We recommend following this section if you plan to deploy the converted TensorRT model in the Jetson Orin.  This tutorial expects the ONNX to be already stored inside the Jetson Orin. 

    1. Access the Jetson's terminal which can be done through [SSH](../../platforms/networking/ssh.md)
    2. Run the conversion command.  We recommend converting the model to FP16 precision for faster inference and negligible degradation in accuracy.  Though if you prefer to keep the model's current precision, then only pass `--onnx` and `--saveEngine` specifiers

        ```shell
        $ /usr/src/tensorrt/bin/trtexec --onnx=/path/to/mymodel.onnx --saveEngine=/path/to/mymodel.engine --fp16 --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw
        ```
    3. If you converted the model with half precision, you can inspect the size of the files and verify that the converted model is approximately half the size of the model with full precision.  The following is an example output on the Jetson Orin
    
        ```shell
        $ ls -lh *.engine
        -rw-rw-r-- 1 jetson jetson  15M Mar 20 15:29 yolov8n-seg-t-2584_fp32.engine
        -rw-rw-r-- 1 jetson jetson 9.3M Mar 20 15:43 yolov8n-seg-t-2584_full_fp16.engine
        ```