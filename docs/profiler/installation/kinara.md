# Kinara Ara-2

The EdgeFirst Profiler runs **Kinara Ara-2** DVM models on Linux (x86_64 or aarch64) hosts that have the Kinara stack installed. The Ara-2 inference path is daemon-based: the profiler talks to the `ara2-proxy` daemon over its IPC channel, the daemon owns the device and runs inference.

## Prerequisites

- Kinara Ara-2 hardware (PCIe card or USB module)
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

`.dvm` files are detected automatically and routed to the Ara-2 backend when a validation session runs. The Kinara daemon owns the device, so the profiler reports **device-side** sub-phase timing (`input_copy`, `invoke`, `output_copy`) along with the host-measured `roundtrip`. When the device-reported sub-phases do not sum to `roundtrip`, the gap reveals host-side overhead — IPC latency between the profiler and `ara2-proxy`, or driver setup time.

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
