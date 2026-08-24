# Linux

The EdgeFirst Profiler ships prebuilt binaries for **x86_64** and **aarch64** Linux against the manylinux2014 baseline (glibc 2.17+). Both architectures get the same default backend, ONNX Runtime, plus optional accelerator backends that load at runtime from their vendor libraries.

## Install

=== "Python (pip)"

    ```sh
    pip install edgefirst-profiler
    ```

=== "Platform installer"

    ```sh
    curl -fsSL https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.sh | bash
    ```

    The installer drops the binary into `/usr/local/bin` (run as root) or `~/.local/bin` (otherwise). It installs the latest release by default; to pin one, append `-s -- --version <version>` to the `bash` invocation.

Confirm:

```sh
edgefirst-profiler --version
```

## Default backend: ONNX Runtime

The default build profiles `.onnx` models on CPU. The profiler dlopens `libonnxruntime.so` at startup; install it once per system:

=== "Debian / Ubuntu"

    ```sh
    sudo apt install libonnxruntime  # or pip install onnxruntime to grab the bundled .so
    ```

=== "Fedora / RHEL"

    ```sh
    sudo dnf install onnxruntime
    ```

=== "From the ORT release tarball"

    Download a matching release from [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime/releases) and place `libonnxruntime.so.<version>` somewhere on the loader path (e.g. `/usr/local/lib`) or set `ORT_DYLIB_PATH`.

### Inference concurrency on CPU

On the CPU execution provider, the profiler chooses how many inferences to run at once from the machine's core count, and splits the cores between the concurrent inference sessions and the surrounding decode stages. The defaults come from fleet measurements on machines from 1 to 96 cores; override the concurrency per run with `--inference-depth N` or the `INFERENCE_DEPTH` environment variable.

### FP32 accuracy on Arm CPUs

On 64-bit Arm hosts, ONNX Runtime's BF16 fast-math GEMM kernels are **off by default**, so FP32 runs are genuinely FP32 and score the same as x86. Earlier releases enabled them by default, which quietly computed `MatMul`/`Gemm` in bfloat16 while reporting the run as FP32 — models with attention blocks (YOLO11, YOLO26) collapsed to near-zero mAP on Arm. Set `EDGEFIRST_ORT_BF16_FASTMATH=1` to opt back in for throughput experiments, bearing in mind that such a run is not an FP32 measurement.

## Optional: NVIDIA CUDA

Pass `--provider cuda` to offload ONNX inference onto an NVIDIA GPU. This works on x86_64 Linux with a discrete GPU and on aarch64 Linux for NVIDIA Jetson / L4T — see the [Jetson Orin guide](jetson_orin.md). CUDA and cuDNN libraries must be present on the system path. If they are missing, the profiler prints an actionable error naming the missing library and the exact `pip install` command — with the specific `nvidia-…-cu12` package filled in — to resolve it. A pre-built [`cuda` container image](docker.md) is also available with the GPU ONNX Runtime and CUDA/cuDNN closure bundled.

**Auto-selected depth on x86_64 Linux with `--provider cuda`:** inference depth 4, preprocess depth 1. Each additional ORT inference slot overlaps GPU execution with host staging, peaking at depth 4; a single preprocess thread avoids CPU contention with CUDA kernel dispatch. Measured on an RTX 4060 with YOLOv8n fp16 at 640×640, this yields approximately 352 → 447 FPS (+27%) compared to the CPU default. The launch-time dialog shows these values under **Auto** when CUDA is selected. The single preprocess worker is a measured override specific to this target — everywhere else, pre-processing fans out to 4 workers by default, whether the images are staged through the CPU or converted zero-copy on the GPU.

**CUDA zero-copy input path (OpenGL–CUDA interop):** disabled by default on x86_64 Linux. On discrete GPUs the GL→CUDA synchronization competes with CUDA inference kernel dispatch, while the PCIe DMA path runs independently — measured at 347 FPS (CPU staging) vs 238 FPS (GL interop) on an RTX 4060. Set `EDGEFIRST_ENABLE_CUDA_ZEROCOPY=1` to opt in; this is useful for benchmarking or integrated targets where the PCIe copy is the bottleneck.

!!! note
    The previous environment variable `EDGEFIRST_DISABLE_CUDA_ZEROCOPY` no longer has any effect.

## Optional: TensorFlow Lite

The TFLite backend handles `.tflite` models and the XNNPACK delegate for accelerated CPU inference. It requires the native TFLite runtime library, `libtensorflow-lite.so`, on the host — not the Python `tflite` or `tflite_runtime` packages, which is why installing those appears to do nothing. Point the profiler at a non-standard location with the `TFLITE_LIBRARY_PATH` environment variable, or use the [`tflite` container image](docker.md), which bundles the runtime. The TFLite runtime is also the gateway to the **NXP Neutron** and **VSI** NPU delegates on i.MX targets — those delegates are `.so` files passed to the profiler via `--delegate`. See the [NXP i.MX 95](imx95.md) and [NXP i.MX 8M Plus](imx8mplus.md) guides.

!!! tip "Preferred runtime on desktop"
    Outside embedded i.MX targets, ONNX Runtime with a platform-appropriate execution provider — CUDA, CoreML, or plain CPU — is the preferred runtime on desktop platforms. Reach for the TFLite backend when you are targeting the NXP Neutron/VSI NPU delegates.

## Verifying the install

After install, sign in to Studio and confirm the credentials are saved:

```sh
edgefirst-profiler login
edgefirst-profiler              # opens TUI on F1 Help
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).

!!! note "Validation needs a writable project"
    Creating a validation session requires write access to the Studio project — you cannot profile against the read-only public **Sample Project** directly. First [copy its dataset](../../getting_started/copy_dataset.md) into a project you own, then create the session there.

If `libonnxruntime` is not found when a session starts, the error message tells you exactly which library is missing and where it was looked for.

## Uninstall

=== "Python (pip)"

    ```sh
    pip uninstall edgefirst-profiler
    ```

=== "Platform installer"

    Delete the binary from wherever the installer placed it:

    ```sh
    rm /usr/local/bin/edgefirst-profiler        # or ~/.local/bin/edgefirst-profiler
    ```

The profiler stores cached downloads in `~/.cache/edgefirst-profiler/` (or `$EDGEFIRST_CACHE`). Remove the cache directory if you want a clean slate.
