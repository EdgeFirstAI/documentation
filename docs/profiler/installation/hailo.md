# Hailo-8 / Hailo-8L

The EdgeFirst Profiler runs compiled **Hailo Executable Format** (`.hef`) models on any Linux host with HailoRT installed and a Hailo accelerator present. Common targets include the **Raspberry Pi 5 AI Kit** (Hailo-8L via M.2), M.2 carriers on x86 hosts, and PCIe Hailo-8 cards.

## Prerequisites

- HailoRT 4.x runtime installed (`libhailort.so` on the loader path)
- Hailo PCIe driver (`hailo_pci`) and udev rules — installed by the HailoRT Debian packages

```sh
hailortcli scan   # should print the device, e.g. "Hailo-8L on PCIe slot ..."
```

If `hailortcli scan` reports no devices, fix the HailoRT install before running the profiler — the profiler depends on the same `libhailort.so` symbols.

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

## Backend routing

The Hailo backend dlopens `libhailort.so` at runtime. As with every other backend, a missing library produces a clear error message naming the file — no `dlopen` traceback.

`.hef` is an edge-only format: there is no cloud machine with a Hailo device attached, so the `dispatch` command rejects a `.hef` artifact up front rather than starting a cloud run that cannot execute. Profile `.hef` models on the target hardware itself.

## Inference depth and batching

On the Raspberry Pi 5 with a Hailo-8L, the measured auto inference depth is **4**, matching the HailoRT async scheduler's driver-reported depth.

The Hailo-only `--batch-size` flag sets how many frames go into each `run_async` batch (default 1, per-frame submission). Device batching is still under development: a value above 1 is accepted with a warning, but the run currently proceeds per-frame, which is the optimized low-latency default. Once batching lands, the intended guidance is to set the batch size to the camera count in a multi-camera deployment — HailoRT overlaps host-to-device transfer, compute, and device-to-host transfer within a batch, raising throughput at close to zero added latency. Non-Hailo backends ignore the flag.

## Per-context timing (`libhailort_profiler.so`)

For per-context lifecycle timing — `configure`, `activate`, `infer`, `deactivate` — the profiler can load an optional Hailo profiler shim, `libhailort_profiler.so`, that wraps HailoRT lifecycle calls. The shim ships in the EdgeFirst SDK and is loaded automatically when present in `/usr/local/lib` or `/usr/lib`.

The Hailo per-context timing appears alongside the rest of the trace in the Studio trace view. Without the shim the profiler still reports end-to-end inference timing, only the lifecycle breakdown is unavailable.

## Multi-device hosts

`hailortcli scan` lists every device on the host. The profiler currently selects the first available device. For multi-device benchmarking, schedule the validation sessions serially or pin each run to a specific device through HailoRT's environment variables.

## Verifying the install

```sh
edgefirst-profiler login
edgefirst-profiler              # opens TUI on F1 Help
```

If a validation session fails with "device busy", another process holds the Hailo device. Stop the holder (`hailortcli`, another `edgefirst-profiler`, an application using HailoRT) and rerun.
