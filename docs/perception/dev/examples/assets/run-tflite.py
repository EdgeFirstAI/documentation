#!/usr/bin/env python3

# This is a modified script from https://github.com/apivovarov/ssd-tflite/blob/master/run-tflite.py

from tflite_runtime.interpreter import Interpreter, load_delegate 
import time
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# import tensorflow as tf 
# Interpreter = tf.lite.Interpreter
# load_delegate = tf.lite.experimental.load_delegate

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

def get_mobilenet_input(image_path, out_size=(300, 300), is_quant=True):
    img = np.array(Image.open(image_path).resize(out_size))
    if not(is_quant):
        img = img.astype(np.float32) / 128 - 1
    return np.array([img]) 


def print_output(res, score_threshold=0.50):
    boxes, classes, scores, num_det = res
    
    print("Found objects:")
    for j in range(int(num_det)):
        cl_id = int(classes[j]) + 1
        label = image_classes[cl_id]
        score = scores[j]
        if score < score_threshold:
            continue
        box = boxes[j]
        print("  ", cl_id, label, score, box)


def draw_output(res, image_path, save_path, score_threshold=0.50):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    boxes, classes, scores, num_det = res
    for j in range(int(num_det)):
        cl_id = int(classes[j]) + 1
        label = image_classes[cl_id]
        score = scores[j]
        if score < score_threshold:
            continue
        box = boxes[j]

        text = f"{label}, {score}"
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

    model_path = "ssd_mobilenet_v1_0.75_depth_quantized_300x300_coco14_sync_2018_07_18.tflite"
    image_path = "dog.jpg"
    save_path = "img_vis.jpg"
    delegate = "/usr/lib/libvx_delegate.so"

    is_quant = "quant" in model_path.lower()

    if os.path.exists(delegate):
        ext_delegate = load_delegate(delegate, {})
        ip = Interpreter(model_path=model_path, experimental_delegates=[ext_delegate])
    else:
        ip = Interpreter(model_path=model_path)

    ip.allocate_tensors()
    ip.invoke() # Model warmup

    inp_id = ip.get_input_details()[0]["index"]
    out_det = ip.get_output_details()
    out_id0 = out_det[0]["index"]
    out_id1 = out_det[1]["index"]
    out_id2 = out_det[2]["index"]
    out_id3 = out_det[3]["index"]

    img = get_mobilenet_input(image_path, is_quant=is_quant)
    
    t0 = ms()
    ip.set_tensor(inp_id, img)
    ip.invoke()
    tt = ms() - t0
    print("Time:", tt, "ms")
    boxes = ip.get_tensor(out_id0).squeeze()
    classes = ip.get_tensor(out_id1).squeeze()
    scores = ip.get_tensor(out_id2).squeeze()
    num_det = ip.get_tensor(out_id3).squeeze()
    print_output([boxes, classes, scores, num_det])
    draw_output([boxes, classes, scores, num_det], image_path, save_path)
