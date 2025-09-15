#!/usr/bin/env python3

from tflite_runtime.interpreter import Interpreter, load_delegate # type: ignore
import time
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# import tensorflow as tf 
# Interpreter = tf.lite.Interpreter
# load_delegate = tf.lite.experimental.load_delegate

image_classes = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

def get_input(image_path: str, input_details: dict) -> np.ndarray:
    _, height, width, _ = input_details.get("shape")
    image = Image.open(image_path)
    size = (image.height, image.width)
    img = np.array(image.resize((width, height)))

    # is TFLite quantized int8 model
    int8 = input_details["dtype"] == np.int8
    # is TFLite quantized uint8 model
    uint8 = input_details["dtype"] == np.uint8
    if int8 or uint8:
        img = img.astype(np.uint8) if uint8 else img.astype(np.int8)
    else:
        img = img.astype(np.float32)
    return np.array([img]), size

def numpy_nms(dets: np.ndarray, scores: np.ndarray, thresh: float) -> list:
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = scores

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort(kind='mergesort')[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)

        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]
    return keep

def decode_boxes(p: np.ndarray, nc: int) -> tuple:
    p = p.transpose((0, 2, 1))
    boxes = p[0, :, 0:4]
    bboxes = np.concatenate([
                boxes[:, 0:2] - boxes[:, 2:4] / 2,
                boxes[:, 0:2] + boxes[:, 2:4] / 2
            ], axis=1)
    scores = p[0, :, 4:(nc+4)]
    masks = p[0, :, (nc+4):]
    classes = np.argmax(scores, axis=1)
    scores = scores.max(axis=1)
    return bboxes, scores, classes, masks

def crop_mask(masks: np.ndarray, boxes: np.ndarray) -> np.ndarray:
    _, h, w = masks.shape
    x1, y1, x2, y2 = np.split(
        boxes[:, :, np.newaxis], 4, axis=1)  # shape (n, 1, 1)
    r = np.arange(w, dtype=boxes.dtype)[None, None, :]  # rows shape(1,1,w)
    c = np.arange(h, dtype=boxes.dtype)[None, :, None]  # cols shape(1,h,1)
    return masks * ((r >= x1 * w) * (r < x2 * w) * (c >= y1 * h) * (c < y2 * h))

def decode_masks(masks: np.ndarray, protos: np.ndarray) -> np.ndarray:
    h, w, c = protos[0].shape
    protos = np.transpose(protos, (0, 3, 1, 2))
    masks = np.matmul(masks, protos.reshape(c, -1)).reshape(-1, h, w)
    return masks

def resize_mask(masks: np.ndarray, size: tuple) -> np.ndarray:
    mask_resized = [
        np.array(Image.fromarray(mask).resize((size[1], size[0]), resample=Image.NEAREST))
        for mask in masks
    ]
    masks = np.stack(mask_resized, axis=0)
    masks = (masks > 0).astype(np.uint8)
    return masks

def print_output(res: list):
    boxes, classes, scores = res
    
    print("Found objects:")
    for j in range(len(boxes)):
        cl_id = int(classes[j]) 
        label = image_classes[cl_id]
        label = "label"
        score = scores[j]
        box = boxes[j]
        print("  ", cl_id, label, score, box)

def mask_image(image: Image.Image, mask: np.ndarray):
    # Transform dimension of masks from a 2D numpy array to 4D with RGBA
    # channels.
    mask_4_channels = np.stack((mask,) * 4, axis=-1)
    # Assign all classes with color white.
    mask_4_channels[mask_4_channels == 1] = 255
    # Temporarily unpack the bands for readability.
    red, green, blue, _ = mask_4_channels.T
    # Areas of all classes.
    u_areas = (red == 255) & (blue == 255) & (green == 255)
    # Color all classes with blue.
    mask_4_channels[..., :][u_areas.T] = (0, 0, 255, 100)
    # Convert array to image object for image processing.
    mask = Image.fromarray(mask_4_channels.astype(np.uint8))

    image = image.convert("RGBA")
    image = Image.alpha_composite(image, mask).convert("RGB")
    return image

def draw_output(res: list, image_path: str, save_path: str):
    image = Image.open(image_path)
    font = ImageFont.load_default()

    boxes, classes, scores, masks = res

    for mask in masks:
        image = mask_image(image, mask)
    draw = ImageDraw.Draw(image)

    for j in range(len(boxes)):
        cl_id = int(classes[j]) 
        label = image_classes[cl_id]
        score = scores[j]
        box = boxes[j]

        text = f"{label}, {score * 100:.2f}%"
        _, _, text_width, text_height = font.getbbox(text)

        xmin, ymin = (int(box[0] * image.width), int(box[1] * image.height))
        xmax, ymax = (int(box[2] * image.width), int(box[3] * image.height))
        draw.rectangle(((xmin, ymin), (xmax, ymax)),
                        outline="RoyalBlue",
                        width=3)
        draw.rectangle(((xmin, ymin), (xmin + text_width, ymin + text_height)),
                       fill="RoyalBlue")
        draw.text((xmin, ymin), text, font=font, align="left", fill="White")

    image.save(save_path)


if __name__ == '__main__':

    ms = lambda: int(round(time.time() * 1000))

    model_path = "yolo11s-seg.tflite"
    image_path = "000000000064.jpg"
    save_path = "img_vis.jpg"
    delegate = "/usr/lib/libvx_delegate.so"
    score_threshold = 0.25
    iou_threshold = 0.70
    nc = len(image_classes)

    if os.path.exists(delegate):
        ext_delegate = load_delegate(delegate, {})
        ip = Interpreter(model_path=model_path, experimental_delegates=[ext_delegate])
    else:
        ip = Interpreter(model_path=model_path)

    ip.allocate_tensors()
    ip.invoke() # Model warmup

    input_det = ip.get_input_details()
    inp_id = input_det[0]["index"]
    out_det = ip.get_output_details()

    # is TFLite quantized int8 model
    int8 = input_det[0]["dtype"] == np.int8
    # is TFLite quantized uint8 model
    uint8 = input_det[0]["dtype"] == np.uint8

    # Preprocess Inputs
    img, size = get_input(image_path, input_det[0])
    
    # Run Model Inference
    t0 = ms()
    ip.set_tensor(inp_id, img)
    ip.invoke()
    tt = ms() - t0
    print("Time:", tt, "ms")

    # Decode Boxes
    box_id, mask_id = None, None
    outputs = []
    for i, out in enumerate(out_det):
        x = ip.get_tensor(out["index"])
        if (int8 or uint8) and x.dtype != np.float32:
            scale, zero_point = out["quantization"]
            x = (x.astype(np.float32) - zero_point) * scale  # re-scale
        outputs.append(x)

        if len(out.get("shape")) > 3:
            mask_id = i
        else:
            box_id = i
    
    boxes, scores, classes, masks = decode_boxes(outputs[box_id], nc)
    
    # Filter By Score
    scores_masks = scores > score_threshold
    boxes = boxes[scores_masks]
    classes = classes[scores_masks]
    scores = scores[scores_masks]
    masks = masks[scores_masks]

    # Filter By NMS
    keep = numpy_nms(boxes, scores, thresh=iou_threshold)
    boxes = boxes[keep]
    classes = classes[keep]
    scores = scores[keep]
    masks = masks[keep]

    # Decode Masks
    masks = decode_masks(masks, np.array(outputs[mask_id], dtype=np.float32))
    masks = resize_mask(masks, size)
    masks = crop_mask(masks, boxes)

    print_output([boxes, classes, scores])
    draw_output([boxes, classes, scores, masks], image_path, save_path)
