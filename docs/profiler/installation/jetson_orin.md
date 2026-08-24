# NVIDIA Jetson Orin

The EdgeFirst Profiler runs on **NVIDIA Jetson Orin** and **Orin Nano** (aarch64) with two acceleration paths:

- **ONNX Runtime with the CUDA execution provider** — drop-in for `.onnx` models, no extra dependencies beyond JetPack's CUDA runtime.
- **TensorRT backend** — for `.engine` / `.trt` files. Loads `libtrt_shim.so`, a thin C++ shim the profiler links to at runtime so the binary itself has zero compile-time CUDA/TensorRT dependencies.

For a guided platform tour see the [NVIDIA Jetson Quick Start](../../platforms/quickstart/jetson_orin/index.md). This page covers only the profiler-specific setup.

## Prerequisites

A working JetPack install with:

- CUDA Runtime
- cuDNN
- TensorRT 10.x (for the TensorRT backend)

```sh
nvcc --version          # CUDA toolkit visible (Jetson devices do not ship nvidia-smi)
ls /usr/lib/aarch64-linux-gnu/libnvinfer.so*   # TensorRT installed
```

If `nvcc` is missing, install the CUDA toolkit packages from JetPack, or check the JetPack/L4T version file at `/etc/nv_tegra_release`.

## Install the profiler

=== "Python (pip)"

    ```sh
    pip install edgefirst-profiler
    ```

=== "Platform installer"

    ```sh
    curl -fsSL https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.sh | bash
    ```

    The aarch64 Linux build is selected automatically.

Confirm:

```sh
edgefirst-profiler --version
```

## ONNX Runtime on Jetson

The CUDA execution provider (`--provider cuda`) runs on Jetson / L4T, so `.onnx` models can be measured on the GPU the same way desktop GPUs are — a CUDA-enabled `libonnxruntime` must be present on the host. The simplest way to get one is the multi-architecture [`cuda` container image](docker.md), which bundles the GPU ONNX Runtime for JetPack 6.2 (CUDA 12.6); on Jetson, run it with `--runtime nvidia` and the container picks up the Tegra driver automatically:

```sh
docker run -it --rm --runtime nvidia -v edgefirst:/config ghcr.io/edgefirstai/profiler-cli:cuda
```

For a CPU baseline, the standard PyPI wheel (`pip install onnxruntime`) provides the CPU-only `libonnxruntime`.

With the CUDA execution provider, per-frame inference time is measured on the GPU's own clock rather than the host clock, removing host scheduling jitter from the reported number (with an automatic host-clock fallback if the GPU clock is unavailable).

Alternatively, convert the model to a TensorRT engine and let the profiler load it through the TensorRT backend described below. See the [TensorRT Converter](../../models/conversion/tensorrt.md) for the conversion workflow.

## TensorRT (recommended for Jetson)

TensorRT is the canonical Jetson backend. The profiler accepts both compiled `.engine` files and source `.onnx` files (which it builds into engines on first use).

### Install `libtrt_shim.so`

The profiler's TensorRT support routes every TensorRT and CUDA call through `libtrt_shim.so`, a thin C++ shared library that wraps the TensorRT 10.x C++ API behind a flat C ABI. The shim is built on the Jetson itself once and dlopened by the profiler at runtime.

A prebuilt `libtrt_shim.so` is included in the EdgeFirst Jetson SDK image; check `/usr/local/lib` and `/usr/lib/aarch64-linux-gnu` before building from source. If you need to rebuild it:

```sh
# From the profiler source tree — build on the target Jetson.
cd shims/trt-shim
mkdir build && cd build
cmake .. && make
sudo install -m 0755 libtrt_shim.so /usr/local/lib/
sudo ldconfig
```

### Per-layer profiling

Enable per-layer GPU profiling on a validation session with the `--layer-profile` flag — TensorRT's `IProfiler` callback reports execution time for every fused layer. Per-layer overhead is roughly 5–10%, so leave it off when measuring deployment latency and on when investigating a bottleneck.

### Throughput and pipeline overlap

TensorRT validation now keeps multiple frames in flight: the GPU works on frame N while frame N+1 is being captured and preprocessed, and detection outputs are read straight from GPU memory rather than copied back to the host first. Measured full-pipeline throughput on a Jetson Orin Nano is **~272 FPS** (yolov5n at 640×640, COCO 5k, MAXN_SUPER); the device itself measures ~358 FPS model-only, so the full image pipeline — not the GPU — is the gate. Detection accuracy is unchanged.

On the Orin Nano the auto pipeline depths are deliberately pinned below the device maximum: **capture 2, inference 4, postprocess 2**. The full pipeline is CPU-contention-bound on the 6-core SoC, not decode-bound — at the generic auto of 4 capture and 4 postprocess workers, the CPU stages oversubscribe the cores and starve the priority-boosted inference dispatch thread, measuring ~250 FPS; pinning capture and postprocess to 2 frees cores for preprocessing and inference and lifts throughput to ~272 FPS.

!!! note "GPU JPEG decode is deliberately not used"
    nvJPEG could decode the dataset's JPEG files on the GPU, but on this shared iGPU it steals streaming multiprocessors from inference and measures **slower** end to end, so the profiler decodes on the CPU by design. Image decode is not the pipeline's gate on the Orin Nano.

The Perfetto trace gains per-frame `trt.h2d`, `trt.infer`, and `trt.d2h` tracks (host-to-device, TensorRT inference, device-to-host) measured with CUDA events, so GPU-side durations are accurate rather than host-side approximations. Falls back automatically on hardware that doesn't support the required GPU memory capabilities.

### Power monitoring

Jetson boards carry an on-board INA3221 power monitor, so the dashboard reports live power: the board-input rail plus its per-component breakdown (for example the CPU/GPU/SoC and DRAM rails), each shown under its real name, and the session report adds a board-power line. The board total is counted once — on a multi-rail device that also exposes a board-total channel, the total is no longer double-added to its own components, which previously inflated a ~6.7 W reading to ~29 W on the Orin Nano.

### Engine sidecar metadata

Compiled TensorRT engines do not carry the EdgeFirst decoder metadata that ONNX `metadata_props` or TFLite associated-files do. The profiler reads sidecars from the engine's parent directory:

- `edgefirst.json` — decoder task, input size, class names
- `labels.txt` — one class name per line (fallback if not in JSON)

Without these the profiler still runs but in **timing-only mode** — no predictions and no mAP. It prints a clear note on stderr explaining what is missing.

## Verifying the install

```sh
edgefirst-profiler login
edgefirst-profiler              # opens TUI on F1 Help
```

If `libtrt_shim.so` is missing when a TensorRT session starts, the error message tells you the search path explicitly — there is no `dlopen` traceback.

## FP16 accuracy reference

Across the YOLO segmentation models tested on Jetson Orin Nano, TensorRT FP16 mixed-precision preserves **box mAP within ±1.6% of FP32**. Mask mAP can see a larger penalty (−0.6% to −6.6%) due to FP16 rounding in the `sigmoid(mask_coeffs @ protos)` multiplication path — a known Ultralytics issue ([#14407](https://github.com/ultralytics/ultralytics/issues/14407), [#13776](https://github.com/ultralytics/ultralytics/issues/13776)). Box coordinates do not pass through the sigmoid and are largely unaffected.
