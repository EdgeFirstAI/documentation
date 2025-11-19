"""
This script is an example for running ONNX models for inference in a PC. 

Run the script using `python run-onnx.py path/to/model.onnx path/to/*.jpg`
"""

import os
import time
import argparse

import numpy as np
import onnxruntime
from PIL import Image, ImageDraw, ImageFont


def get_input(image_path: str, inputs: list) -> np.ndarray:
    shape = inputs[0].shape
    _, _, height, width = shape

    image = Image.open(image_path)
    size = (image.height, image.width)
    img = np.array(image.resize((width, height)), dtype=np.float32)
    img /= 255.0  # Float models requires unsigned normalization.
    img = np.transpose(img, (2, 0, 1))  # HWC to CHW
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
                        outline="RoyalBlue",
                        width=3)
        draw.rectangle(((xmin, ymin), (xmin + text_width, ymin + text_height)),
                       fill="RoyalBlue")
        draw.text((xmin, ymin), text, font=font, align="left", fill="White")

    image.save(save_path)


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("model", type=str, help="path/to/model.onnx")
    ap.add_argument("images", type=str, help="path/to/*.jpg", nargs='+')
    ap.add_argument("--labels", type=str, help="Provide a list of labels", nargs='+', default=["coffeecup"])
    ap.add_argument("--score", type=float, default=0.25)
    ap.add_argument("--iou", type=float, default=0.70)
    ap.add_argument("--save", type=str, default="results")
    args = ap.parse_args()

    ms = lambda: int(round(time.time() * 1000))
    inference_times = []
    os.makedirs(args.save, exist_ok=True)

    # Loading the Model
    providers = onnxruntime.get_available_providers()
    if 'TensorrtExecutionProvider' in providers:
        providers.remove('TensorrtExecutionProvider')
    print(f"Using Execution Providers: {providers}")
    model = onnxruntime.InferenceSession(args.model, providers=providers)

    inputs = model.get_inputs()
    outputs = model.get_outputs()
    output_names = [x.name for x in outputs]
    
    # Multitask model
    if len(outputs) > 2: 
        labels = ["background"] + args.labels
    else:
        labels = args.labels
    nc = len(labels)  # number of classes

    for image_path in args.images:
        image, size = get_input(image_path, inputs)

        # Model Inference
        t0 = ms()
        outputs = model.run(output_names, {inputs[0].name: image})
        tt = ms() - t0
        inference_times.append(tt)

        box_id, score_id, mask_id = None, None, None
        for i, x in enumerate(outputs):
            shape = x.shape
            if len(shape) == 4 and shape[-1] == 4:
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
