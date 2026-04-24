# Deploying Ultralytics in the PC

If you have an ONNX or a TFLite Ultralytics model, you can follow these instructions for running the model on your PC.  You will need [Python 3.10](https://www.python.org/downloads/) to run this example.

If you have an ONNX model, download the [run-onnx.py Python script](../assets/run-yolo-onnx.py){: download="run-onnx.py"}.  Otherwise, if you have a TFLite model, download the [run-tflite.py Python script](../assets/run-yolo-tflite.py){: download="run-tflite.py"}.  These scripts will load the model for inference across multiple images and saves the images with visualizations in your PC.  Run the scripts with the steps shown below.

As mentioned under [Quick Start -> Train a Vision Model](../../../getting_started/train_vision.md), you can find the trained model artifacts (.onnx or .tflite) in the training session which you can then download into your PC.

{{ figure("/models/assets/training/vision-session-artifacts-ultralytics.jpg", "Training Session Artifacts") }}

For this Python script you will need a set of images and a model file.  You can click on the following link and download these [set of images with coffee cup samples](../assets/coffeecup.zip){: download="coffeecup.zip"}.  Once downloaded, unzip the file into a directory.  Next download a sample [ONNX](../assets/coffeecup-yolov8n-segmentation-rgb-640x640-t-266e.onnx){: download="coffeecup-yolov8n-segmentation-rgb-640x640-t-266eonnx"} or [TFLite](../assets/coffeecup-yolov8n-segmentation-rgb-640x640-t-266e_quant-u8-i8.tflite){: download="coffeecup-yolov8n-segmentation-rgb-640x640-t-266e_quant-u8-i8.tflite"} model to run the following examples.

1. Install required dependencies.

    === "ONNX"

        ```shell
        pip install onnxruntime-gpu pillow numpy
        ```

        !!! note "Tested Versions"
            
            The following versions of these dependencies were tested.

            ```
            $ pip list
            Package         Version
            --------------- -------
            numpy           2.2.6
            onnxruntime-gpu 1.23.2
            pillow          12.0.0
            ```

    === "TFLite"

        ```shell
        pip install tensorflow pillow numpy
        ```

        !!! note "Tested Versions"
            
            The following versions of these dependencies were tested.

            ```
            $ pip list
            Package         Version
            --------------- -------
            numpy           2.2.6
            tensorflow      2.20.0
            pillow          12.0.0
            ```

2. Run the script

    === "ONNX"

        If you have downloaded the sample images and the ONNX model above, run this command to use the script.  Otherwise modify the path to the model and the images specific to your system.  If you have multiple labels in your dataset specify them as `--labels bench coco` for example.

        ```shell
        $ python run-onnx.py coffeecup-yolov8n-segmentation-rgb-640x640-t-266e.onnx coffeecup/*.jpg --labels coffeecup --save results
        Using Execution Providers: ['CUDAExecutionProvider', 'CPUExecutionProvider']
        Objects found in image:  20250430_172430_17.jpg
        0 coffeecup 0.9715922 [0.10267723 0.05801326 0.3234266  0.4559123 ]
        0 coffeecup 0.9628352 [0.4175132  0.13497958 0.5866379  0.48802176]
        0 coffeecup 0.9602233 [0.27721608 0.3844774  0.5638     0.83782506]
        Objects found in image:  IMG_9007_13.jpg
        0 coffeecup 0.970845 [0.09871185 0.2060864  0.33400756 0.5183377 ]
        Objects found in image:  IMG_9015_35.jpg
        0 coffeecup 0.9790739 [0.1998756  0.30725    0.61030895 0.7444632 ]
        Objects found in image:  IMG_9028_86.jpg
        0 coffeecup 0.9756339 [0.26327372 0.368227   0.68208754 0.76707125]
        Average Inference Time: 51.75 ms
        ```

    === "TFLite"

        If you have downloaded the sample images and the TFLite model above, run this command to use the script.  Otherwise modify the path to the model and the images specific to your system.  If you have multiple labels in your dataset specify them as `--labels bench coco` for example.

        ```shell
        $ python run-yolo-tflite.py coffeecup-yolov8n-segmentation-rgb-640x640-t-266e_quant-u8-i8.tflite coffeecup/*.jpg --labels coffeecup --save results
        2026-04-24 16:16:26.304031: I external/local_xla/xla/tsl/cuda/cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
        2026-04-24 16:16:26.352894: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
        To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
        2026-04-24 16:16:27.474238: I external/local_xla/xla/tsl/cuda/cudart_stub.cc:31] Could not find cuda drivers on your machine, GPU will not be used.
        /home/john/Repositories/Benchmarks/venv/lib/python3.10/site-packages/tensorflow/lite/python/interpreter.py:457: UserWarning:     Warning: tf.lite.Interpreter is deprecated and is scheduled for deletion in
            TF 2.20. Please use the LiteRT interpreter from the ai_edge_litert package.
            See the [migration guide](https://ai.google.dev/edge/litert/migration)
            for details.
            
        warnings.warn(_INTERPRETER_DELETION_WARNING)
        INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
        Objects found in image:  20250430_172430_17.jpg
        0 coffeecup 0.97604585 [0.10980516 0.07320344 0.32941547 0.4636218 ]
        0 coffeecup 0.97604585 [0.4270201  0.14640687 0.59782815 0.48802292]
        0 coffeecup 0.9516447 [0.26841262 0.3782178  0.56122637 0.84183955]
        Objects found in image:  IMG_9007_13.jpg
        0 coffeecup 0.97604585 [0.10980516 0.20740974 0.32941547 0.52462465]
        Objects found in image:  IMG_9015_35.jpg
        0 coffeecup 0.97604585 [0.20740975 0.3172149  0.6222293  0.7564356 ]
        Objects found in image:  IMG_9028_86.jpg
        0 coffeecup 0.97604585 [0.25621206 0.3660172  0.67103153 0.7564355 ]
        Average Inference Time: 122.50 ms
        ```

3. See the model output visualizations.

    A directory called "results" should be created which contains the same input images with annotations to visualize the output of the trained model.

    === "ONNX"

        | 20250430_172430_17.jpg                              | IMG_9007_13.jpg                              |
        |-----------------------------------------------------|----------------------------------------------|
        | ![1](../assets/results-onnx/20250430_172430_17-yolo.jpg) | ![2](../assets/results-onnx/IMG_9007_13-yolo.jpg) |

        | IMG_9015_35.jpg                              | IMG_9028_86                                  |
        |----------------------------------------------|----------------------------------------------|
        | ![3](../assets/results-onnx/IMG_9015_35-yolo.jpg) | ![4](../assets/results-onnx/IMG_9028_86-yolo.jpg) |

    === "TFLite"

        | 20250430_172430_17.jpg                                | IMG_9007_13.jpg                                |
        |-------------------------------------------------------|------------------------------------------------|
        | ![1](../assets/results-tflite/20250430_172430_17-yolo.jpg) | ![2](../assets/results-tflite/IMG_9007_13-yolo.jpg) |

        | IMG_9015_35.jpg                                | IMG_9028_86                                    |
        |------------------------------------------------|------------------------------------------------|
        | ![3](../assets/results-tflite/IMG_9015_35-yolo.jpg) | ![4](../assets/results-tflite/IMG_9028_86-yolo.jpg) |
