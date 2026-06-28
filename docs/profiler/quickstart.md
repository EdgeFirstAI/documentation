# Quick Start

This guide walks you from "nothing installed" to a published validation session in roughly fifteen minutes. The profiler is always operated against an EdgeFirst Studio session.

## 1. If you haven't already, log in to EdgeFirst Studio

1. Go to {{ studio_link("EdgeFirst Studio") }}
2. If you do not have an account, {{ studio_link("create a free account", "signup") }} on the landing page
3. Log in with your username and password

## 2. Create your project in EdgeFirst Studio

{% include-markdown "discrete/studio/create_project.md" heading-offset=0 %}

## 3. Create an Ultralytics training session

!!! warning "Use your own project"
    Profiling must be run against a project you own. Running a profiling or validation session on the **Sample Project** — or any public, read-only project — will fail with an error. Make sure you created your own project in [Step 2](#2-create-your-project-in-edgefirst-studio) before continuing.

{% include-markdown "discrete/models/train_ultralytics.md" heading-offset=0 %}

## 4. Install the profiler

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

## 5. Sign in to EdgeFirst Studio (profiler CLI)

```sh
edgefirst-profiler login
```

The interactive prompt asks for **server**, **username**, and **password**. The credentials are saved to `~/.config/edgefirststudio/token` and refresh automatically while you are using the profiler. For headless / CI flows, see [Connecting to EdgeFirst Studio](studio/connecting.md).

## 6. Launch the TUI

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

## 7. Run a validation session

The profiler is operated against a Studio validation session. Both paths produce the same Studio session card and the same set of accuracy charts.

!!! warning "Validation sessions need a writable project"
    Creating a validation session requires **write access** to the Studio project. You cannot validate against the read-only public **Sample Project** directly — first [copy its dataset](../getting_started/copy_dataset.md) into a project you own (and add your model), then create the training and validation session there.

### Path A — start from the profiler (recommended for new users)

Press **F2** to switch to the Studio screen. If you are not signed in, the login form appears first.

{{ figure("assets/tui-studio-login.png", "F2 Studio — login form") }}

Once signed in, navigate the explorer:

```text
Projects  →  Experiments  →  Training Sessions  →  Artifacts
```

{{ figure("assets/tui-studio-explorer.png", "F2 Studio — explorer drilling into a training session") }}

Each artifact is prefixed with a colored dot indicating whether it can be deployed on the current host:

| Indicator | Status | Meaning | Example artifacts |
|-----------|--------|---------|-------------------|
| 🟢 Green | Deployable | Format recognized and all runtime requirements met on this host. | `.onnx` (Generic ONNX), `.tflite` (Generic TFLite) |
| 🟠 Orange | Conditions not confirmed | Known deployable format for a specific target, but the required hardware, runtime, or accelerator was not detected. | `.hef` (Hailo-8L runtime absent), `.dvm` (NXP Ara240 not present), `.engine` (no CUDA host), `.imx95.tflite` (different SoC) |
| 🔴 Red | Not deployable | Supporting file, archive, or unrecognized format — not a model the profiler can run directly. | `labels.txt`, `_saved_model.zip`, `.tensorrt.zip` |

Select an artifact and choose **Validate**. The profiler creates a new validation session in Studio, downloads anything missing, jumps to **F4 Profiler**, and starts the run.

{{ figure("assets/tui-launch-validate.png", "F2 Studio — confirming Validate against a model artifact") }}

Before the run starts, a **launch dialog** appears. For ONNX models it first asks which execution provider to use (CPU, CUDA if available, or CoreML on macOS). Then it shows four per-stage depth sliders — Capture, Preprocess, Inference, and Postprocess — each defaulting to **Auto**, which resolves to the value measured fastest for your model, runtime, and host. Press `Enter` to accept the Auto defaults and start immediately, or `c` to customize the depths. The dialog warns if a platform constraint (such as the i.MX 95 Neutron single-bind delegate) holds a stage to a single thread.

The F4 dashboard streams iteration-level latency, system metrics, and per-stage timings while the run executes:

{{ figure("assets/tui-profiler.png", "EdgeFirst Profiler — F4 dashboard during a run") }}

The system-metrics row includes live **power draw** and on-board **temperatures** wherever the hardware exposes a sensor. The profiler shows a power meter only for the rails it can actually read — the CPU, GPU, Neural Engine, and DRAM rails on Apple Silicon, and the real board rails on a Linux device with a supported power monitor (for example an NVIDIA Jetson's board-input rail and its per-component breakdown). On a target with no power sensor, no power meters are shown — rather than a row pinned at 0 W — and the session report notes that power is unavailable. Temperatures are read from the platform's thermal zones and `hwmon` sensors, so the readout reflects what each board actually measures.

When the run finishes, a completion summary shows the headline numbers and the path to the trace file. The artifacts upload to Studio automatically and the cloud validator is triggered.

```text
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

## 8. View the results in Studio

Both paths land you at the same place: the validation session card in EdgeFirst Studio. The card shows progress while the cloud validator runs, then surfaces the accuracy charts and trace viewer when it completes.

{{ figure("assets/studio-trace-viewer.png", "EdgeFirst Studio — trace viewer on a completed validation session, showing pipeline stages and per-operator timing") }}

See [Object Detection Metrics](../models/validation/metrics/detection/index.md) and [Segmentation Metrics](../models/validation/metrics/segmentation.md) for the metrics reference.

## Next steps

- **Profile on edge hardware.** The convenience install path works on desktop hosts and most target boards. Embedded targets with NPU/GPU acceleration have a few extra knobs — pick your target from the [installation guides](installation/index.md).
- **Pick the right Studio path.** [Validation from Studio](studio/from_studio.md) (session created in the web UI) versus [Validation from the Profiler](studio/from_profiler.md) (session created from the TUI).
- **Connect to a different Studio.** See [Connecting to EdgeFirst Studio](studio/connecting.md) for `test` / `stage` / `saas` server selection and headless credential handling.
