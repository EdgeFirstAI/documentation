# NXP i.MX 95

The EdgeFirst Profiler runs on the **NXP i.MX 95** (aarch64) and uses the **Neutron NPU** for hardware-accelerated inference. The Neutron NPU is exposed to the profiler through the TFLite C library and the NXP `libneutron_delegate.so`.

For a guided platform tour see the [i.MX 95 Quick Start](../../platforms/quickstart/imx95/index.md). This page covers only the profiler-specific setup.

## Prerequisites

- NXP Linux BSP image with the EdgeFirst SDK overlay
- `libtensorflowlite_c.so` (preinstalled in the EdgeFirst image)
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

The profiler picks a TFLite delegate automatically — and you can override it on the validation session if needed. Delegate values:

| Value | Behavior |
| ----- | -------- |
| _(omitted)_ / `auto` | Probe well-known NPU paths (`/usr/lib/libneutron_delegate.so`, `/usr/lib/libvx_delegate.so`); fall back to XNNPACK. |
| `xnnpack` | Explicit XNNPACK CPU delegate. |
| `none` / `cpu` | No delegate — reference kernels. |
| path to `.so` | Load a custom delegate from disk. |

Auto-detection reads `/sys/firmware/devicetree/base/compatible` to identify i.MX 95 and pre-populate the delegate path in the TUI's profile configuration screen.

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
