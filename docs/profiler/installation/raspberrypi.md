# Raspberry Pi 5

The EdgeFirst Profiler runs on the **Raspberry Pi 5** (aarch64). The CPU baseline uses ONNX Runtime; optional accelerators include the **Hailo-8L** M.2 module — the same M.2 form factor Raspberry Pi's AI Kit ships with — accessed through HailoRT.

For a guided platform tour see the [Raspberry Pi Quick Start](../../platforms/quickstart/raspberrypi/index.md). This page covers only the profiler-specific setup.

## Prerequisites

- Raspberry Pi OS 64-bit (Bookworm or later)
- `libonnxruntime.so` (`sudo apt install libonnxruntime` or `pip install onnxruntime`)
- For the Hailo accelerator: HailoRT installed and `libhailort.so` on the loader path — see the [Hailo install guide](hailo.md)

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

## CPU baseline (ONNX Runtime)

The default `--provider cpu` is the most predictable baseline. CPU inference on the RPi5 makes the **capture** and **preprocess** stages a meaningful fraction of total wall time — the Studio trace view will show whether the bottleneck is the model or the pipeline around it.

## Hailo-8 / 8L accelerator

When a Hailo M.2 module is present and HailoRT is installed, the profiler routes compiled `.hef` files through the Hailo backend automatically. The Hailo backend is described in detail on the [Hailo install page](hailo.md), including the `libhailort_profiler` shim that exposes per-context timing.

## Thermal considerations

The RPi5 will throttle under sustained inference if the SoC reaches ~85 °C. The profiler samples thermal-zone temperatures and reports them as system-metric counters; if the temperature climbs steadily during a long run, look at the per-iteration latency in the dashboard — a sudden bump usually corresponds to a thermal throttle event. On the Pi 5 the readout also includes the **RP1** I/O controller's temperature, captured through its `hwmon` sensor alongside the SoC thermal zones.

A small heatsink and fan is enough to keep the SoC out of throttle territory during validation runs.

## Verifying the install

```sh
edgefirst-profiler login
edgefirst-profiler              # opens TUI on F1 Help
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).
