## Copy Dataset

{% include-markdown "discrete/datasets/copy_dataset.md" %}

## Tag Dataset

{% include-markdown "discrete/datasets/tag_dataset.md" %}

{% include-markdown "discrete/models/train_vision.md" %}

## Convert Model for NPU

Once the model is trained in EdgeFirst Studio, you will find `<model_name>_saved_model.zip` and `<model_name>.onnx` artifacts.

{{ figure("/models/assets/training/vision-session-artifacts.jpg", "Model Artifacts") }}

The i.MX 8M Plus supports two NPU backends depending on your board variant.  Select the tab that matches your hardware:

=== "Standard i.MX 8M Plus"

    The standard i.MX 8M Plus uses the built-in 2 TOPS AI accelerator via the OpenVX delegate.  Convert your model to quantized TFLite to leverage it.  The following outlines the basic steps required to convert a model to quantized TFLite format.  For detailed information about the conversion process and available configuration options, refer to the [TFLite Converter](../../models/conversion/tflite.md).

    {% include-markdown "discrete/models/convert_to_tflite.md" heading-offset=2 %}

=== "i.MX 8M Plus + Ara240 DNPU"

    The [NXP Ara240 DNPU](https://www.nxp.com/products/ARA240) is available on the i.MX 8M Plus freedom board and offers higher NPU throughput.  Convert your model to DVM format to leverage it.  The following outlines the basic steps required to convert a model to quantized Kinara ARA2 format.  For detailed information about the conversion process and available configuration options, refer to the [Ara2 Converter](../../models/conversion/ara2.md).

    {% include-markdown "discrete/models/convert_to_ara2.md" heading-offset=2 %}

{% include-markdown "discrete/models/validate_vision_ontarget.md" %}

## Deploy Model on i.MX 8M Plus

{% include-markdown "discrete/models/deploy_on_target.md" heading-offset=2 %}
