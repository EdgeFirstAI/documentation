# Deep View RT Middleware
The Deep View Middleware toolset includes a wide variety of tools that can be used for each step of the deployment pipeline. We have the Deep View Converter to handle conversion and optimization of models to our propietary model format. These models have been optimized for our EdgeFirst Platforms and in a wide range of scenarios will provide an increase in inference.

We have our backend engine in Deep View RT that is capable of inference and can be built into applications or workflows using the models converted. The Deep View RT engine is capable of running inference on many different devices and EdgeFirst Platforms in addition to running inference on the CPU, GPU, and NPU.

Finally, in development is our HAL (Hardware Abstraction Library), which will simplify the deployment pipeline and allow for minimally coded application pipelines to be highly optimized on whichever EdgeFirst Platform you are using for inference.

## Deep View Converter
The Deep View Converter is a tool for taking a pretrained model from a framework, such as any from TensorFlow or ONNX, and converting this model to our proprietary format RTM. During this process, there are many optimizations that are performed on the layers within the model, folding layers to reduce model complexity, modifying operations to ones that are more efficient on EdgeFirst Platforms, overall improving the inference time of the models. These models are fully functional with our tools within our Middleware Suite and are ready to be deployed for any project.

Previously, the converter was capable of handling conversion between the various formats, converting ONNX to TFLite and vice versa, but due to the rate of change of these libraries and the improvement in conversion tools between these main frameworks, the Deep View Converter going forward will focus solely on conversion to RTM, dropping the plugin system that was being used for conversion between these alternate frameworks.

Additionally, due to the the improvements in quantization capabilities of each framework, we do recommend using their tools for quantization. Support does exist within the converter for quantization currently, but as the tools change and improve at a steady rate, we recommend using the tools listed for quantization for [TensorFlow](https://www.tensorflow.org/model_optimization/guide/quantization/post_training) and [ONNX](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)

### Setup
If you have previously had the Deep View Converter installed, it is highly recommended to run the following to remove the plugin system as you update to this self-contained conversion process.

``` shell
pip uninstall deepview-converter deepview-converter-rtm deepview-converter-tflite deepview-converter-onnx
```

The converter is a Python-based tool and as such can be installed directly through pip using the following
``` shell
pip install rtm-converter
```
Now you are all set up to use the Deep View Converter with any model you are looking to run on your EdgeFirst Platform.

### Usage
The Deep View Converter has a lot of customizations that will be described in the later section, but for basic conversion the command is as simple as the following where you provide the filename of the model to be converted and the filename of where you want the RTM to be saved.

``` shell
rtm-converter input_model.tflite output_model.rtm
```

### Detailed Usage
There are a handful of arguments that you may see in common use and I will describe those ones first, before continuing with the more obscure arguments that have niche usage.

``` shell
rtm-converter --input_names node1,node2,... --output_names outnode1,outnode2,... model_in.tflite model_out.rtm
```
The input and output name arguments allow you to trim the model during conversion if there are sections that are unneeded. A common use is to trim the model before a decoder used for detection, so then those outputs can be taken and sent through our optimized decoders.

``` shell
rtm-converter --input_type int8 --output_type float32 model_in.tflite model_out.rtm
```
The input and output type arguments can be used in a quantized model to modify the datatypes of the inputs and outputs of the model, to remove a potential additional step of quantizing/dequantizing inputs or outputs.

``` shell
rtm-converter --labels labels.txt model_in.onnx model_out.rtm
```
The labels argument can be used to tell the RTM to store the list of labels directly into the file. This can then be accessed through the API to retrieve the labels for use in the pipeline.

``` shell
rtm-converter --metadata file1.bin --metadata file2.bin,entry_name1 --metadata file3.bin,entry_name2,application/octet-stream \
    model_in.onnx model_out.rtm
```
The metadata argument is a repeatable argument that can be used to store any additional information within the RTM. These are stored in the metadata field and can be accessed as seen in this [sample](). When providing a .txt file, it will be stored as plaintext, but otherwise the file provided will be stored as bytes.

These cover the majority of arguments that will be used the most, but there are many others that can be viewed in the help dialog of the tool.

## Deep View RT Engine
The Deep View RT engine is a C based library that provides easy to use tools for developing applications with your model that are optimized for the EdgeFirst Platforms. The main component of the Deep View RT engine is the engine itself and there are many optimizations that are performed to benefit the inference and overall pipeline time. The Deep View RT engine makes use of various plugins that allow for accelerated inference on whichever processor is specified, whether it is using OpenCL for float models on the GPU or OpenVX for quantized models on the GPU or NPU.

With the API provided you can build native C applications that take advantage of the Deep View RT engine, and additionally we provide Python bindings for the engine that can installed through pip with the following

``` shell
pip install deepview-rt
```

Documentation for using the APIs for both C and Python are currently being updated and will be provided alongside a new update that will look to simplify the application building process.
