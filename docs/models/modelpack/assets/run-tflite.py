#!/usr/bin/env python3

from tflite_runtime.interpreter import Interpreter, load_delegate # type: ignore

import time
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

image_classes = [
    "background",
    "coffeecup"
]


def get_input(image_path: str, input_details: dict) -> np.ndarray:
    _, height, width, _ = input_details.get("shape")
    image = Image.open(image_path)
    size = (image.height, image.width)
    img = np.array(image.resize((width, height)))

    # is TFLite quantized int8 model
    int8 = input_details["dtype"] == np.int8
    _, zp = input_details["quantization"]
    if int8:
        zp = abs(zp)
        img = (img.astype(np.int16) - zp).astype(np.int8)
    return np.array([img]), size


def numpy_nms(
    boxes: np.ndarray,
    scores: np.ndarray,
    iou_threshold: float = 0.70,
    max_detections: int = 300,
    eps: float = 1e-7
) -> np.ndarray:
    if len(boxes) == 0:
        return np.array([], dtype=np.int32)

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Calculate areas (remove the +1 for normalized coordinates)
    areas = (x2 - x1) * (y2 - y1)

    # Sort by scores in descending order
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        if len(keep) >= max_detections:
            break

        # Calculate intersection coordinates
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        # Calculate intersection area (remove +1 for normalized coords)
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h

        # Calculate IoU
        union = areas[i] + areas[order[1:]] - inter
        iou = inter / (union + eps)

        # Keep boxes with IoU less than threshold
        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]

    return np.array(keep, dtype=np.int32)


def resize_mask(mask: np.ndarray, size: tuple) -> np.ndarray:
    return np.array(Image.fromarray(mask).resize((size[1], size[0]), 
                                                 resample=Image.NEAREST))


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
    image = mask_image(image, masks)
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

    model_path = "coffeecup-modelpack-multitask-t-1f54.tflite"
    image_path = "IMG_9004.png"
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

    box_id, score_id, mask_id = None, None, None
    outputs = []
    for i, out in enumerate(out_det):
        x = ip.get_tensor(out["index"])

        # Output Dequantization
        scale, zero_point = out["quantization"]
        if x.dtype != np.float32 and scale > 0:
            x = (x.astype(np.float32) - zero_point) * scale  # re-scale
        outputs.append(x)

        shape = out.get("shape")
        if len(shape) == 4 and shape[-1] == 4:
            box_id = i
        elif len(shape) == 3:
            if shape[-1] == nc:
                score_id = i
            else:
                mask_id = i

    boxes = outputs[box_id][0]  # shape (n, 4)
    scores = outputs[score_id][0]  # shape (n, num_classes)
    masks = outputs[mask_id][0]  # shape (h, w)
    
    boxes = np.reshape(boxes, (-1, 4))
    scores = np.reshape(scores, (boxes.shape[0], -1))
    classes = np.argmax(scores, axis=1).astype(np.int32)

    # Prefilter boxes and scores by minimum score
    max_scores = np.max(scores, axis=1)
    filt = max_scores >= score_threshold

    # Prefilter the boxes, scores and classes IDs.
    scores = max_scores[filt]
    boxes = boxes[filt]
    classes = classes[filt]

    keep = numpy_nms(boxes, scores, iou_threshold=iou_threshold)
    boxes = boxes[keep]
    classes = classes[keep]
    scores = scores[keep]
    masks = resize_mask(masks, size)

    print_output([boxes, classes, scores])
    draw_output([boxes, classes, scores, masks], image_path, save_path)
