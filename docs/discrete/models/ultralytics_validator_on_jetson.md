# Multi-Framework Validation

This guide will show you how to setup and run validation in the Jetson Orin.  You can either deploy the validator from the [Ultralytics Framework](https://docs.ultralytics.com/modes/val/) or [EdgeFirst Validator](https://pypi.org/project/edgefirst-validator/).

## Ultralytics Validation

This guide will show how to use the [Ultralytics Validator](https://docs.ultralytics.com/modes/val/) in the Jetson Orin.  This guide expects you to have a [Jetson Orin setup](../../platforms/quickstart/jetson_orin/setup.md) already.  Please follow the setup guide to setup your Jetson Orin with a python environment activated that will be used in this instruction.

### Install Ultralytics and Dependencies

Start by installing the Ultralytics framework and the required dependencies.  The setup installations for PyTorch and TorchVision is based on this [article](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html#prereqs-install) and this [forum](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048).  However, these instructions have been modified to be compatible with Jetpack v6.2.1 deployed in the device.

1. Install Ultralytics `pip install ultralytics`
2. Check the CUDA version of the device `nvidia-smi`.  In this case, the CUDA version is `12.6`

    ```shell
    +---------------------------------------------------------------------------------------+
    | NVIDIA-SMI 540.4.0                Driver Version: 540.4.0      CUDA Version: 12.6     |
    |-----------------------------------------+----------------------+----------------------+
    | GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
    |                                         |                      |               MIG M. |
    |=========================================+======================+======================|
    |   0  Orin (nvgpu)                  N/A  | N/A              N/A |                  N/A |
    | N/A   N/A  N/A               N/A /  N/A | Not Supported        |     N/A          N/A |
    |                                         |                      |                  N/A |
    +-----------------------------------------+----------------------+----------------------+

    +---------------------------------------------------------------------------------------+
    | Processes:                                                                            |
    |  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
    |        ID   ID                                                             Usage      |
    |=======================================================================================|
    |  No running processes found                                                           |
    +---------------------------------------------------------------------------------------+
    ```

3. Install system packages required by PyTorch

    ```shell
    $ sudo apt-get -y update
    $ sudo apt-get install -y python3-pip libopenblas-dev;
    ```

4. Install [cusparselt](../../platforms/quickstart/jetson_orin/assets/install_cusparselt.sh){: download="install_cusparselt.sh"}.  Click on the link to download "install_cusparselt.sh" and SCP the file into the Jetson Orin
    
    The contents of "install_cusparselt.sh" is as follows.  You can also copy and paste the contents and create this file in your Jetson Orin.

    ```sh
    #!/bin/bash

    set -ex

    # cuSPARSELt license: https://docs.nvidia.com/cuda/cusparselt/license.html
    mkdir tmp_cusparselt && cd tmp_cusparselt

    if [[ ${CUDA_VERSION:0:4} =~ ^12\.[1-6]$ ]]; then
        arch_path='sbsa'
        export TARGETARCH=${TARGETARCH:-$(uname -m)}
        if [ ${TARGETARCH} = 'amd64' ] || [ "${TARGETARCH}" = 'x86_64' ]; then
            arch_path='x86_64'
        fi
        CUSPARSELT_NAME="libcusparse_lt-linux-${arch_path}-0.5.2.1-archive"
        curl --retry 3 -OLs https://developer.download.nvidia.com/compute/cusparselt/redist/libcusparse_lt/linux-${arch_path}/${CUSPARSELT_NAME}.tar.xz
    elif [[ ${CUDA_VERSION:0:4} == "11.8" ]]; then
        CUSPARSELT_NAME="libcusparse_lt-linux-x86_64-0.4.0.7-archive"
        curl --retry 3 -OLs https://developer.download.nvidia.com/compute/cusparselt/redist/libcusparse_lt/linux-x86_64/${CUSPARSELT_NAME}.tar.xz
    fi

    tar xf ${CUSPARSELT_NAME}.tar.xz
    sudo cp -a ${CUSPARSELT_NAME}/include/* /usr/local/cuda/include/
    sudo cp -a ${CUSPARSELT_NAME}/lib/* /usr/local/cuda/lib64/
    cd ..
    rm -rf tmp_cusparselt
    sudo ldconfig
    ```

    ```shell
    $ export CUDA_VERSION=12.6 # Modify to match to your CUDA version
    $ chmod +x ./install_cusparselt.sh
    $ ./install_cusparselt.sh
    ```

5. Fetch the PyTorch and [TorchVision](../../platforms/quickstart/jetson_orin/assets/torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl){: download="torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl"} wheel files built for the Jetson Orin

    You can either click on the links above or run the following commands.

    ```shell
    $ wget https://nvidia.box.com/shared/static/zvultzsmd4iuheykxy17s4l2n91ylpl8.whl -O torch-2.3.0-cp310-cp310-linux_aarch64.whl
    $ wget https://nvidia.box.com/shared/static/u0ziu01c0kyji4zz3gxam79181nebylf.whl -O torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl
    ```

    Create the environment variables, but modify the path to point to the wheels in your system.

    ```shell
    $ export TORCH_INSTALL=/path/to/torch-2.3.0-cp310-cp310-linux_aarch64.whl
    $ export TORCHVISION_INSTALL=/path/to/torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl
    ```

6. Install PyTorch and TorchVision wheels

    ```shell
    $ python3 -m pip install --upgrade pip; python3 -m pip install numpy=='1.26.1'; python3 -m pip install --no-cache $TORCH_INSTALL $TORCHVISION_INSTALL
    ```

7. Verify PyTorch is installed with CUDA enabled

    ```shell
    $ python
    >>> import torch
    >>> print(torch.__version__)
    2.3.0
    >>> print(torch.version.cuda)
    12.4
    >>> print(torch.cuda.is_available())
    True
    ```

### Run Ultralytics Validation

1. To run Ultralytics validation, download and SCP into your device the [TensorRT YOLOv8s Model](../../platforms/quickstart/jetson_orin/assets/yolov8s-seg-fp16.engine){: download="yolov8s-seg-fp16.engine"} and the coco128-seg.yaml

    ```shell
    $ wget https://raw.githubusercontent.com/ultralytics/ultralytics/refs/heads/main/ultralytics/cfg/datasets/coco128-seg.yaml
    ```

2. Next download and SCP the [val.py](../../platforms/quickstart/jetson_orin/assets/val.py){: download="val.py"} script which utilizes the Ultralytics framework.  

    The contents of the file is shown below.  You can also copy and paste the contents and create this file in your Jetson Orin.

    ```sh
    from ultralytics import YOLO
    import numpy as np

    # Load a model
    model = YOLO("yolov8s-seg-fp16.engine")

    # Validate the model
    metrics = model.val(data="coco128-seg.yaml")

    print(f"{metrics.box.map50=}")
    print(f"{metrics.box.map=}")
    print(f"{metrics.box.mp=}")
    print(f"{metrics.box.mr=}")
    print(f"{np.mean(metrics.box.f1)=}")
    print("=============================")
    print(f"{metrics.seg.map50=}")
    print(f"{metrics.seg.map=}")
    print(f"{metrics.seg.mp=}")
    print(f"{metrics.seg.mr=}")
    print(f"{np.mean(metrics.seg.f1)=}")
    ```

    Ensure that you change the path to the model `YOLO("/path/to/mymodel")` and the path to `data="/path/to/mydataset"` specific in your system.

3. Run the validation script `python val.py`

    You see the following outputs from the script.

    ```shell
    Ultralytics 8.4.41 🚀 Python-3.10.12 torch-2.3.0 CUDA:0 (Orin, 7620MiB)
    Loading yolov8s-seg-fp16.engine for TensorRT inference...
    [04/24/2026-14:36:57] [TRT] [I] Loaded engine size: 25 MiB
    [04/24/2026-14:36:57] [TRT] [I] [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +21, now: CPU 0, GPU 43 (MiB)
    ...
    .
    .
    Class     Images  Instances      Box(P          R      mAP50  mAP50-95)     Mask(P          R      mAP50  mAP50-95): 1
    ...
    .
    .
    all        128        929      0.738      0.684      0.751      0.581      0.725      0.671      0.714      0.473
    ...
    .
    .
    Speed: 3.5ms preprocess, 24.2ms inference, 0.0ms loss, 14.2ms postprocess per image
    Results saved to runs/segment/val-15
    metrics.box.map50=0.7513853053824255
    metrics.box.map=0.5809804783662014
    metrics.box.mp=0.7376484261462859
    metrics.box.mr=0.6842731600893526
    np.mean(metrics.box.f1)=0.6596868913567399
    =============================
    metrics.seg.map50=0.713661683646676
    metrics.seg.map=0.473296910773104
    metrics.seg.mp=0.7249905687994127
    metrics.seg.mr=0.6713176684327864
    np.mean(metrics.seg.f1)=0.6476963946045288
    ```

## EdgeFirst Validation

1. Install edgefirst-validator `pip install edgefirst-validator`
2. Download and SCP into your device the [TensorRT YOLOv8s Model](../../platforms/quickstart/jetson_orin/assets/yolov8s-seg-fp16.engine){: download="yolov8s-seg-fp16.engine"} and the coco128-seg.yaml

    ```shell
    $ wget https://raw.githubusercontent.com/ultralytics/ultralytics/refs/heads/main/ultralytics/cfg/datasets/coco128-seg.yaml
    ```

3. Run validation `edgefirst-validator yolov8s-seg-fp16.engine coco128-seg.yaml`

    You should see the following output.

    ```shell
        +--------------------------------------------------+
        | Model: yolov8s-seg-fp16.engine                   |
        | Dataset: .                                       |
        +--------------------------------------------------+
        |                DETECTION METRICS                 |
        +--------------------------------------------------+
        | Ground Truths: 929                               |
        | Predictions: 12334                               |
        +---------------+-------------------+--------------+
        |               | Mean Precision    |    71.49     |
        |               | mAP@0.5           |    73.01     |
        | Precision (%) | mAP@0.75          |    58.94     |
        |               | mAP@0.5-0.95      |    56.24     |
        +---------------+-------------------+--------------+
        | Recall (%)    | Mean Recall       |    67.16     |
        +---------------+-------------------+--------------+
        | F1 Score (%)  | Mean F1           |    64.46     |
        +---------------+-------------------+--------------+
        |           INSTANCE SEGMENTATION METRICS          |
        +--------------------------------------------------+
        |               | Mean Precision    |    71.18     |
        |               | mAP@0.5           |    69.91     |
        | Precision (%) | mAP@0.75          |    51.46     |
        |               | mAP@0.5-0.95      |    46.74     |
        +---------------+-------------------+--------------+
        | Recall (%)    | Mean Recall       |    65.97     |
        +---------------+-------------------+--------------+
        | F1 Score (%)  | Mean F1           |    63.72     |
        +---------------+-------------------+--------------+
        | Mask IoU (%)  | Mean IoU          |    77.05     |
        +---------------+-------------------+--------------+
    +----------------------------------------------------------+
    | Input Time (ms) | Inference Time (ms) | Output Time (ms) |
    +-----------------+---------------------+------------------+
    | Min: 7.03       | Min: 24.4           | Min: 8.22        |
    | Max: 12.65      | Max: 25.82          | Max: 539.86      |
    | Avg: 9.0        | Avg: 24.48          | Avg: 176.19      |
    +-----------------+---------------------+------------------+
        +--------------------------------------------------+
        |                  SET PARAMETERS                  |
        +--------------------------------------------------+
        | engine: gpu                                      |
        | warmup: 5                                        |
        | backend: opencv                                  |
        | preprocessing: letterbox                         |
        | normalization: unsigned                          |
        | NMS: torch                                       |
        | NMS max detections: 300                          |
        | NMS IoU threshold: 0.7                           |
        | NMS score threshold: 0.001                       |
        | metric: iou                                      |
        | include background: False                        |
        +--------------------------------------------------+
        |           FOUND OPTIMAL NMS THRESHOLDS           |
        +--------------------------------------------------+
        | IoU threshold: 0.261                             |
        | score threshold: 0.233                           |
        +--------------------------------------------------+
        +--------------------------------------------------+
        |     DEPLOYMENT METRICS @ OPTIMAL THRESHOLDS      |
        +---------------+----------------+-----------------+
        | Ground Truths | True Positives | False Negatives |
        +---------------+----------------+-----------------+
        |      929      |      591       |       323       |
        +-------------------------+------------------------+
        |    Classification FP    |    Localization FP     |
        +-------------------------+------------------------+
        |            15           |          194           |
        +-------------------------+------------------------+
        |    Overall Accuracy     |         52.63          |
        |    Mean Class Accuracy  |         53.52          |
        +-------------------------+------------------------+
        |    Overall Precision    |         73.88          |
        |    Mean Class Precision |         70.44          |
        +-------------------------+------------------------+
        |    Overall Recall       |         63.62          |
        |    Mean Class Recall    |         65.96          |
        +-------------------------+------------------------+
    ```

For an in-depth tutorial on running `edgefirst-validator` on target see [On Target Validation](../../models/validation/vision/user_managed.md).

Once you have validated your model and found that the performance is ready for deployment, you can proceed towards deploying your model on target.
