# macOS

The EdgeFirst Profiler ships a native **arm64** binary for macOS 11 and later. macOS is supported for **ONNX model development** — the vendor accelerator backends (TFLite/Neutron/VSI delegates, Hailo, TensorRT, Ara-2) are Linux-only and either fail to compile or require Linux-only runtime libraries.

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

Pass `--provider coreml` to offload supported subgraphs to the Apple Neural Engine or Metal GPU when running a validation session.

The CoreML EP caches compiled subgraphs at `~/Library/Caches/edgefirst-profiler/coreml/`. The first run of a given model is slower while compilation happens; subsequent runs are warm.

CoreML coverage is partial — operators not supported by the Apple Neural Engine fall back to CPU within the same graph. Studio's trace view shows exactly which ops ran where.

## Verifying the install

```sh
edgefirst-profiler login        # save Studio credentials
edgefirst-profiler              # opens TUI on F1 Help
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).

## What is not supported on macOS

| Backend | Why not |
| ------- | ------- |
| TensorFlow Lite | `libtensorflowlite_c.so` is Linux-only in the EdgeFirst distribution |
| NXP Neutron / VSI delegates | Delegates ship with NXP Linux BSPs only |
| Kinara Ara-2 | `ara2-proxy` daemon is Linux-only |
| Hailo | HailoRT does not ship a macOS build |
| TensorRT | TensorRT is Jetson / Linux + NVIDIA GPU |

If you need to validate against these backends from a Mac, [SSH](../../platforms/networking/ssh.md) into the target board and run the profiler there.
