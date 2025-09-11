import zenoh
from zenoh import Encoding
from edgefirst.schemas.edgefirst_msgs import DmaBuffer, Box, Detect, Track
from edgefirst.schemas.std_msgs import Header
from edgefirst.schemas.builtin_interfaces import Time
from tflite_runtime.interpreter import Interpreter, load_delegate 
from PIL import Image, ImageDraw, ImageFont
from argparse import ArgumentParser
import sys
import mmap
import ctypes
import os
import asyncio
import time
import numpy as np
import cv2
import threading

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


# Constants for syscall
SYS_pidfd_open = 434  # From syscall.h
SYS_pidfd_getfd = 438 # From syscall.h
GETFD_FLAGS = 0

# C bindings to syscall (Linux only)
if sys.platform.startswith('linux'):
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
else:
    print("DMA only works on EdgeFirst Platforms")
    sys.exit(0)

def pidfd_open(pid: int, flags: int = 0) -> int:
    return libc.syscall(SYS_pidfd_open, pid, flags)

def pidfd_getfd(pidfd: int, target_fd: int, flags: int = GETFD_FLAGS) -> int:
    return libc.syscall(SYS_pidfd_getfd, pidfd, target_fd, flags)

def draw_output(res, image_path, save_path, score_threshold=0.50):
    image = image_path
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

class MessageDrain:
    def __init__(self, loop):
        self._queue = asyncio.Queue(maxsize=100)
        self._loop = loop

    def callback(self, msg):
        if not self._loop.is_closed():
            if self._queue.full():
                self._queue.get_nowait()
            self._loop.call_soon_threadsafe(self._queue.put_nowait, msg)

    async def read(self):
        return await self._queue.get()

    async def get_latest(self):
        latest = await self._queue.get()
        while not self._queue.empty():
            latest = self._queue.get_nowait()
        return latest

def dma_worker(msg, ip, ids, session, args):
    dma_buf = DmaBuffer.deserialize(msg.payload.to_bytes())
    input_timestamp = Time(sec=dma_buf.header.stamp.sec,
                           nanosec=dma_buf.header.stamp.nanosec)
    pidfd = pidfd_open(dma_buf.pid)
    if pidfd < 0:
        return

    fd = pidfd_getfd(pidfd, dma_buf.fd, GETFD_FLAGS)
    if fd < 0:
        return

    # Now fd can be used as a file descriptor
    mm = mmap.mmap(fd, dma_buf.length)
    yuy2_bytes = mm[:dma_buf.length]
    im_buf = np.frombuffer(yuy2_bytes, dtype=np.uint8)
    mm.close()
    os.close(fd)
    os.close(pidfd)

    input_shape = [int(x) for x in args.shape.split(',')]
    if len(input_shape) != 2:
        raise AssertionError("Input shape should be only the height and width, ie. 300,300")

    fourcc_str = "".join([chr((dma_buf.fourcc >> (8 * i)) & 0xFF) for i in range(4)])
    
    # YUY2 is 2 bytes per pixel, so shape is (height, width * 2)
    if fourcc_str == "YUYV":
        yuy2_np = im_buf.reshape((dma_buf.height, dma_buf.width, 2))
        # Convert YUY2 to RGB
        rgb_img = cv2.cvtColor(yuy2_np, cv2.COLOR_YUV2RGB_YUY2)
    elif fourcc_str == "RGBA":
        rgb_img = im_buf.reshape((dma_buf.height, dma_buf.width, 4))
        rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGBA2RGB)
    else:
        print("Image type %s currently unsupported for this sample")
        return

    rgb_img = cv2.resize(rgb_img, (input_shape[0], input_shape[1]))
    rgb_img = np.transpose(rgb_img, [1,0,2])
    rgb_img = np.reshape(rgb_img, [1] + list(rgb_img.shape))
    

    ip.set_tensor(ids[4], rgb_img)
    start_time = time.time()
    ip.invoke()
    model_time = time.time() - start_time
    model_sec = int(model_time)
    model_nanosec = int((model_time - model_sec) * 1e9)
    model_timestamp = Time(sec = model_sec,
                           nanosec = model_nanosec)
    
    boxes = ip.get_tensor(ids[0]).squeeze()
    classes = ip.get_tensor(ids[1]).squeeze()
    scores = ip.get_tensor(ids[2]).squeeze()
    num_det = ip.get_tensor(ids[3]).squeeze()

    publish_boxes = []
    for i in range(int(num_det)):
        if scores[i] < args.threshold:
            continue
        center_x = (boxes[i][2] + boxes[i][0]) / 2
        center_y = (boxes[i][3] + boxes[i][1]) / 2
        width = boxes[i][2] - boxes[i][0]
        height = boxes[i][3] - boxes[i][1]
        label = image_classes[int(classes[i]) + 1]
        publish_boxes.append(Box(center_x = center_x,
                                 center_y = center_y,
                                 width = width,
                                 height = height,
                                 label = label,
                                 score = scores[i],
                                 track=Track()))
    now = time.time()
    cur_sec = int(now)
    cur_nanosec = int((now - cur_sec) * 1e9)
    output_timestamp = Time(sec=cur_sec, nanosec=cur_nanosec)
    detect_header = Header(stamp=Time(sec=cur_sec, nanosec=cur_nanosec))
    detect_obj = Detect(header=detect_header,
                        input_timestamp=input_timestamp,
                        model_time=model_timestamp,
                        output_time=output_timestamp,
                        boxes=publish_boxes)

    session.put("rt/model/boxes2d", detect_obj.serialize(),
                encoding="edgefirst_msgs/msg/Detect")

async def dma_handler(drain, ip, ids, session, args):
    while True:
        try:
            msg = await drain.get_latest()
            thread = threading.Thread(target=dma_worker, args=[msg, ip, ids, session, args])
            thread.start()
            
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
        except KeyboardInterrupt:
            while thread.is_alive():
                await asyncio.sleep(0.001)
            thread.join()
            break
    
async def main_async(args):
    # Setup rerun
    # Zenoh config
    config = zenoh.Config()
    config.insert_json5("scouting/multicast/interface", "'lo'")
    session = zenoh.open(config)

    # Create drains
    loop = asyncio.get_running_loop()
    drain = MessageDrain(loop)

    delegate = "/usr/lib/libvx_delegate.so"
    if os.path.exists(delegate):
        ext_delegate = load_delegate(delegate, {})
        ip = Interpreter(model_path=args.model, experimental_delegates=[ext_delegate])
    else:
        ip = Interpreter(model_path=args.model)

    ip.allocate_tensors()
    ip.invoke() # Model warmup

    ids = []
    out_det = ip.get_output_details()
    ids.append(out_det[0]["index"])
    ids.append(out_det[1]["index"])
    ids.append(out_det[2]["index"])
    ids.append(out_det[3]["index"])
    ids.append(ip.get_input_details()[0]["index"])

    session.declare_subscriber('rt/camera/dma', drain.callback)
    try:
        await asyncio.gather((dma_handler(drain, ip, ids, session, args)))
    except KeyboardInterrupt:
        session.close()
        sys.exit(0)


def main():
    args = ArgumentParser(description="EdgeFirst Samples - Detect Publisher")
    args.add_argument('-m', '--model', type=str, default=None,
                      help="The model that will be performing inference.")
    args.add_argument('-t', '--threshold', type=float, default=0.5,
                      help="The score threshold for boxes to be published.")
    args.add_argument('-s', '--shape', type=str, default="300,300",
                      help="Comma delimited input shape of the model h,w")
    args = args.parse_args()

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
