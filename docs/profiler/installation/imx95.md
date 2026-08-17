# NXP i.MX 95

The EdgeFirst Profiler runs on the **NXP i.MX 95** (aarch64) and uses the **Neutron NPU** for hardware-accelerated inference. The Neutron NPU is exposed to the profiler through the TFLite C library and the NXP `libneutron_delegate.so`.

For a guided platform tour see the [i.MX 95 Quick Start](../../platforms/quickstart/imx95/index.md). This page covers only the profiler-specific setup.

## Prerequisites

- NXP Linux BSP image with the EdgeFirst SDK overlay
- `libtensorflow-lite.so` (preinstalled in the EdgeFirst image; override the search path with `TFLITE_LIBRARY_PATH`)
- `libneutron_delegate.so` (preinstalled in the EdgeFirst image)
- `neutron-converter` toolchain (cross-host, used to compile models before deployment)

The Neutron NPU only executes models that have been **passed through the Neutron Converter** — the converter rewrites a standard TFLite model into a graph the Neutron NPU can run. See the [Neutron Converter](../../models/conversion/neutron.md) guide.

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

When launching the profiler with a TFLite model on i.MX 95, a **delegate selection dialog** appears in the TUI. The dialog works like the ONNX execution-provider modal — the user picks Neutron, VX, or CPU/XNNPACK explicitly rather than relying on auto-detection. Models that require the Neutron delegate (detected from the model file) skip the general dialog and go straight to a Neutron-specific picker. For headless use, the `--delegate` CLI flag bypasses the dialog entirely.

| Value | Behavior |
| ----- | -------- |
| _(omitted)_ / `auto` | Probe well-known NPU paths (`/usr/lib/libneutron_delegate.so`, `/usr/lib/libvx_delegate.so`); fall back to XNNPACK. |
| `xnnpack` | Explicit XNNPACK CPU delegate. |
| `none` / `cpu` | No delegate — reference kernels. |
| `gpu` | LiteRT GPU (CL/GL) delegate when present — experimental. |
| `qnn` / `qnn-htp`, `qnn-gpu`, `qnn-dsp` | Qualcomm QNN delegate (Android targets; requires a build with the `qnn` feature and the device's Qualcomm libraries) — experimental. |
| path to `.so` | Load a custom delegate from disk. |

Unrecognized delegate names (a typo like `xnnpak`) are rejected at parse time with the valid options listed, rather than being treated as a file path. The Qualcomm backend previously offered as `qnn-cpu` is now `qnn-dsp` — there is no CPU backend in the QNN delegate, and `qnn-dsp` names the real legacy Hexagon DSP backend.

Auto-detection reads `/sys/firmware/devicetree/base/compatible` to identify i.MX 95 and pre-populate the delegate path in the TUI's profile configuration screen.

## Neutron inference modes

The Neutron delegate supports two inference modes. The profiler detects which mode is available automatically — profiling works correctly in both.

**DMA-BUF zero-copy mode** (default when the kernel zero-copy patch is present, or `NEUTRON_ENABLE_ZERO_COPY=1`)

The delegate binds a single DMA-BUF tensor shared between the CPU and the NPU. Because the input is bound once and cannot be rebound per frame, one inference slot runs at a time and pre-processing collapses to a single worker that serializes with inference. This serialization is a property of single-bind delegates — Neutron in zero-copy mode, and the i.MX 8M Plus VxDelegate — not of the pipeline: everywhere else, pre-processing fans out in parallel. This is the original Neutron inference mode.

**CPU-staging mode** (activated automatically when the kernel zero-copy patch is absent, or `NEUTRON_ENABLE_ZERO_COPY=0`)

No DMA-BUF binding is used. Up to 4 independent inference slots run in parallel, giving significantly higher throughput. The profiler sets the inference depth to 4 automatically in this mode. Measured throughput on i.MX 95 Pro running YOLOv5n at 640×640: ~73 FPS at depth 1, ~97 FPS at depth 4. These are sweep-measured overrides for the i.MX 95, and they take precedence over the generic core-count-based inference depth defaults introduced for CPU runtimes — the i.MX 95 keeps its measured tuning.

!!! note "Fallback from zero-copy"

    Previously, running a Neutron model on a board without the kernel zero-copy patch caused a crash on the first frame. The profiler now detects the missing patch and falls back to CPU-staging automatically.

## Container image

!!! tip "Run from a container instead"
    The `imx95` tag of the [profiler container images](docker.md) bundles the Neutron delegate and driver from the eIQ Neutron SDK 3.0.1 along with the TFLite runtime, so no local install is needed. Map the NPU with `--device /dev/neutron0` plus the board's DMA-heap node (`ls /dev/dma_heap/`), or run with `--privileged` to grant both in one flag. The matching Neutron firmware must still be installed on the **host** — the kernel loads it from the host filesystem, not from inside the container.

## Per-tick Neutron profiling

When both conditions below are met, the profiler reports **per-tick** timing — every NPU kernel (`Conv2DDenseTT`, `AddTT`, …) appears as its own slice in the Studio trace view:

1. The model was compiled with **`enable_profiling: true`** in the [Neutron Converter](../../models/conversion/neutron.md).
2. The target runs **Neutron drivers ≥ 3.0.1** (tested on 3.0.1), shipped as part of the [eIQ Neutron SDK](https://www.nxp.com/design/design-center/software/eiq-ai-development-environment/eiq-toolkit-for-end-to-end-model-development-and-deployment:EIQ-TOOLKIT).

!!! note "Older 2.x drivers"

    The profiler remains fully functional with Neutron drivers 2.x — inference timing, pipeline-stage breakdown, and accuracy metrics all work normally. Only the **per-operation NPU timing** (op-level profiling of the Neutron graph) is unavailable without 3.0.1+ drivers.

To get human-readable kernel names rather than opaque IDs, pass the Neutron converter statistics file produced when the model was compiled:

```sh
neutron-converter --dump-statistics-file yolov8n_neutron.statistics ...
```

Provide that file to the validation session via `--neutron-statistics yolov8n_neutron.statistics`. Without the statistics file the timing is still captured — only the labels become opaque IDs.

## Verifying the install

```sh
edgefirst-profiler login
edgefirst-profiler              # opens TUI on F1 Help; F4 auto-populates the delegate path
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).
