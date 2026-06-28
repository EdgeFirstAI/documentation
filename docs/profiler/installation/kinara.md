# Kinara Ara240

The EdgeFirst Profiler runs **Kinara Ara240** DVM models on Linux (x86_64 or aarch64) hosts that have the Kinara stack installed. The Ara240 inference path is daemon-based: the profiler talks to the `ara2-proxy` daemon over its IPC channel, the daemon owns the device and runs inference.

## Prerequisites

- Kinara Ara240 hardware (PCIe card or USB module)
- Kinara SDK with the `ara2-proxy` daemon and Kinara drivers
- `ara2-proxy` running as a system service (started automatically by the Kinara SDK installer in most cases)

```sh
systemctl status ara2-proxy    # should be active (running)
```

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

`.dvm` files are detected automatically and routed to the Ara240 backend when a validation session runs. The Kinara daemon owns the device, so the profiler reports **device-side** sub-phase timing (`input_copy`, `invoke`, `output_copy`) along with the host-measured `roundtrip`. When the device-reported sub-phases do not sum to `roundtrip`, the gap reveals host-side overhead — IPC latency between the profiler and `ara2-proxy`, or driver setup time.

The Ara240 backend keeps up to **8 inference slots** in flight concurrently; this is the auto-selected default and is the setting at which the profiler approaches the NPU throughput ceiling. On i.MX 95 — where the Ara240 is accessed over PCIe from the Cortex-A core — the ceiling is model-specific: approximately **194 FPS for YOLOv5n** and **249 FPS for YOLOv8n** at 640×640 input resolution.

The Perfetto trace now exposes per-frame NPU tracks: `npu.h2d` (PCIe host-to-device transfer), `npu.compute` (NPU execution), and `npu.d2h` (PCIe device-to-host transfer). This replaces the previous aggregate timing and lets you see precisely where each inference frame spends its time.

## Model metadata

DVM files use a **zip trailer** to embed decoder configuration and class labels. When the trailer is missing or the model was produced by a toolchain that does not write it, the profiler runs in timing-only mode and prints a note on stderr.

## Verifying the install

```sh
edgefirst-profiler login
edgefirst-profiler              # opens TUI on F1 Help
```

If the `ara2-proxy` daemon is not running when a session starts, the profiler returns an error pointing at the daemon — not a connection-refused traceback. Restart the daemon:

```sh
sudo systemctl restart ara2-proxy
```

Then run a validation session — see [Validation from Studio](../studio/from_studio.md) or [Validation from the Profiler](../studio/from_profiler.md).
