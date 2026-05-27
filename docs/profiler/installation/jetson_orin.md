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

A stable, JetPack-compatible `onnxruntime-gpu` aarch64 wheel channel is not currently available — the Jetson AI Lab index is intermittent and the EdgeFirst-maintained channel is not yet published. Until that lands, **ONNX Runtime on Jetson is CPU-only** through the standard PyPI wheel:

```sh
pip install onnxruntime
```

For GPU inference on Jetson, convert the model to a TensorRT engine first and let the profiler load it through the TensorRT backend described below. See the [TensorRT Converter](https://doc.edgefirst.ai/test/models/conversion/tensorrt/) for the conversion workflow.

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
