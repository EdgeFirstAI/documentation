# Deploy Vision Model

You can deploy your model using Studio Runner - a Python implementation that demonstrates reading from the camera, run model inference, and displays the model outputs in the monitor.

1. Download the [Studio Runner Python Wheel](../../../models/deployment/assets/studio_runner_py-0.0.0-py3-none-any.whl){:download="studio_runner_py-0.0.0-py3-none-any.whl"}
2. If you don't already have a model, you can download this [sample model](../../../models/deployment/assets/coffeecup-yolov8n-segmentation-rgb-640x640-t-266e_quant-u8-i8.tflite){:download="coffeecup-yolov8n-segmentation-rgb-640x640-t-266e_quant-u8-i8.tflite"} to run this example
3. SCP both the wheel and the model to the i.MX 8M Plus

    ```shell
    scp studio_runner_py-0.0.0-py3-none-any.whl root@<ip address>:~/
    scp coffeecup-yolov8n-segmentation-rgb-640x640-t-266e_quant-u8-i8.tflite root@<ip address>:~/
    ```

4. On device, create and activate a Python Virtual Environment

    ```shell
    # python3 -m venv venv --system-site-packages
    # source venv/bin/activate
    # pip install --upgrade pip
    ```

5. Install the Studio Runner wheel; also install the [EdgeFirst Profiler](../../../profiler/index.md) for on-target validation alongside it

    ```shell
    # pip install studio_runner_py-0.0.0-py3-none-any.whl
    # pip install edgefirst-profiler
    ```

6. Run the program on target

    ```shell
    # studio-runner-py coffeecup-yolov8n-segmentation-rgb-640x640-t-266e_quant-u8-i8.tflite
    ```

    You should see the following display appear on your monitor.  This model should be able to segment coffee cups in the frame.

    {{ figure("../../../models/assets/deployment/coffeecup-detection-sample.jpg", "Sample Coffee Cup Detection") }}

!!! note "Official Deployment Applications"
    Official native deployment applications are still under development.  These instructions are provided to give users starting examples for running the model using Python.

For more deployment examples, you can deploy your model directly from your phone’s browser using [EdgeFirst Studio](../../../models/deployment/studio.md).
