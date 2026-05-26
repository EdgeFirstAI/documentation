# Installation

The EdgeFirst Profiler is distributed three ways, with the same native binary in every case:

- **`pip install edgefirst-profiler`** — the convenience path. Pulls the binary plus the few Python-side helpers needed for end-to-end workflows. This is the recommended default.
- **Platform installer scripts** (`install.sh` / `install.ps1`) — the right choice for environments where Python is not available, or where the binary needs to land in a system-wide path like `/usr/local/bin`.
- **Vendor-shipped EdgeFirst images** — pre-installed and pinned to the BSP version for that target. Nothing to do.

Per-target pages below cover the runtime libraries, NPU delegates, daemons, and quirks that apply once the binary is in place.

## Supported targets

| Target | Architecture | Default backend | Optional accelerator |
|---|---|---|---|
| [Linux](linux.md) | x86_64, aarch64 | ONNX Runtime (CPU) | TFLite XNNPACK |
| [macOS](macos.md) | Apple Silicon | ONNX Runtime (CPU) | CoreML execution provider |
| [Windows](windows.md) | x86_64 | ONNX Runtime (CPU) | — |
| [NVIDIA Jetson Orin](jetson_orin.md) | aarch64 | ONNX Runtime (CUDA EP) | TensorRT (via `libtrt_shim.so`) |
| [NXP i.MX 95](imx95.md) | aarch64 | TFLite | Neutron NPU delegate |
| [NXP i.MX 8M Plus](imx8mplus.md) | aarch64 | TFLite | VSI NPU delegate |
| [Raspberry Pi 5](raspberrypi.md) | aarch64 | ONNX Runtime (CPU) | Hailo-8 / 8L (via HailoRT) |
| [Kinara Ara-2](kinara.md) | x86_64 / aarch64 host | DVM via `ara2-proxy` | — |
| [Hailo-8 / 8L](hailo.md) | any host with HailoRT | HailoRT | — |

The profiler binary is the same on every target — what varies is which **runtime libraries** must be present on the system so the matching backend can `dlopen` them. Every backend loads its vendor library dynamically; nothing is statically linked, so a missing library on one target never breaks the profiler on another.

## Backends and how they are selected

The inference backend is chosen automatically from the model file extension:

| Extension | Backend | Runtime dependency |
|---|---|---|
| `.onnx` | ONNX Runtime | `libonnxruntime.so` / `.dylib` |
| `.tflite` | TensorFlow Lite | `libtensorflowlite_c.so` (Linux only) |
| `.dvm` | Kinara Ara-2 | `ara2-proxy` daemon (Linux only) |
| `.hef` | Hailo | `libhailort.so` (Linux only) |
| `.engine` / `.trt` | TensorRT | `libtrt_shim.so` on Jetson |

When the runtime library is missing, the profiler reports a clear error pointing at the per-target installation guide — not a `dlopen` traceback.
