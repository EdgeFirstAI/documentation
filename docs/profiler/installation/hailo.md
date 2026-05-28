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
