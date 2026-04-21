# Timing Metrics

For each type of model validation (object detection, segmentation, fusion), the timing metrics are also reported.  These metrics provide an indication of the end-to-end pipeline latency when the model is deployed.  The timing measurements are based on three stages:

1. Input Time: time measured to preprocess the inputs based on the model's requirements.  This can include input normalization, quantization, or transformations such as resizing, letterbox, or padding
2. Inference Time: time measured to run the model for inference per sample
3. Output Time: time measured to postprocess raw predictions.  This can include decoding and NMS

The minimum, maximum, and average timings of each of these stages are represented as a bar chart as shown below.

{{ figure("../../assets/metrics/model-timings.jpg", "Model Timings") }}

Furthermore, the distribution of the average timings are represented as a pie chart.  This chart gives an indication of which stage of the pipeline takes the most time.

{{ figure("../../assets/metrics/timing-distribution.jpg", "Average Timings") }}
