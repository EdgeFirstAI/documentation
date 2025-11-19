"""
This script is an example for running TFLite models for inference in a PC. 

Run the script using `python run-tflite.py path/to/model.tflite path/to/*.jpg`
"""

import os
import time
import argparse

import numpy as np
import tensorflow as tf 
from PIL import Image, ImageDraw, ImageFont

Interpreter = tf.lite.Interpreter
load_delegate = tf.lite.experimental.load_delegate


class Colors:
    def __init__(self):
        hexs = (
            "042AFF",  # strong blue
            "FF444F",  # strong red
            "00DFB7",  # teal
            "BD00FF",  # purple
            "A2FF0B",  # lime
            "FC6D2F",  # orange
            "FF6FDD",  # pink
            "00B4FF",  # cyan
            "111F68",  # navy
            "26C000",  # bright green
            "DD00BA",  # magenta
            "01FFB3",  # aqua green
            "7D24FF",  # violet
            "FF1B6C",  # pink-red
            "7B0068",  # deep purple
            "0BDBEB",  # light teal
            "00FFFF",  # light cyan
            "F3F3F3",  # *gray moved to near end*
        )
        self.palette = [self.hex2rgb(f"#{c}") for c in hexs]
        self.n = len(self.palette)
        self.pose_palette = np.array(
            [
                [255, 128, 0],
                [255, 153, 51],
                [255, 178, 102],
                [230, 230, 0],
                [255, 153, 255],
                [153, 204, 255],
                [255, 102, 255],
                [255, 51, 255],
                [102, 178, 255],
                [51, 153, 255],
                [255, 153, 153],
                [255, 102, 102],
                [255, 51, 51],
                [153, 255, 153],
                [102, 255, 102],
                [51, 255, 51],
                [0, 255, 0],
                [0, 0, 255],
                [255, 0, 0],
                [255, 255, 255],
            ],
            dtype=np.uint8,
        )

    def __call__(self, i: int, bgr: bool = False) -> tuple:
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h: str) -> tuple:
        return tuple(int(h[1 + i: 1 + i + 2], 16) for i in (0, 2, 4))

COLORS = Colors()


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


def print_output(res: list, labels: list):
    boxes, classes, scores = res
    
    for j in range(len(boxes)):
        cl_id = int(classes[j]) 
        label = labels[cl_id]
        label = "label"
        score = scores[j]
        box = boxes[j]
        print("  ", cl_id, label, score, box)


def mask_image(image: Image.Image, mask: np.ndarray):

    # Transform dimension of masks from a 2D numpy array to 4D into RGBA.
    if len(mask.shape) > 2:
        _, height, width = mask.shape
    else:
        height, width = mask.shape
    mask_4_channels = np.zeros((height, width, 4), dtype=np.uint8)

    labels = np.sort(np.unique(mask))
    for label in labels:
        if label != 0:
            # Designate a color for each class.
            mask_4_channels[mask == label] = \
                np.append(COLORS(label), 130)

    # Convert array to image object for image processing.
    mask = Image.fromarray(mask_4_channels.astype(np.uint8))

    image = image.convert("RGBA")
    image = Image.alpha_composite(image, mask).convert("RGB")
    return image


def draw_output(res: list, labels: list, image_path: str, save_path: str):
    image = Image.open(image_path)
    font = ImageFont.load_default()

    boxes, classes, scores, masks = res
    image = mask_image(image, masks)
    draw = ImageDraw.Draw(image)

    for j in range(len(boxes)):
        cl_id = int(classes[j])
        label = labels[cl_id]
        score = scores[j]
        box = boxes[j]

        text = f"{label}, {score * 100:.2f}%"
        _, _, text_width, text_height = font.getbbox(text)

        xmin, ymin = (int(box[0] * image.width), int(box[1] * image.height))
        xmax, ymax = (int(box[2] * image.width), int(box[3] * image.height))
        draw.rectangle(((xmin, ymin), (xmax, ymax)),
                       outline=COLORS(cl_id),
                       width=3)
        draw.rectangle(((xmin, ymin), (xmin + text_width, ymin + text_height)),
                       fill=COLORS(cl_id))
        draw.text((xmin, ymin), text, font=font, align="left", fill="White")

    image.save(save_path)

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("model", type=str, help="path/to/model.tflite")
    ap.add_argument("images", type=str, help="path/to/*.jpg", nargs='+')
    ap.add_argument("--labels", type=str, help="Provide a list of labels", nargs='+', default=["coffeecup"])
    ap.add_argument("--score", type=float, default=0.25)
    ap.add_argument("--iou", type=float, default=0.70)
    ap.add_argument("--save", type=str, default="results")
    ap.add_argument("--delegate", type=str, default="/usr/lib/libvx_delegate.so")
    args = ap.parse_args()

    ms = lambda: int(round(time.time() * 1000))
    inference_times = []
    os.makedirs(args.save, exist_ok=True)

    if os.path.exists(args.delegate):
        ext_delegate = load_delegate(args.delegate, {})
        ip = Interpreter(model_path=args.model, experimental_delegates=[ext_delegate])
    else:
        ip = Interpreter(model_path=args.model)

    ip.allocate_tensors()
    ip.invoke() # Model warmup

    input_det = ip.get_input_details()
    inp_id = input_det[0]["index"]
    out_det = ip.get_output_details()

    # Multitask model
    if len(out_det) > 2: 
        labels = ["background"] + args.labels
    else:
        labels = args.labels
    nc = len(labels)  # number of classes

    for image_path in args.images:
        # Preprocess Inputs
        image, size = get_input(image_path, input_det[0])

        # Run Model Inference
        t0 = ms()
        ip.set_tensor(inp_id, image)
        ip.invoke()
        tt = ms() - t0
        inference_times.append(tt)

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
            if len(shape) == 4 and shape[-1] == 4 and shape[-2] == 1:
                box_id = i
            elif len(shape) == 3:
                if shape[-1] == nc:
                    score_id = i
                else:
                    mask_id = i

        boxes = outputs[box_id][0]  # shape (n, 4)
        scores = outputs[score_id][0]  # shape (n, num_classes)
        masks = None
        if mask_id is not None:
            masks = outputs[mask_id][0]  # shape (h, w)
        
        boxes = np.reshape(boxes, (-1, 4))
        scores = np.reshape(scores, (boxes.shape[0], -1))
        classes = np.argmax(scores, axis=1).astype(np.int32)

        # Prefilter boxes and scores by minimum score
        max_scores = np.max(scores, axis=1)
        filt = max_scores >= args.score

        # Prefilter the boxes, scores and classes IDs.
        scores = max_scores[filt]
        boxes = boxes[filt]
        classes = classes[filt]

        keep = numpy_nms(boxes, scores, iou_threshold=args.iou)
        boxes = boxes[keep]
        classes = classes[keep]
        scores = scores[keep]

        if masks is not None:
            masks = resize_mask(masks, size)

        print("Objects found in image: ", os.path.basename(image_path))
        print_output([boxes, classes, scores], labels=labels)
        draw_output([boxes, classes, scores, masks], labels=labels, image_path=image_path, 
                    save_path=os.path.join(args.save, os.path.basename(image_path)))
        
    if len(inference_times):
        avg_inference_time = sum(inference_times) / len(inference_times)
        print(f"Average Inference Time: {avg_inference_time:.2f} ms")
        