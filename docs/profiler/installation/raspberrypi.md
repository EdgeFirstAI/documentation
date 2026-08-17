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

## Real-time scheduling and sudo

Real-time inference scheduling (`SCHED_FIFO`) requires elevated privileges on the Raspberry Pi, and it gives lower and more consistent inter-inference latency. The TUI asks **before validation starts** whether to run under `sudo` or to continue at normal priority; passwordless sudo skips the password prompt. If a run fails partway on a privilege error instead — for example NPU or GPU zero-copy access being denied — the dashboard explains that elevated privileges are required and offers to re-run under `sudo`.

Either way, trace and prediction files are handed back to your user afterward so the EdgeFirst Studio upload still works; the explicit `--output-owner <uid:gid|username>` flag (or the `EDGEFIRST_OUTPUT_OWNER` environment variable) overrides the target owner for scripted or root workflows. Each run also records its privilege diagnostics in `profiler.log` — the user it ran as, whether it was elevated via sudo, and whether inference obtained real-time scheduling priority or fell back to normal — so you can confirm from the log alone that an elevated retry took effect.

## Hailo-8 / 8L accelerator

When a Hailo M.2 module is present and HailoRT is installed, the profiler routes compiled `.hef` files through the Hailo backend automatically. The Hailo backend is described in detail on the [Hailo install page](hailo.md), including the `libhailort_profiler` shim that exposes per-context timing.

On the RPi5 with a Hailo-8L, the measured auto inference depth is **4**, matching the HailoRT async scheduler's driver-reported depth. The Hailo-only `--batch-size` flag exists but device batching is still under development: a value above 1 is accepted with a warning and the run proceeds per-frame, which is the optimized low-latency default.

## Thermal considerations

The RPi5 will throttle under sustained inference if the SoC reaches ~85 °C. The profiler samples thermal-zone temperatures and reports them as system-metric counters; if the temperature climbs steadily during a long run, look at the per-iteration latency in the dashboard — a sudden bump usually corresponds to a thermal throttle event. On the Pi 5 the readout also includes the **RP1** I/O controller's temperature, captured through its `hwmon` sensor alongside the SoC thermal zones.

A small heatsink and fan is enough to keep the SoC out of throttle territory during validation runs.

## Verifying the install

```sh
edgefirst-profiler login
edgefirst-profiler              # opens TUI on F1 Help
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).
