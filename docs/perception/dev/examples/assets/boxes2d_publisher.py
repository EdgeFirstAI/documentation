# SPDX-License-Identifier: Apache-2.0
# Copyright © 2025 Au-Zone Technologies. All Rights Reserved.

import zenoh
from edgefirst.schemas.edgefirst_msgs import CameraFrame, DetectBox, Model
from edgefirst.schemas.std_msgs import Header
from edgefirst.schemas.builtin_interfaces import Duration
from tflite_runtime.interpreter import Interpreter, load_delegate 
from PIL import Image, ImageDraw, ImageFont
from argparse import ArgumentParser
import sys
import mmap
import ctypes
import os
import socket
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


def duration_since(start_time):
    elapsed = time.time() - start_time
    sec = int(elapsed)
    return Duration(sec=sec, nanosec=int((elapsed - sec) * 1e9))


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

def frame_worker(msg, ip, ids, session, host, args):
    try:
        frame = CameraFrame.from_cdr(msg.payload.to_bytes())
    except Exception as e:
        print(f"Error processing Camera Frame: {e}", file=sys.stderr)
        return

    decode_start = time.time()
    tensor = frame.tensor
    height, width = tensor.shape[0], tensor.shape[1]

    pidfd = pidfd_open(tensor.pid)
    if pidfd < 0:
        return

    # All planes of the frame share one DMA buffer, so the handle of the
    # first plane is enough to reach the whole frame.
    fd = pidfd_getfd(pidfd, tensor.planes[0].handle, GETFD_FLAGS)
    if fd < 0:
        return

    length = max(p.offset + p.size for p in tensor.planes)
    mm = mmap.mmap(fd, length, offset=0)
    nv12 = b"".join(mm[p.offset:p.offset + p.used] for p in tensor.planes)
    mm.close()
    os.close(fd)
    os.close(pidfd)

    input_shape = [int(x) for x in args.shape.split(',')]
    if len(input_shape) != 2:
        raise AssertionError("Input shape should be only the height and width, ie. 300,300")

    nv12_np = np.frombuffer(nv12, dtype=np.uint8).reshape((height * 3 // 2, width))
    rgb_img = cv2.cvtColor(nv12_np, cv2.COLOR_YUV2RGB_NV12)

    rgb_img = cv2.resize(rgb_img, (input_shape[0], input_shape[1]))
    rgb_img = np.transpose(rgb_img, [1, 0, 2])
    rgb_img = np.reshape(rgb_img, [1] + list(rgb_img.shape))
    input_time = duration_since(decode_start)

    ip.set_tensor(ids[4], rgb_img)
    model_start = time.time()
    ip.invoke()
    model_time = duration_since(model_start)

    output_start = time.time()
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
        publish_boxes.append(DetectBox(center_x=center_x,
                                       center_y=center_y,
                                       width=width,
                                       height=height,
                                       label=label,
                                       score=float(scores[i])))

    # Propagate the camera frame's own acquisition timestamp so consumers
    # (e.g. the Web UI) can align these boxes with the frame they came from.
    model_header = Header(stamp=frame.stamp, frame_id=frame.frame_id)
    model_obj = Model(header=model_header,
                      input_time=input_time,
                      model_time=model_time,
                      output_time=duration_since(output_start),
                      decode_time=duration_since(decode_start),
                      boxes=publish_boxes)

    session.put(f"{host}/model/output", model_obj.to_bytes(),
                encoding="edgefirst_msgs/msg/Model")

async def frame_handler(drain, ip, ids, session, host, args):
    while True:
        try:
            msg = await drain.get_latest()
            thread = threading.Thread(target=frame_worker, args=[msg, ip, ids, session, host, args])
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
    host = socket.gethostname()

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

    session.declare_subscriber(f"{host}/camera/frame", drain.callback)
    try:
        await asyncio.gather((frame_handler(drain, ip, ids, session, host, args)))
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

