import numpy as np
from PIL import Image, ImageFont, ImageDraw
import onnxruntime

# NMS implementation in Python and Numpy
def NMS(bboxes, psocres, threshold):

    xmin = bboxes[:, 0]
    ymin = bboxes[:, 1]
    xmax = bboxes[:, 2]
    ymax = bboxes[:, 3]

    sorted_idx = psocres.argsort()[::-1]
    areas = (xmax - xmin + 1) * (ymax - ymin + 1)

    keep = []
    while len(sorted_idx) > 0:
        rbbox_i = sorted_idx[0]
        keep.append(rbbox_i)

        overlap_xmins = np.maximum(xmin[rbbox_i], xmin[sorted_idx[1:]])
        overlap_ymins = np.maximum(ymin[rbbox_i], ymin[sorted_idx[1:]])
        overlap_xmaxs = np.minimum(xmax[rbbox_i], xmax[sorted_idx[1:]])
        overlap_ymaxs = np.minimum(ymax[rbbox_i], ymax[sorted_idx[1:]])

        overlap_widths = np.maximum(0, (overlap_xmaxs - overlap_xmins+1))
        overlap_heights = np.maximum(0, (overlap_ymaxs - overlap_ymins+1))
        overlap_areas = overlap_widths * overlap_heights

        ious = overlap_areas / \
            (areas[rbbox_i] + areas[sorted_idx[1:]] - overlap_areas)

        delete_idx = np.where(ious > threshold)[0]+1
        delete_idx = np.concatenate(([0], delete_idx))

        sorted_idx = np.delete(sorted_idx, delete_idx)

    return keep

# Loading the Model
providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
model_path = "modelpack.onnx"
model = onnxruntime.InferenceSession(model_path, providers=providers)

inputs = model.get_inputs()
outputs = model.get_outputs()

dtype = inputs[0].type
shape = inputs[0].shape[1:3]
height, width = shape

output_names = [x.name for x in outputs]

# Loading the Image
image_path = "sample-coffee-cup.jpg"
original = Image.open(image_path)

# Image Preprocessing
image = original.resize((width, height))
image = np.array(image).astype(np.uint8) 
input_tensor = np.expand_dims(image, axis=0).astype(np.float32)
input_tensor /= 255.0 # Float models requires unsigned normalization.

# Model Inference
outputs = model.run(output_names, {model.get_inputs()[0].name: input_tensor})

# Parsing the Outputs
boxes, classes, scores, masks = None, None, None, None
if isinstance(outputs, list):
    for output in outputs:
        if len(output.shape) == 4:
            if output.shape[-2] == 1:
                boxes = output
            else:
                masks = output
        else:
            scores = output
else:
    masks = outputs

# Setting NMS Parameters
iou_threshold = 0.50
score_threshold = 0.25

# Decoding Detection Outputs
boxes = np.reshape(boxes, (-1, 4))
scores = scores[0][..., 1:]  # Remove background boxes first
classes = np.argmax(scores, axis=-1).reshape(-1)

# Apply NMS Filters
max_scores = np.max(scores, axis=-1)
mask = max_scores >= score_threshold
scores = max_scores[mask]
boxes = boxes[mask]
classes = classes[mask]

keep = NMS(
    boxes,
    scores,
    threshold=iou_threshold
)

boxes = boxes[keep]
scores = scores[keep]
classes = classes[keep]

# Decoding Segmentation Masks
masks = np.argmax(masks, axis=-1)
masks = masks.astype(np.uint8)
masks = Image.fromarray(masks[0])
masks = masks.resize((original.width, original.height), Image.NEAREST)

# Visualization of the Outputs
with open('labels.txt', 'r') as f:
    labels = f.readlines()
labels = [label.strip() for label in labels]
labels.remove("background")
colors = np.random.randint(0, 256, (len(labels), 3))

font = ImageFont.load_default()
font._size = 500

# Draw Bounding Boxes
for box, score, cls in zip(boxes, scores, classes):
    xmin, ymin, xmax, ymax = box
    # Resize boxes to original size
    xmin = int(xmin * original.width)
    ymin = int(ymin * original.height)
    xmax = int(xmax * original.width)
    ymax = int(ymax * original.height)
    # Draw boxes into original image
    draw = ImageDraw.Draw(original)
    draw.rectangle((xmin, ymin, xmax, ymax),
                    outline=tuple(colors[cls]), width=5)
    draw.text((xmin, ymin),
                f"{labels[cls]}: {score:.2f}", fill=(0,0,0), font=font)

# Draw Segmentation masks
unique_labels = np.unique(masks).tolist()
unique_labels.sort()

for label in unique_labels[1:]:
    mask = np.array(masks)
    mask = mask == label
    color_mask = np.array(original)
    color_mask[mask] = colors[label - 1]
    original = Image.blend(
        original.convert('RGBA'),
        Image.fromarray(color_mask).convert('RGBA'),
        alpha=0.5
    )

original.save("output_onnx.png")
