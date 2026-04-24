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
