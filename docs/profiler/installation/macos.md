# macOS

The EdgeFirst Profiler ships a native **arm64** binary for macOS 11 and later. macOS is supported for **ONNX model development** — the vendor accelerator backends (TFLite/Neutron/VSI delegates, Hailo, TensorRT, Ara240) are Linux-only and either fail to compile or require Linux-only runtime libraries.

The macOS-specific accelerator path is the **CoreML execution provider** through ONNX Runtime, which offloads supported subgraphs to the Apple Neural Engine or the Metal GPU.

## Install

=== "Python (pip)"

    ```sh
    pip install edgefirst-profiler
    ```

=== "Platform installer"

    ```sh
    curl -fsSL https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.sh | bash
    ```

    The installer drops the binary into `~/.local/bin` (default) or `/usr/local/bin` (run as root). If the install path is not on your `PATH`, the script prints the exact line to add to your shell profile.

Confirm:

```sh
edgefirst-profiler --version
```

## ONNX Runtime — required

ONNX Runtime is the default and only fully-supported backend on macOS. Install it via Homebrew:

```sh
brew install onnxruntime
```

Homebrew installs `libonnxruntime.dylib` into `/opt/homebrew/lib`. That path is not on macOS's default dyld search path, but the profiler scans it explicitly — you do **not** need to set `ORT_DYLIB_PATH` or `DYLD_LIBRARY_PATH`.

If you maintain a non-Homebrew install, set `ORT_DYLIB_PATH` to the absolute path of your `libonnxruntime.dylib`.

## CoreML execution provider

The bare `--provider coreml` flag is no longer accepted. Pass one of the three explicit compute-unit options instead (the old flag prints an error listing the replacements):

| Flag | Compute unit | Notes |
| ---- | ------------ | ----- |
| `--provider coreml-cpu` | CoreML CPU kernels | Good baseline; no GPU or ANE scheduling overhead |
| `--provider coreml-gpu` | Metal Performance Shaders, CPU fallback | Best throughput for GPU-heavy models. Auto inference depth: **3**, the only CoreML provider with a pinned platform default (measured knee — ~427 FPS at depth 2, ~476 FPS at depth 3, ~466 FPS at depth 4) |
| `--provider coreml-ane` | Apple Neural Engine, CPU fallback only | Uses the generic auto inference depth (2) — the ANE serializes device work internally, so deeper pipelines mainly buy preprocess overlap |

**In the TUI:** the launch-time dialog presents a navigable list of providers — CPU, CoreML CPU, CoreML GPU, CoreML ANE — instead of the previous fixed two-key prompt. Navigate with ↑/↓ and press Enter to confirm, or press the number key shown next to the row.

The `--provider qnn-htp` option also parses on macOS, but it is Android-only — on any non-Android host the run falls back to the CPU provider and says so.

The CoreML model is compiled fresh each run; this one-time compile happens during session setup and does not affect the measured inference timings.

CoreML coverage is partial — operators not supported by the selected compute unit fall back to CPU within the same graph. Studio's trace view shows exactly which ops ran where; the per-operation device-placement diagnostics are no longer printed to the terminal.

## Verifying the install

```sh
edgefirst-profiler login        # save Studio credentials
edgefirst-profiler              # opens TUI on F1 Help
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).

## What is not supported on macOS

| Backend | Why not |
| ------- | ------- |
| TensorFlow Lite | `libtensorflow-lite.so` is Linux-only in the EdgeFirst distribution |
| NXP Neutron / VSI delegates | Delegates ship with NXP Linux BSPs only |
| Kinara Ara240 | `ara2-proxy` daemon is Linux-only |
| Hailo | HailoRT does not ship a macOS build |
| TensorRT | TensorRT is Jetson / Linux + NVIDIA GPU |

If you need to validate against these backends from a Mac, [SSH](../../platforms/networking/ssh.md) into the target board and run the profiler there.
