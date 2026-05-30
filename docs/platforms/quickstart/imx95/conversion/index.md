# Model Conversions

Now that you have trained your Vision model, we recommend quantizing your model to leverage the platform's NPU and optimize model performance. 

If you have an i.MX 95 freedom board with [Ara240 DNPU](https://www.nxp.com/products/ARA240), we recommend converting the model to [Kinara ARA-2 DVM format](convert_kinara.md) for optimized performance leveraging the ARA240 DNPU chip integrated on the system.

Otherwise, we recommend converting the model to a [Quantized TFLite](convert_neutron.md) to leverage the i.MX 95 Neutron Delegate.
