# NXP i.MX 8M Plus

The EdgeFirst Profiler runs on the **NXP i.MX 8M Plus** (aarch64) and uses the **VeriSilicon (VSI) NPU** for hardware-accelerated inference, exposed through the TFLite C library and the `libvx_delegate.so` shared object.

For a guided platform tour see the [i.MX 8M Plus Quick Start](../../platforms/quickstart/imx8mplus/index.md). This page covers only the profiler-specific setup.

## Prerequisites

- NXP Linux BSP image with the EdgeFirst SDK overlay
- `libtensorflow-lite.so` (preinstalled; override the search path with `TFLITE_LIBRARY_PATH`)
- `libvx_delegate.so` (preinstalled)

The i.MX 8M Plus VSI NPU runs standard TFLite models — no model rewrite is required, unlike the i.MX 95 Neutron NPU. Quantize the model to `int8` for best performance; floating-point graphs fall back to CPU.

## Install the profiler

=== "Python (pip)"

    ```sh
    pip install edgefirst-profiler
    ```

=== "Platform installer"

    ```sh
    curl -fsSL https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.sh | bash
    ```

Confirm:

```sh
edgefirst-profiler --version
```

## Delegate selection

When launching the profiler with a TFLite model on i.MX 8M Plus, a **delegate selection dialog** appears in the TUI, letting users pick VX or CPU/XNNPACK explicitly. For headless use, the `--delegate` CLI flag bypasses the dialog; the `auto` value in the table below still applies in that case.

| Value | Behavior on i.MX 8M Plus |
| ----- | ------------------------ |
| _(omitted)_ / `auto` | Auto-detects i.MX 8M Plus from device-tree compatible string and loads `libvx_delegate.so`. |
| `xnnpack` | CPU baseline. |
| `none` / `cpu` | Reference kernels only. |
| `gpu` | LiteRT GPU (CL/GL) delegate when present — experimental. |
| `qnn` / `qnn-htp`, `qnn-gpu`, `qnn-dsp` | Qualcomm QNN delegate (Android targets; requires a build with the `qnn` feature and the device's Qualcomm libraries) — experimental. |
| path to `.so` | Custom delegate. |

Unrecognized delegate names (a typo like `xnnpak`) are rejected at parse time with the valid options listed, rather than being treated as a file path. The Qualcomm backend previously offered as `qnn-cpu` is now `qnn-dsp` — there is no CPU backend in the QNN delegate, and `qnn-dsp` names the real legacy Hexagon DSP backend.

## Inference depth

The VSI delegate supports **only one** in-flight inference at a time. The profiler detects this and clamps `--inference-depth` down to a single inference slot — CPU stages (capture, postprocess, encode) still overlap with the single inference, but two inferences cannot run concurrently on the NPU. NPU delegates are exempt from the core-aware concurrency default that CPU TFLite runs get: the clamp to one slot applies regardless of the host's core count.

The Studio trace view makes this serialization visible — back-to-back invoke slices touch but never overlap.

See the [Pipelining](../concepts/pipelining.md) concept page for the full backend table, the sequential vs. pipelined mental model, and how each mode appears in the trace viewer.

## Container image

!!! tip "Run from a container instead"
    The `imx8mp` tag of the [profiler container images](docker.md) bundles the VX delegate, the Vivante OpenVX userspace stack, and the TFLite runtime, so no local install is needed. Map the NPU with `--device /dev/galcore` plus the board's DMA-heap node (`ls /dev/dma_heap/`), or run with `--privileged` to grant both in one flag.

## Verifying the install

```sh
edgefirst-profiler login
edgefirst-profiler              # F4 Profiler should show /usr/lib/libvx_delegate.so auto-filled
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).
