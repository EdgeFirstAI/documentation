# Validation from EdgeFirst Studio

A validation session is created from the Studio web UI; the session ID is then handed to the profiler on the target device, which downloads the model and dataset, runs the pipeline, and publishes the artifacts back to Studio for accuracy and timing analysis.

## 1. Create a validation session in Studio

From the Model Experiments dashboard, open the training session whose artifact you want to validate, then click **New Validation Session**. Choose **User Managed** as the validation type.

{{ figure("../assets/studio-create-session.png", "EdgeFirst Studio — creating a user-managed validation session") }}

In the dialog, set:

- **Session name** — a human-readable label.
- **Model artifact** — the model file to validate (e.g., `best.onnx`, `best.tflite`, `best.engine`). The list reflects every artifact the training session produced.
- **Dataset / partition** — the dataset and partition the profiler will validate against (typically `validation`).
- **Parameters** — confidence threshold, IoU threshold, NMS top-K, max detections. Defaults match the COCO evaluation protocol; override only if you know why.

Click **Start Session**. Studio creates a session card with a short ID, e.g., `v-1b51`.

{{ figure("../assets/studio-session-id.png", "Validation session card with session ID v-1b51") }}

## 2. Run the profiler on the target

[SSH](../../platforms/networking/ssh.md) into the target board and, if you have not already, [install the profiler](../installation/index.md) and [sign in to Studio](connecting.md).

Run the validation pass:

```sh
edgefirst-profiler validate --session-id v-1b51
```

When invoked with `--session-id` directly from the terminal, the profiler runs **headlessly** — there is no TUI, just a progress-bar-driven report. The same workflow is also available from inside the TUI; see [Validation from the Profiler](from_profiler.md) for that path.

The profiler:

1. Resolves the session against Studio.
2. Downloads the model artifact and dataset partition into the cache (`~/.cache/edgefirst-profiler/` on Linux, `~/Library/Caches/edgefirst-profiler/` on macOS).
3. Runs the full pipeline (decode → preprocess → inference → postprocess → NMS) over every image in the dataset.
4. Writes `predictions.parquet` and `trace.pftrace` into the cached session directory.
5. Uploads both artifacts to Studio and triggers the cloud validator.

Pass `--no-publish` to keep the run local, or `--no-validate` to publish artifacts without triggering the cloud validator (useful when you just want the trace).

If the model already lives on disk and you want to avoid the download:

```sh
edgefirst-profiler validate \
    --session-id v-1b51 \
    --model /path/to/best.onnx
```

### What the run looks like

The output is a sequence of progress bars (model download, inference, prediction upload) followed by a formatted **Session Report** table — pipeline-stage timings, throughput, coverage, and a trace file path:

```text
$ edgefirst-profiler validate --session-id v-1ce9
Fetching validation session v-1ce9...
[00:00:04 ETA: 0s] Downloading model ✓ ████████ 10.87 MB/10.87 MB
...
[00:02:48 ETA: 0s] Inference ████████ 5,000/5,000 (29.6/s)
...
  Pipeline Stage Breakdown
  -----------------------------------------------------------------------
  Stage                Mean   Median      p95      p99      Min      Max
  image_decode        2.7ms    2.6ms    4.2ms    6.0ms    477µs   22.2ms
  preprocess          1.1ms    766µs    2.7ms    8.8ms     89µs   29.2ms
  inference          33.4ms   31.8ms   40.6ms   47.1ms   28.4ms    1.35s
  ...
  End-to-end         39.1ms   37.2ms   48.0ms   55.7ms   32.2ms    1.35s
  Throughput      29.6 FPS

  Trace: ~/.cache/edgefirst-profiler/validation/v-1ce9/trace.pftrace
...
Results published to Studio session v-1ce9
Validator job submitted (job_id: 144e959d-...)
```

The Pipeline Stage Breakdown shows the same data that drives the F4 TUI dashboard, formatted as a static table. The **Trace** path is the local copy of the file that was also uploaded to Studio; the full-resolution trace viewer lives in the validation session card in Studio.

!!! note "System resource samples are Linux-only"
    The **System Resources** rows (CPU / Memory / RSS) are sampled from `/proc` and `/sys` and will report as zero on macOS or Windows hosts.

## 3. Watch the session in Studio

While the profiler runs, the session card in Studio updates with status and progress. When the cloud validator finishes, the card transitions to **Complete** and the **View Validation Charts** button appears.

{{ figure("../assets/studio-session-progress.png", "Validation session card showing progress while the profiler runs and the cloud validator finishes") }}

The metrics dashboard contains the standard `pycocotools` outputs (box mAP@0.5:0.95, AP/AR breakdowns, AP per class) plus instance-segmentation mask metrics when applicable. See [Object Detection Metrics](../../models/validation/metrics/detection/index.md) and [Segmentation Metrics](../../models/validation/metrics/segmentation.md) for the full reference.

{{ figure("../assets/studio-validation-metrics.png", "EdgeFirst Studio — validation metrics dashboard on a completed session: mAP, AP/AR breakdowns, confusion matrices, PR curves") }}

## 4. Open the trace in Studio

Click **Open Trace** on the session card to load the published `trace.pftrace` in Studio's trace viewer. The trace contains:

- Pipeline-stage spans (decode / preprocess / inference / postprocess / NMS).
- Per-operator timing for the backend used (ORT nodes, TFLite ops, Neutron ticks, TensorRT layers, Hailo contexts).
- System-metric counters (CPU%, RSS, temperature).

{{ figure("../assets/studio-trace-viewer.png", "EdgeFirst Studio — trace viewer: pipeline-stage spans, per-operator timing, and system-metric counters") }}

## Tips

- **Override the output directory** with `--output /path/to/results` when running on a board with a small root filesystem.
- **Skip the cloud validator** with `--no-validate` to publish only the timing trace. Useful when iterating on a model where you have already confirmed accuracy.
- **Pre-fill the TUI from a session** by running `edgefirst-profiler --session-id v-1b51` (no `validate` subcommand). The TUI launches and jumps straight to the F4 Profiler screen with the session already resolved.

## Comparing runs

Two completed sessions can be opened side-by-side from the Model Experiments dashboard. See [Validation Sessions](../../studio/models.md#validation-sessions) for the comparison view.
