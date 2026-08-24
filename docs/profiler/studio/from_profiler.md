# Validation from the Profiler

The profiler's **F2 Studio** screen exposes the same project / experiment / training-session / artifact hierarchy you see in the EdgeFirst Studio web UI, plus the actions needed to create a validation session in place — without round-tripping through the browser. This flow is the fastest path from "I have a board running the profiler" to "I have published validation results in Studio".

## When to use this flow

- The model you want to validate already lives in a Studio training session.
- You are working on the target board and want to avoid switching to a desktop browser.
- You want to spin up several quick validation runs (different artifacts, different confidence thresholds) without creating each session by hand.

For the classic flow — where the session is created in Studio first — see [Validation from Studio](from_studio.md).

## Walkthrough

### 1. Open the F2 Studio screen

Launch the TUI, press **F2**. If you are not signed in, the login form appears first — see [Connecting to EdgeFirst Studio](connecting.md).

Once signed in the screen shows the **Projects** explorer.

{{ figure("../assets/tui-studio-explorer.png", "F2 Studio explorer — projects, experiments, training sessions, artifacts") }}

### 2. Navigate to a training session

Use `↑` / `↓` to move and `Enter` to drill down:

```text
Projects  →  Experiments  →  Training Sessions  →  Artifacts
```

Each level renders the same metadata you see in the Studio web UI: project owner, last update, experiment status, training-session metrics. The breadcrumb across the top tracks where you are.

{{ figure("../assets/tui-launch-validate.png", "F2 Studio explorer — confirming a validate action against an artifact") }}

`Backspace` (or `Esc`) goes one level up. Quit-on-Esc is disabled inside the explorer so you cannot accidentally lose your place.

### 3. Pick an artifact and an action

The artifact list shows only recognized model formats — ONNX, TFLite, DVM, Hailo, and TensorRT — hiding label files, archives, and other non-model artifacts a training session produces. When you select an artifact (e.g., `best.onnx`, `best.tflite`, `best.engine`), an action menu pops up:

| Action | Behavior |
| ------ | -------- |
| **Validate** | Create a new validation session bound to this artifact and the training session's dataset, then jump to the F4 Profiler screen to run it. |
| **Live** | _(reserved)_ Selecting it reports "Live profiling is not yet supported. Coming in a future release." |

Choosing **Validate** opens an inline configuration panel: dataset partition, confidence threshold, IoU threshold, top-K, max detections. Sensible defaults are pre-filled from the training session.

!!! warning "Validation sessions need a writable project"
    Creating a validation session requires **write access** to the Studio project. The profiler cannot create a session against the read-only public **Sample Project**; when this happens, the dashboard's dialog explains the two ways forward: choose **Continue profiling-only** to run the model locally and see its on-device performance without publishing, or — to publish results — [copy the dataset](../../getting_started/copy_dataset.md) into a project you own (and add your model), then create the training and validation session there. (On a read-only or public project, a `--training-session` run falls back to local-only mode automatically — see [CLI equivalent](#cli-equivalent) below.)

### 4. Confirm and run

Submit the configuration. The profiler:

1. Calls Studio to create the validation session (returns a `v-XXXX` ID).
2. Downloads any artifacts that are not already cached.
3. Switches to the F4 Profiler screen and starts the run automatically.

Before the dashboard starts, the profiler downloads any dataset frames that are not already cached. The TUI shows a progress panel during the download:

{{ figure("../assets/tui-downloading-dataset.png", "F2 Studio explorer — dataset download progress before validation starts") }}

Once the dataset is local, the status bar shows the new session ID and the F4 dashboard streams iteration-level latency, system metrics, and per-stage timing as the pipeline executes:

{{ figure("../assets/tui-profiler.png", "F4 dashboard during a profiler-initiated validation session") }}

### 5. Publishing

Publish is automatic for sessions created from the F2 flow — on completion the run computes the accuracy metrics on the device and uploads the full artifact set to Studio: `predictions.parquet`, `trace.pftrace`, `metrics.yaml`, `platform.yaml`, and the chart JSONs. There is no separate cloud-validator step. A fresh run preserves the session ID in its output directory (`./results/<v-XXXX>/`) so you can re-publish or re-run from the CLI later if you need to; a re-validation of an existing session writes its results beside the session's own cached files instead, keeping one run's artifacts in one place (an explicit `--output` overrides either location).

To skip the upload (e.g., when investigating a one-off timing question and the accuracy numbers are not interesting), use the configuration panel's **Publish: off** toggle before starting the run.

## CLI equivalent

The TUI flow is convenient, but the same effect is reachable from the CLI when you already know the artifact you want:

```sh
edgefirst-profiler validate --training-session t-abc123
```

Without `--model`, this lists the training session's available model artifacts and exits — the same listing `--list-models` produces explicitly. Re-run with `--model <artifact-name>` to select one; the profiler then creates the validation session itself, downloads the artifact, runs the pipeline, and publishes the results:

```sh
edgefirst-profiler validate \
    --training-session t-abc123 \
    --model best.tflite
```

With `--training-session`, `--model` names a Studio artifact to download, not a local file path. `--training-session` produces a brand-new validation session every time it is run; pass `--session-id v-XXXX` instead to re-publish to an existing session.

To profile locally **without** creating a Studio session — useful for a quick one-off timing check — pass `--no-publish`:

```sh
edgefirst-profiler validate --training-session t-abc123 --no-publish
```

The run writes `predictions.parquet` and `trace.pftrace` to disk and skips session creation and publishing entirely. This is the CLI equivalent of the F2 panel's **Publish: off** toggle. On a read-only or public project — where the profiler cannot create a session — a `--training-session` run falls back to this local-only behavior automatically.

## Publishing results produced elsewhere

The `publish` command separates profiling from publishing: point it at files a run already produced — `--predictions <parquet>`, plus optionally `--metrics <file>`, `--charts-dir <dir>`, and `--trace <file>` — and it creates a validation session (`--training-session`, `--artifact`, `--name`) and uploads them. Measure on the target device, then publish from whatever machine has the files and Studio credentials:

```sh
edgefirst-profiler publish \
    --training-session t-abc123 \
    --artifact best.onnx \
    --name "imx95-npu-run" \
    --predictions results/predictions.parquet \
    --metrics results/metrics.yaml \
    --trace results/trace.pftrace
```

Passing `--session v-XXXX` instead publishes into an existing session, preserving its ID — useful for backfilling metrics and charts onto a session whose predictions were already uploaded, without disturbing them.

Omitting `--metrics` uploads the predictions and leaves the session awaiting accuracy, which any host can fill in afterwards with `validate --predictions <parquet> --session-id <id>`. This two-step route is the intended path for segmentation runs on memory-constrained devices, where evaluating mask accuracy on-device can run out of memory even though the device writes the predictions file fine.

To launch a run on Studio-managed cloud hardware instead of your own device, see the `dispatch` command in [Cloud Runs](cloud.md).

## When the run completes

The completion summary in the TUI lists the new session ID, the headline latency numbers, and the local trace path. For a published run, the popup also shows the session's Studio link, widening to fit long URLs rather than truncating them; press **c** while the popup is showing to copy it to the system clipboard (this works on Linux desktops too, where the copied text now persists so it can be pasted elsewhere). A headless CLI run prints the same link as `View details:`, rendered as a real clickable hyperlink in terminals that support it. Press **Enter** to dismiss and return to the dashboard. Switch back to F2 to drill into the just-created session and confirm Studio received the artifacts; from there the Studio web UI is the canonical place for charts, comparisons, and the trace viewer.
