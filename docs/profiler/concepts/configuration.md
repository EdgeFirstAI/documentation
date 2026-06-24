# Training Configurations

The [EdgeFirst Model Zoo](https://huggingface.co/spaces/EdgeFirst/Models) includes profiling results for Ultralytics YOLO models across multiple versions, architectures, and model sizes. This page provides instructions for configuring EdgeFirst Studio to reproduce and train YOLO models in various formats.

EdgeFirst Studio training sessions allow you to configure the model version, size, and type. Use the table below as a reference when configuring a training session to reproduce a specific model format.

{{ figure("../assets/studio-yolo-model-configurations.jpg", "Ultralytics Studio Configurations") }}

| Model Name   | Version | Size   | Type         |
|--------------|---------|--------|--------------|
| [yolov5n-det](https://huggingface.co/EdgeFirst/yolov5-det)  | v5      | nano   | detection    |
| [yolov5s-det](https://huggingface.co/EdgeFirst/yolov5-det)  | v5      | small  | detection    |
| [yolov5m-det](https://huggingface.co/EdgeFirst/yolov5-det)  | v5      | medium | detection    |
| [yolov8n-det](https://huggingface.co/EdgeFirst/yolov8-det)  | v8      | nano   | detection    |
| [yolov8s-det](https://huggingface.co/EdgeFirst/yolov8-det)  | v8      | small  | detection    |
| [yolov8m-det](https://huggingface.co/EdgeFirst/yolov8-det)  | v8      | medium | detection    |
| [yolov8n-seg](https://huggingface.co/EdgeFirst/yolov8-seg)  | v8      | nano   | segmentation |
| [yolov8s-seg](https://huggingface.co/EdgeFirst/yolov8-seg)  | v8      | small  | segmentation |
| [yolov8m-seg](https://huggingface.co/EdgeFirst/yolov8-seg)  | v8      | medium | segmentation |
| [yolo11n-det](https://huggingface.co/EdgeFirst/yolo11-det)  | v11     | nano   | detection    |
| [yolo11s-det](https://huggingface.co/EdgeFirst/yolo11-det)  | v11     | small  | detection    |
| [yolo11m-det](https://huggingface.co/EdgeFirst/yolo11-det)  | v11     | medium | detection    |
| [yolo11n-seg](https://huggingface.co/EdgeFirst/yolo11-seg)  | v11     | nano   | segmentation |
| [yolo11s-seg](https://huggingface.co/EdgeFirst/yolo11-seg)  | v11     | small  | segmentation |
| [yolo11m-seg](https://huggingface.co/EdgeFirst/yolo11-seg)  | v11     | medium | segmentation |
| [yolo26n-det](https://huggingface.co/EdgeFirst/yolo26-det)  | v26     | nano   | detection    |
| [yolo26s-det](https://huggingface.co/EdgeFirst/yolo26-det)  | v26     | small  | detection    |
| [yolo26m-det](https://huggingface.co/EdgeFirst/yolo26-det)  | v26     | medium | detection    |
| [yolo26n-seg](https://huggingface.co/EdgeFirst/yolo26-seg)  | v26     | nano   | segmentation |
| [yolo26s-seg](https://huggingface.co/EdgeFirst/yolo26-seg)  | v26     | small  | segmentation |
| [yolo26m-seg](https://huggingface.co/EdgeFirst/yolo26-seg)  | v26     | medium | segmentation |
