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

    The installer drops the binary into `/usr/local/bin` (run as root) or `~/.local/bin` (otherwise). Pin a specific release with `--version`:

    ```sh
    curl -fsSL https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.sh | bash -s -- --version 1.0.1
    ```

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

## Optional: NVIDIA CUDA (x86_64)

Pass `--provider cuda` to offload ONNX inference onto an NVIDIA GPU. CUDA and cuDNN libraries must be present on the system path. If they are missing, the profiler prints an actionable error naming the missing library and the exact `pip install` command — with the specific `nvidia-…-cu12` package filled in — to resolve it.

**Auto-selected depth on x86_64 Linux with `--provider cuda`:** inference depth 4, preprocess depth 1. Each additional ORT inference slot overlaps GPU execution with host staging, peaking at depth 4; a single preprocess thread avoids CPU contention with CUDA kernel dispatch. Measured on an RTX 4060 with YOLOv8n fp16 at 640×640, this yields approximately 352 → 447 FPS (+27%) compared to the CPU default. The launch-time dialog shows these values under **Auto** when CUDA is selected.

**CUDA zero-copy input path (OpenGL–CUDA interop):** disabled by default on x86_64 Linux. On discrete GPUs the GL→CUDA synchronization competes with CUDA inference kernel dispatch, while the PCIe DMA path runs independently — measured at 347 FPS (CPU staging) vs 238 FPS (GL interop) on an RTX 4060. Set `EDGEFIRST_ENABLE_CUDA_ZEROCOPY=1` to opt in; this is useful for benchmarking or integrated targets where the PCIe copy is the bottleneck.

!!! note
    The previous environment variable `EDGEFIRST_DISABLE_CUDA_ZEROCOPY` no longer has any effect.

## Optional: TensorFlow Lite

The TFLite backend handles `.tflite` models and the XNNPACK delegate for accelerated CPU inference, and requires a working TFLite environment on the host. The TFLite C library is also the gateway to the **NXP Neutron** and **VSI** NPU delegates on i.MX targets — those delegates are `.so` files passed to the profiler via `--delegate`. See the [NXP i.MX 95](imx95.md) and [NXP i.MX 8M Plus](imx8mplus.md) guides.

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
