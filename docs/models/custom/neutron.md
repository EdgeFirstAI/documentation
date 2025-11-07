# Neutron Model Conversion

In this section, you will find instructions for converting a quantized TFLite model using NXP's eIQ Neutron Converter to allow deployment of the model in the i.MX 95 EVK platform.

You can follow along these three steps to get you started.

1. Install eIQ Toolkit
2. Run Neutron Converter
3. Deploy the model in the i.MX 95 platform

## Install eIQ Toolkit

Visit the eIQ Toolkit [Downloads page](https://www.nxp.com/design/design-center/software/eiq-ai-development-environment/eiq-toolkit-for-end-to-end-model-development-and-deployment:EIQ-TOOLKIT).  In this example, the Windows installer is selected.  Click "Download" to download the installer in your system.

<figure markdown="span">
![eIQ Toolkit Installer](assets/eIQ-toolkit-installer.jpg){ align=center }
<figcaption>eIQ Toolkit Installer</figcaption>
</figure>

!!! info "NXP Account"

    You will need to be signed in to nxp.com to download the installer.


Once downloaded, click on the executable to start the installation process.

<figure markdown="span">
![eIQ Toolkit Installer](assets/eIQ-toolkit-installer-executable.jpg){ align=center }
<figcaption>eIQ Toolkit Installer</figcaption>
</figure>

Follow the Setup Wizard that pops up and accepts the terms and agreement.  

| Setup Wizard                          | Terms and Agreement                       |
|---------------------------------------|-------------------------------------------|
| ![Start](assets/eIQ-setup-wizard.jpg) | ![terms](assets/eIQ-terms-agreements.jpg) |

Next, specify the folder to store the toolkit.  It's recommended to keep the suggested path.  Keep all settings default and finally click "Install" to start the installation.

| Installation Path                         | Install                            |
|-------------------------------------------|------------------------------------|
| ![path](assets/eIQ-installation-path.jpg) | ![install](assets/eIQ-install.jpg) |

Wait for the installation to finish and once it's done, click "Finish".

| Installation Path                           | Complete                                          |
|---------------------------------------------|---------------------------------------------------|
| ![process](assets/eIQ-installation-process.jpg) | ![complete](assets/eIQ-installation-complete.jpg) |

Once NXP eIQ Toolkit is installed, open a command prompt in your system and verify the installation with the command below.

```shell
>"C:\nxp\eIQ_Toolkit_v1.17.0\eIQ Portal.exe"
```

This should start the eIQ portal.  To exit the application, CTRL-C on the command prompt.

<figure markdown="span">
![eIQ Portal](assets/eIQ-portal.jpg){ align=center }
<figcaption>eIQ Portal</figcaption>
</figure>

## Run Neutron Converter

Prior to running the converter, confirm your target's BSP.  This will be useful in specifying the version of Neutron Converter needed in your system.

```shell
# uname -a
Linux imx95evk 6.12.20-lts-next-gdfaf2136deb2 #1 SMP PREEMPT Wed Jun  4 10:15:09 UTC 2025 aarch64 GNU/Linux
```

Now, check that Neutron Converter is installed in your system with the version that matches your target's BSP (6.12.20).

```shell
>C:\nxp\eIQ_Toolkit_v1.17.0\bin\neutron-converter\MCU_SDK_25.06.00+Linux_6.12.20_2.0.0\neutron-converter.exe --version
eIQ neutron-converter.exe version 2.0.2+0X0cebb80a
```

!!! tip "Help Options"

    You can find the options and descriptions with the command.

    ```
    >C:\nxp\eIQ_Toolkit_v1.17.0\bin\neutron-converter\MCU_SDK_25.06.00+Linux_6.12.20_2.0.0\neutron-converter.exe --help
    ```

Once that the right version of Neutron Converter is available in your system, you can start converting quantized TFLite models to be executable in i.MX 95 platforms with the command below.  You can find instructions for quantizing ONNX to TFLite in the [Model Quantization section](quantize.md).  In this example, the TFLite model `yolov8s-seg_full_integer_quant.tflite` from Ultralytics will be used.

```shell
>C:\nxp\eIQ_Toolkit_v1.17.0\bin\neutron-converter\MCU_SDK_25.06.00+Linux_6.12.20_2.0.0\neutron-converter.exe --input yolov8s-seg_full_integer_quant.tflite --target imx95
Converting model with the following options:
  Input  = yolov8s-seg_full_integer_quant.tflite
  Output = yolov8s-seg_full_integer_quant_converted.tflite
  Target = imx95
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
Starting Tile scheduling. This might take a while.
[================================================================================] 100 %
Starting TCM allocation. This might take a while.
[================================================================================] 100 %
Conversion statistics:
  Number of operators after import    = 293
  Number of operators after optimize  = 338
    Number of operators converted     = 303
    Number of operators NOT converted = 35
  Number of operators after extract   = 36
    Number of Neutron graphs          = 1
    Number of operators NOT converted = 35
  Operator conversion ratio           = 303 / 338 = 0.89645
  Operators converted                 = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,243,244,245,246,247,248,249,250,251,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,275,276,277,278,279,280,281,282,283,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,330,331,332,333,334,335,336,337,
Time for optimization = 0.0457691 (seconds)
Time for extraction   = 0.459354 (seconds)
Time for generation   = 154.223 (seconds)
```

!!! note "Model Input"

    --input takes the path to the TFLite model. 

A new model file will be generated with the suffix "_converted" in the model name.  This converted model will be ready for deployment in the i.MX 95 platform.

## Deploy the model in the i.MX 95 platform

Follow the instructions shown in [Deploying Quantized TFLite](npu.md#deploying-quantized-tflite) for more details.  Otherwise, the steps below show python examples for loading and running the model for inference in the device.  You can download the Python script

You can download our [Python Script](assets/run-tflite-neutron.py){: download="run-tflite.py"} and this sample image [000000000064.jpg](assets/000000000064.jpg){: download="000000000064.jpg" } taken from [COCO128](https://www.kaggle.com/datasets/ultralytics/coco128) for running the example on the target using the command below.

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

1. Load the model specifying the external delegate to use the device's NPU.

    ```python
    model_path = "yolov8s-seg_full_integer_quant_converted.tflite"
    delegate = "/usr/lib/libneutron_delegate.so"

    ext_delegate = load_delegate(delegate, {})
    ip = Interpreter(model_path=model_path, experimental_delegates=[ext_delegate])
    ```

    !!! note "Neutron Delegate"
        The Neutron delegate is specified with `experimental_delegates=[ext_delegate]`. 
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
