#!/usr/bin/env python3

import onnxruntime as ort
import time
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont


image_classes = {
    1: 'person',
    2: 'bicycle',
    3: 'car',
    4: 'motorcycle',
    5: 'airplane',
    6: 'bus',
    7: 'train',
    8: 'truck',
    9: 'boat',
    10: 'traffic light',
    11: 'fire hydrant',
    13: 'stop sign',
    14: 'parking meter',
    15: 'bench',
    16: 'bird',
    17: 'cat',
    18: 'dog',
    19: 'horse',
    20: 'sheep',
    21: 'cow',
    22: 'elephant',
    23: 'bear',
    24: 'zebra',
    25: 'giraffe',
    27: 'backpack',
    28: 'umbrella',
    31: 'handbag',
    32: 'tie',
    33: 'suitcase',
    34: 'frisbee',
    35: 'skis',
    36: 'snowboard',
    37: 'sports ball',
    38: 'kite',
    39: 'baseball bat',
    40: 'baseball glove',
    41: 'skateboard',
    42: 'surfboard',
    43: 'tennis racket',
    44: 'bottle',
    46: 'wine glass',
    47: 'cup',
    48: 'fork',
    49: 'knife',
    50: 'spoon',
    51: 'bowl',
    52: 'banana',
    53: 'apple',
    54: 'sandwich',
    55: 'orange',
    56: 'broccoli',
    57: 'carrot',
    58: 'hot dog',
    59: 'pizza',
    60: 'donut',
    61: 'cake',
    62: 'chair',
    63: 'couch',
    64: 'potted plant',
    65: 'bed',
    67: 'dining table',
    70: 'toilet',
    72: 'tv',
    73: 'laptop',
    74: 'mouse',
    75: 'remote',
    76: 'keyboard',
    77: 'cell phone',
    78: 'microwave',
    79: 'oven',
    80: 'toaster',
    81: 'sink',
    82: 'refrigerator',
    84: 'book',
    85: 'clock',
    86: 'vase',
    87: 'scissors',
    88: 'teddy bear',
    89: 'hair drier',
    90: 'toothbrush'
}


def print_output(res):
    boxes, classes, scores = res
    
    print("Found objects:")
    for j in range(len(boxes)):
        cl_id = int(classes[j]) 
        label = image_classes[cl_id]
        score = scores[j]
        box = boxes[j]
        print("  ", cl_id, label, score, box)


def draw_output(res, image_path, save_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    boxes, classes, scores = res
    for j in range(len(boxes)):
        cl_id = int(classes[j]) 
        label = image_classes[cl_id]
        score = scores[j]
        box = boxes[j]

        text = f"{label}, {score * 100:.2f}%"
        _, _, text_width, text_height = font.getbbox(text)

        xmin, ymin = (int(box[1] * image.width), int(box[0] * image.height))
        xmax, ymax = (int(box[3] * image.width), int(box[2] * image.height))
        draw.rectangle(((xmin, ymin), (xmax, ymax)),
                        outline="RoyalBlue",
                        width=3)
        draw.rectangle(((xmin, ymin), (xmin + text_width, ymin + text_height)),
                       fill="RoyalBlue")
        draw.text((xmin, ymin), text, font=font, align="left", fill="White")
    image.save(save_path)


if __name__ == '__main__':

    ms = lambda: int(round(time.time() * 1000))

    model_path = "ssd_mobilenet_v1_12-int8.onnx"
    image_path = "000000000064.jpg"
    save_path = "img_vis.jpg"
    score_threshold = 0.1
    
    session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

    input_name = session.get_inputs()[0].name
    input_shape = session.get_inputs()[0].shape
    dtype = session.get_inputs()[0].type
    input_dtype = np.uint8 if "uint8" in dtype else np.float32
    height, width = 640, 640

    image = Image.open(image_path)
    img = np.array(image.resize((width, height)))
    img = np.expand_dims(img, axis=0).astype(input_dtype)

    t0 = ms()
    outputs = session.run(None, {input_name: img})
    tt = ms() - t0
    print("Time:", tt, "ms")

    boxes, classes, scores, _ = outputs
    boxes = boxes.squeeze()
    classes = classes.squeeze()
    scores = scores.squeeze()
    
    mask = scores >= score_threshold
    boxes = boxes[mask]
    classes = classes[mask]
    scores = scores[mask]
    
    print_output([boxes, classes, scores])
    draw_output([boxes, classes, scores], image_path, save_path)
