# Installation

The EdgeFirst Profiler is distributed four ways. Each ships the matching native binary for your host's OS and architecture (`x86_64` / `aarch64`, Linux / macOS / Windows) — the source and the CLI are identical, only the compiled artifact differs.

- **`pip install edgefirst-profiler`** — the convenience path. Pulls the binary plus the few Python-side helpers needed for end-to-end workflows. This is the recommended default.
- **Platform installer scripts** (`install.sh` / `install.ps1`) — the right choice for environments where Python is not available, or where the binary needs to land in a system-wide path like `/usr/local/bin`.
- **Container images** — pre-built images on the GitHub Container Registry (`ghcr.io/edgefirstai/profiler-cli`) with the inference runtime already bundled, published per release as CPU, CUDA, TFLite, and NXP NPU variants. See [Container Images](docker.md).
- **Vendor-shipped EdgeFirst images** — pre-installed and pinned to the BSP version for that target. Nothing to do.

Per-target pages below cover the runtime libraries, NPU delegates, daemons, and quirks that apply once the binary is in place.

## Supported targets

| Target | Architecture | Default backend | Optional accelerator |
| ------ | ------------ | --------------- | -------------------- |
| [Linux](linux.md) | x86_64, aarch64 | ONNX Runtime (CPU) | TFLite XNNPACK |
| [macOS](macos.md) | Apple Silicon | ONNX Runtime (CPU) | CoreML execution provider |
| [Windows](windows.md) | x86_64 | ONNX Runtime (CPU) | — |
| [NVIDIA Jetson Orin](jetson_orin.md) | aarch64 | ONNX Runtime (CUDA EP) | TensorRT (via `libtrt_shim.so`) |
| [NXP i.MX 95](imx95.md) | aarch64 | TFLite | Neutron NPU delegate |
| [NXP i.MX 8M Plus](imx8mplus.md) | aarch64 | TFLite | VSI NPU delegate |
| [Raspberry Pi 5](raspberrypi.md) | aarch64 | ONNX Runtime (CPU) | Hailo-8 / 8L (via HailoRT) |
| [Kinara Ara240](kinara.md) | x86_64 / aarch64 host | DVM via `ara2-proxy` | — |
| [Hailo-8 / 8L](hailo.md) | any host with HailoRT | HailoRT | — |
| Android (Snapdragon) | aarch64 | ONNX Runtime (QNN EP, `--provider qnn-htp`) | TFLite QNN / GPU delegates (experimental) |

Android support runs inside the EdgeFirst mobile applications rather than as a standalone CLI install. The ONNX route takes a Qualcomm-precompiled `*.qnn.onnx` artifact and runs it on the Hexagon NPU through ONNX Runtime's QNN execution provider; the device must supply the Qualcomm runtime and a QNN-enabled ONNX Runtime — the profiler ships neither. The experimental TFLite `--delegate qnn` and `--delegate gpu` routes are available to try but are excluded from published hardware comparisons for now.

The profiler CLI and the workflow it drives are the same on every target — what varies (besides the OS/arch-matched binary) is which **runtime libraries** must be present on the system so the matching backend can `dlopen` them. Every backend loads its vendor library dynamically; nothing is statically linked, so a missing library on one target never breaks the profiler on another.

## Backends and how they are selected

The inference backend is chosen automatically from the model file extension:

| Extension | Backend | Runtime dependency |
| --------- | ------- | ------------------ |
| `.onnx` | ONNX Runtime | `libonnxruntime.so` (Linux) / `libonnxruntime.dylib` (macOS) / `onnxruntime.dll` (Windows) |
| `*.qnn.onnx` | ONNX Runtime (QNN EP) | Android only — QNN-enabled ONNX Runtime plus the Qualcomm runtime, supplied by the device |
| `.tflite` | TensorFlow Lite | `libtensorflow-lite.so` (Linux only); override the search path with `TFLITE_LIBRARY_PATH` |
| `.dvm` | Kinara Ara240 | `ara2-proxy` daemon (Linux only) |
| `.hef` | Hailo | `libhailort.so` (Linux only) |
| `.engine` / `.trt` | TensorRT | `libtrt_shim.so` on Jetson |

When the runtime library is missing, the profiler reports a clear error pointing at the per-target installation guide — not a `dlopen` traceback.
