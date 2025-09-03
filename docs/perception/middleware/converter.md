# Deep View Converter
The Deep View Converter is a tool for taking a pretrained model from a framework, such as any from TensorFlow or ONNX, and converting this model to our proprietary format RTM. During this process, there are many optimizations that are performed on the layers within the model, folding layers to reduce model complexity, modifying operations to ones that are more efficient on EdgeFirst Platforms, overall improving the inference time of the models. These models are fully functional with our tools within our Middleware Suite and are ready to be deployed for any project.

Previously, the converter was capable of handling conversion between the various formats, converting ONNX to TFLite and vice versa, but due to the rate of change of these libraries and the improvement in conversion tools between these main frameworks, the Deep View Converter going forward will focus solely on conversion to RTM, dropping the plugin system that was being used for conversion between these alternate frameworks.

## Setup
If you have previously had the Deep View Converter installed, it is highly recommended to run the following to remove the plugin system as you update to this self-contained conversion process.

``` shell
pip uninstall deepview-converter deepview-converter-rtm deepview-converter-tflite deepview-converter-onnx
```

The converter is a Python-based tool and as such can be installed directly through pip using the following
``` shell
pip install deepview-converter-rtm
```
Now you are all set up to use the Deep View Converter with any model you are looking to run on your EdgeFirst Platform.

## Usage
The Deep View Converter has a lot of customizations that will be described in the later section, but for basic conversion the command is as simple as the following where you provide the filename of the model to be converted and the filename of where you want the RTM to be saved.

``` shell
deepview-converter input_model.tflite output_model.rtm
```

## Detailed Usage
There are a handful of arguments that you may see in common use and I will describe those ones first, before continuing with the more obscure arguments that have niche usage.

``` shell
deepview-converter --input_names node1,node2,... --output_names outnode1,outnode2,... model_in.tflite model_out.rtm
```
The input and output name arguments allow you to trim the model during conversion if there are sections that are unneeded. A common use is to trim the model before a decoder used for detection, so then those outputs can be taken and sent through our optimized decoders.

``` shell
deepview-converter --input_type int8 --output_type float32 model_in.tflite model_out.rtm
```
The input and output type arguments can be used in a quantized model to modify the datatypes of the inputs and outputs of the model, to remove a potential additional step of quantizing/dequantizing inputs or outputs.

``` shell
deepview-converter --labels labels.txt model_in.onnx model_out.rtm
```
The labels argument can be used to tell the RTM to store the list of labels directly into the file. This can then be accessed through the API to retrieve the labels for use in the pipeline.

``` shell
deepview-converter --metadata file1.bin --metadata file2.bin,entry_name1 --metadata file3.bin,entry_name2,application/octet-stream \
    model_in.onnx model_out.rtm
```
The metadata argument is a repeatable argument that can be used to store any additional information within the RTM. These are stored in the metadata field and can be accessed as seen in this [sample](). When providing a .txt file, it will be stored as plaintext, but otherwise the file provided will be stored as bytes.

These cover the majority of arguments that will be used the most, but there are many others that I will go through now.