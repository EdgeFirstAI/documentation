# Quick Start

This guide walks you from "nothing installed" to a published validation session in roughly five minutes. The profiler is always operated against an EdgeFirst Studio session.

## 1. Install the profiler

The recommended convenience path is `pip`. The wheel ships the same native binary the platform installers deliver, and pulls in the few Python-side helpers needed for end-to-end workflows. Platform installers are provided for environments where Python is not available.

=== "Python (pip)"

    ```sh
    pip install edgefirst-profiler
    ```

=== "Linux / macOS"

    ```sh
    curl -fsSL https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.sh | bash
    ```

=== "Windows (PowerShell)"

    ```powershell
    irm https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.ps1 | iex
    ```

Confirm the install:

```sh
edgefirst-profiler --version
```

For per-target details (NPU delegates, runtime libraries, hardware-specific quirks) see the [installation guides](installation/index.md).

## 2. Sign in to EdgeFirst Studio

```sh
edgefirst-profiler login
```

The interactive prompt asks for **server**, **username**, and **password**. The credentials are saved to `~/.config/edgefirststudio/token` and refresh automatically while you are using the profiler. For headless / CI flows, see [Connecting to EdgeFirst Studio](studio/connecting.md).

## 3. Launch the TUI

Running `edgefirst-profiler` with no subcommand launches the interactive terminal UI. Any explicit subcommand — `validate`, `login`, `publish`, `report` — bypasses the TUI and runs headlessly.

```sh
edgefirst-profiler
```

The TUI opens on the **F1 Help** screen, which lists the keybindings and the four screens available to you:

{{ figure("assets/tui-help-screen.png", "EdgeFirst Profiler — F1 Help screen, shown on launch") }}

Four function keys switch between screens:

| Key | Screen | Purpose |
|-----|--------|---------|
| F1 | Help | Keybindings and a short orientation — the landing screen |
| F2 | Studio | Sign in to EdgeFirst Studio, browse projects, run validation sessions |
| F3 | Files | Browse the local filesystem |
| F4 | Profiler | Configure and run a profiling pass with a live dashboard |

Press `q` to quit (disabled while typing into form fields). `Ctrl-C` always quits.

## 4. Run a validation session

The profiler is operated against a Studio validation session. Both paths produce the same Studio session card and the same set of accuracy charts.

### Path A — start from the profiler (recommended for new users)

Press **F2** to switch to the Studio screen. If you are not signed in, the login form appears first.

{{ figure("assets/tui-studio-login.png", "F2 Studio — login form") }}

Once signed in, navigate the explorer:

```
Projects  →  Experiments  →  Training Sessions  →  Artifacts
```

{{ figure("assets/tui-studio-explorer.png", "F2 Studio — explorer drilling into a training session") }}

Select an artifact and choose **Validate**. The profiler creates a new validation session in Studio, downloads anything missing, jumps to **F4 Profiler**, and starts the run.

{{ figure("assets/tui-launch-validate.png", "F2 Studio — confirming Validate against a model artifact") }}

The F4 dashboard streams iteration-level latency, system metrics, and per-stage timings while the run executes:

{{ figure("assets/tui-profiler.png", "EdgeFirst Profiler — F4 dashboard during a run") }}

When the run finishes, a completion summary shows the headline numbers and the path to the trace file. The artifacts upload to Studio automatically and the cloud validator is triggered.

```
╔═ Profiling Complete ═════════════════════════════╗
║                                                  ║
║  Iterations: 100                                 ║
║                                                  ║
║  Mean:  43.76 ms                                 ║
║  P95:   44.12 ms                                 ║
║  P99:   44.51 ms                                 ║
║  Min:   43.21 ms  Max: 45.03 ms                  ║
║                                                  ║
║  Trace: ./results/trace.pftrace                  ║
║                                                  ║
║  [Enter] Dismiss                                 ║
╚══════════════════════════════════════════════════╝
```

For the full walkthrough see [Validation from the Profiler](studio/from_profiler.md).

### Path B — start from Studio

Create a user-managed validation session in the Studio web UI ([instructions](studio/from_studio.md)). Make a note of the session ID, then on the target:

```sh
edgefirst-profiler validate --session-id v-1ce9
```

The profiler runs headlessly, prints progress bars for download/inference/upload, emits a formatted **Session Report** to stdout, and publishes results to Studio when the run completes.

## 5. View the results in Studio

Both paths land you at the same place: the validation session card in EdgeFirst Studio. The card shows progress while the cloud validator runs, then surfaces the accuracy charts and trace viewer when it completes.

{{ figure("assets/studio-trace-viewer.png", "EdgeFirst Studio — trace viewer on a completed validation session, showing pipeline stages and per-operator timing") }}

See [Object Detection Metrics](../models/validation/metrics/detection/index.md) and [Segmentation Metrics](../models/validation/metrics/segmentation.md) for the metrics reference.

## Next steps

- **Profile on edge hardware.** The convenience install path works on desktop hosts and most target boards. Embedded targets with NPU/GPU acceleration have a few extra knobs — pick your target from the [installation guides](installation/index.md).
- **Pick the right Studio path.** [Validation from Studio](studio/from_studio.md) (session created in the web UI) versus [Validation from the Profiler](studio/from_profiler.md) (session created from the TUI).
- **Connect to a different Studio.** See [Connecting to EdgeFirst Studio](studio/connecting.md) for `test` / `stage` / `saas` server selection and headless credential handling.
