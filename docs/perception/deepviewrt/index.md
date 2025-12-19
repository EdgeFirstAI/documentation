# Deep View RT

Deep View RT has two components currently and is being expanded further for each step of the deployment pipeline. We have the Deep View RT Edge-Optimized Inference Engine that is capable of inference and can be built into applications or workflows using converted models. The Deep View RT Edge-Optimized Inference Engine is capable of running inference on many different devices and EdgeFirst Platforms in addition to running inference on the CPU, GPU, and NPU. We then have the Deep View Converter to handle conversion and optimization of models to our propietary model format. These models have been optimized for our EdgeFirst Platforms and in a wide range of scenarios will provide an increase in inference.

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
pip install deepview-converter
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

### Workflows

In this section I am going to go through the quantization workflows along with API usage for the Deep View Converter. All examples will build off of the basics covered previously. Quantization is supported through the Deep View Converter as well for both frameworks, but as they continue to change and evolve, the process that is used within the converter may no longer be the most optimal method and eventually cause issues, so instead we recommend to use the tools provided by ONNX and TensorFlow and use the Deep View Converter only for that final step to generate the RTM file.

#### Quantization

When looking to quantize an ONNX model, please refer to this [documentation](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html).

When looking to quantize a TensorFlow model, please refer to this [documentation](https://www.tensorflow.org/model_optimization/guide/quantization/post_training).

The first step will be to quantize the model following whichever documentation is appropriate to an 8-bit representation. Currently, the Deep View Converter has support for float32, int8, and uint8 models. If you are looking to use a different format, please contact us.

You can additionally quantize the model through the Deep View Converter using the following CLI commands

``` shell
rtm-converter --quantize --quant_normalization signed --samples samples_folder --num_samples 30 model.h5 model_quant.rtm
rtm-converter --quantize --quant_normalization signed --samples samples_folder --num_samples 30 model.onnx model_quant.rtm
```

!!! warning "ONNX Quantization"
    It is especially recommended to use the provided tools over the Deep View Converter for generating a quantized ONNX model

The --quantize argument is responsible for flagging that you wish to quantize the model.
The --quant_normalization argument is used for specifying what normalization is used for the input.
The --samples argument is where you specify what folder contains the sample inputs to be used for quantization
The --num_samples argument is as expected and lets you specify how many samples to use for quantization, by default this is 10.

Now at this point, you will have your quantized model that can be used with the general workflow described above with no additional arguments necessary. There are some arguments which apply only to quantized models, please refer to the help command for further information on those arguments.

#### API

For the use of the API in this example, I will assume that the model you have generated needs no further adjustments other than to be converted to the RTM format.

Sample Code

``` python
from deepview_rtm.optimizer import DeepViewOptimizer
from deepview_rtm.exporter_v1 import DeepViewExporter

optimizer = DeepViewOptimizer(model_file)
exporter = DeepViewExporter(optimizer, "model name")                                        
buffer = exporter.run()

with open(outfile, 'wb') as f:
    f.write(buffer)
```

As with all of the options available from the command line, they are also available as further arguments for the DeepViewOptimizer and DeepViewExporter. Please refer to further documentation for all of the available arguments to both classes.

This code can be combined with any code developed to quantize your model through ONNX or TensorFlow as a final step to generate the RTM in one step when using the API.

The first step is the optimization step which takes as an argument the filename of your model. The Optimizer will first decode your model into a generic graph format which then runs through a variety of optimizations that combines various operations and removes time ineffective operations for better optimized operations.

After that step, you use the Exporter, which takes that graph from the Optimizer to encode the newly optimized graph into the RTM format which can be run using the Deep View RT Edge-Optimized Inference Engine, which we will cover next.

Finally, you will save the output FlatBuffer, which is used for the RTM format, to whichever file you desire.

## Deep View RT Edge-Optimized Inference Engine

The Deep View RT Edge-Optimized Inference Engine is a C based library that provides easy to use tools for developing applications with your model that are optimized for the EdgeFirst Platforms. The main component of the Deep View RT Inference Engine is the engine itself and there are many optimizations that are performed to benefit the inference and overall pipeline time. The Deep View RT Inference Engine makes use of various plugins that allow for accelerated inference on whichever processor is specified, whether it is using OpenCL for float models on the GPU or OpenVX for quantized models on the GPU or NPU.

With the API provided you can build native C applications that take advantage of the Deep View RT Inference Engine, and additionally we provide Python bindings for the engine that can installed through pip with the following

``` shell
pip install deepview-rt
```

Documentation for using the APIs for both C and Python are currently being updated and will be provided alongside a new update that will look to simplify the application building process.
