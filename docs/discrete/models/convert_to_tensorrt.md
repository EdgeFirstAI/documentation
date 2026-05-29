Conversion has two stages: EdgeFirst Studio packages the ONNX model and supporting files into a portable `.tensorrt.zip` bundle, and then `build.sh` runs on the target Jetson to compile the engine. The bundle itself is portable across machines; the resulting `.engine` is hardware-specific and must be built on (or for) the device that will run it.

!!! info "Native cross-compilation support"

    Native cross-compilation of TensorRT engines is in progress and will eliminate the second on-device build stage when available.

1. Click on the completed training session.

    {{ figure("/models/assets/training/vision-view-train-details.jpg", "Completed Training Session") }}

2. Navigate to the **Artifacts** tab and click the **TensorRT Converter** button under **Converters** on the right.

    {{ figure("/models/assets/conversion/tensorrt-converter-button.jpg", "TensorRT Converter") }}

3. Click **Start App** to begin the conversion. The launch form has no settings — the output is a portable bundle, not a final engine.

    {{ figure("/models/assets/conversion/tensorrt-converter-options.jpg", "TensorRT Converter Options") }}

4. Download the resulting `<model>.tensorrt.zip` bundle from the session's **Artifacts** tab.

    {{ figure("/models/assets/conversion/tensorrt-converter-bundle.jpg", "TensorRT Converter Bundle") }}

5. Copy the bundle to the Jetson via [SCP](https://en.wikipedia.org/wiki/Secure_copy_protocol):

    ```shell
    $ scp <model>.tensorrt.zip username@hostname:~/
    ```

6. On the Jetson, unzip the bundle into a folder:

    ```shell
    $ unzip -d <model>/ <model>.tensorrt.zip
    ```

7. Enter the extracted folder:

    ```shell
    $ cd <model>/
    ```

    !!! note "Prerequisites"

        Steps a and b ensure the required binaries are on `PATH`. Steps c and d authenticate the `--publish` upload to EdgeFirst Studio.

        1. Ensure the `trtexec` binary is on `PATH`:

            ```shell
            $ export PATH=$PATH:/usr/src/tensorrt/bin
            ```

        2. Ensure `jq` is installed:

            ```shell
            $ sudo apt install -y jq
            ```

        3. Install the [edgefirst-client](../../perception/studio.md) package:

            ```shell
            $ pip3 install edgefirst-client
            ```

        4. Log in to EdgeFirst Studio:

            ```shell
            $ edgefirst-client login
            ```

8. Compile the bundle into a TensorRT engine with `--publish` to push the sealed artifact back to EdgeFirst Studio.

    Run the build:

    ```shell
    $ ./build.sh fp16 --publish
    ```

    The script verifies `trtexec`, `jq`, and `python3` are on `PATH` (all default on JetPack 6.2), then:

    1. Calls `trtexec --onnx=model.onnx --fp16 --saveEngine=<name>.fp16.engine`.
    2. Updates `edgefirst.json` with on-target build values via `jq` (precision, engine `sha256`, build timestamp, on-device TRT version, builder flags).
    3. ZIP-appends `edgefirst.json` and `labels.txt` to the engine using Python's `zipfile` module.
    4. If `--publish` is set, uploads the sealed engine to Studio via `edgefirst-client upload-artifact`. See the [edgefirst-client](../../perception/studio.md) page for more.

    The output is a sealed `.fp16.engine` with metadata readable by any ZIP reader; the TensorRT deserializer ignores trailing bytes.

9. The compiled `<model>.fp16.engine` is now ready to deploy. The artifact is also available in the Studio session for re-download to other compatible devices. Verify the engine loads successfully with:

    ```shell
    $ trtexec --loadEngine=<model>.fp16.engine --iterations=100
    ```
