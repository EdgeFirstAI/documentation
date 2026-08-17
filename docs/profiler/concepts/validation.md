# Validation and Metrics

The profiler does not just produce predictions for something else to score. It computes the accuracy metrics itself, on the machine that ran the model — full COCO detection and segmentation results with per-class breakdowns — and writes them to disk alongside the predictions and the trace. EdgeFirst Studio is where those results are published, compared, and browsed, but it is not where they are calculated, and a run does not need Studio at all to produce them.

That has two practical consequences. A validation run works completely offline, against a local model, a local directory of images, and a local ground-truth file. And the numbers are available on the target, in the console and in `metrics.yaml`, the moment the run finishes.

## When accuracy is computed

The `--validation` flag decides whether and when scoring happens:

| Mode | Behavior |
| ---- | -------- |
| `after` | Score once profiling completes, reusing the predictions already written to disk. Adds no overhead to the profiled run. |
| `during` | Score concurrently with profiling, so the cost of validation itself is captured in the trace. |
| `off` | Skip on-agent scoring. Predictions still publish (unless `--no-publish`); accuracy is left to be computed elsewhere. |

Left unset, the mode resolves automatically: `after` when a ground-truth source is available, otherwise `off`. Most runs never need to set it.

!!! note "`--no-validate` no longer exists"

    Earlier releases accepted a `--no-validate` flag. It has been replaced by `--validation off`, and passing the old name now fails with an unknown-argument error. Update any scripts that still use it.

Validation and publishing are independent. `--validation off` still uploads the predictions; `--no-publish` keeps everything local but still scores the run when ground truth is available.

## Where ground truth comes from

Any one of these supplies it:

- **A validation session** (`--session-id`) — the session's dataset provides the annotations.
- **A training session** (`--training-session`) — its own dataset validation split is used.
- **A local annotations file** (`--ground-truth <file>`) — an EdgeFirst ground-truth file in `.arrow`, `.ipc`, or `.parquet` form, which bypasses the Studio dataset download entirely.

`--annotation-set <id>` overrides which annotation set is fetched when the ground truth comes from Studio; by default the session's configured set is used.

Passing `--images <dir>` alongside a session deliberately turns validation off. A custom image directory carries no ground truth of its own, so scoring it against the session's annotations would produce meaningless accuracy numbers. The profiler prints a warning explaining the forced setting and profiles the images anyway.

A fully offline accuracy run therefore looks like this:

```sh
edgefirst-profiler validate \
    --model ./best.onnx \
    --images ./val2017/ \
    --ground-truth ./annotations.arrow \
    --output ./results
```

## What a validated run produces

Every run writes `metrics.yaml` next to the trace, and prints the same figures as a readable console summary — the detection and segmentation metric tables, per-threshold precision, recall and F1, any dropped-row warnings, and the validation wall-clock.

The document has up to six top-level sections, each omitted when it does not apply:

| Section | Contents |
| ------- | -------- |
| `detection` | The 12 standard COCO summary metrics for boxes — `AP`, `AP50`, `AP75`, `APs`, `APm`, `APl`, `AR1`, `AR10`, `AR100`, `ARs`, `ARm`, `ARl` |
| `segmentation` | The same 12 metrics computed over masks, for a segmentation model |
| `deployment` | A classification breakdown at a range of score thresholds, with the true-positive IoU, image count, and ignored-crowd count |
| `sahi` | Tile counts and tiled-inference timing, present only when the run actually tiled — see [Tiled Inference (SAHI)](sahi.md) |
| `system` | CPU utilization, memory, power rails, and temperatures, each summarized over the run |
| `timing` | Measured throughput and per-stage timing — see below |

Per-class rows attach to one task only, the primary one: segmentation when the model produced masks, detection otherwise. Each row carries that class's `AP`, `AP50`, `AP75`, and `AR100`.

### The `timing` section

`timing` has up to four blocks. `timing.inline` holds the per-stage summary and the bottleneck figures, including `capture_bound`, `compute_bottleneck_stage`, and `compute_bottleneck_fps`. `timing.runtime` records the pipeline configuration the run resolved. `timing.concurrency` holds the measured worker occupancy, queue statistics, and the per-stage reservation verdicts. `timing.trace` holds what was recovered from the run's own `trace.pftrace`: the completed frame count, an FPS summary, per-stage duration statistics, and the model's top kernels by total execution time.

Both `timing.concurrency` and the capture-bound figures are explained in [Pipelining](pipelining.md).

### Charts

A published run also carries a full chart set, produced by the profiler and uploaded with everything else: accuracy charts (per-class precision, recall and F1, PR curves, mAP breakdowns), the deployment classification breakdown, inline timing and throughput charts, device execution-timing charts from the trace (per-stage overlap, inference sub-phase breakdowns, per-operation timing), system-telemetry charts for CPU, memory, power and temperature, and the two concurrency charts — a queue-depth timeline and per-stage worker occupancy.

!!! note "Memory on constrained devices"

    Scoring streams the predictions and annotations rather than loading both tables into memory. Segmentation validation in particular now peaks at roughly 1.2–1.6 GiB on a full COCO-scale run, where it previously needed several gigabytes, so scoring can finish on memory-constrained devices without a separate host step.

## Re-scoring a run without re-running the model

Accuracy can be recomputed from a predictions file at any time — after a ground-truth correction, or while iterating on a model converter — without touching the model or the images:

```sh
# Re-score a local predictions file, fully offline
edgefirst-profiler validate \
    --predictions ./results/predictions.parquet \
    --ground-truth ./annotations.arrow \
    --trace ./results/trace.pftrace
```

`--predictions <file>` skips model loading and image processing entirely. `--trace <file>` hands the reprocess the original run's trace, so the recomputed results carry the run's real measured timing — per-stage execution windows, worker concurrency, and throughput on a measured basis — plus the full device-timing and system-telemetry chart set. Without a trace, a reprocess that has no session to fetch one from has no measurement source at all, and throughput falls back to a configured estimate. Pointing `--trace` at a path that does not exist is an error rather than a silent fallback.

To re-score a session whose predictions were already uploaded, from a machine that never held the original file:

```sh
edgefirst-profiler validate --session-id v-XXXX --reprocess
```

`--reprocess` fetches the session's own predictions parquet from Studio instead of requiring a local copy, and fetches its trace too. A local `--trace` takes precedence over that download. Note that a bare `--session-id` without `--reprocess` is unchanged and still runs the full validation, downloading the model and dataset and re-running inference.

A re-validation writes its results beside the session rather than into the default output directory; an explicit `--output` still overrides that.

## Reporting on a trace after the fact

`report` summarizes any run the profiler recorded, from its trace alone:

```sh
edgefirst-profiler report ./results/trace.pftrace
```

It prints the pipeline configuration, frame count, end-to-end latency, FPS, steady-state per-stage timing, top kernels, system telemetry, queue statistics, and the worker-concurrency verdict table. Pass `--json` or `--yaml` for a machine-readable version instead — the same `system` and `timing` sections as the standard metrics document, so a trace report is directly comparable with any validation run's published metrics.

## Measuring and publishing separately

`publish` uploads a finished result set to Studio without re-running anything, so the machine that measured and the machine with Studio credentials do not have to be the same one:

```sh
edgefirst-profiler publish \
    --training-session t-XXXX \
    --artifact best.onnx \
    --name "Orin Nano FP16" \
    --predictions ./results/predictions.parquet \
    --metrics ./results/metrics.yaml \
    --charts-dir ./results/charts \
    --trace ./results/trace.pftrace
```

Passing `--session <id>` instead publishes into an existing session, preserving its `v-XXXX` id, so metrics and charts can be backfilled onto an already-published session without disturbing its predictions.

### The two-step route for segmentation on small devices

Omitting `--metrics` uploads the predictions and leaves the session awaiting accuracy. A host with more memory then fills it in:

```sh
# On the device — profile and publish predictions only
edgefirst-profiler validate --model best.onnx --images ./val/ --validation off
edgefirst-profiler publish --training-session t-XXXX --artifact best.onnx \
    --name "…" --predictions ./results/predictions.parquet

# On a host — score the parquet and complete the session
edgefirst-profiler validate --predictions ./predictions.parquet --session-id v-XXXX
```

This is what segmentation runs need on memory-constrained devices, where evaluating mask accuracy on-device can still exhaust the available memory even though the device writes the predictions file without trouble.

For scripting, `publish` prints one status line per outcome — `session-created <id>` before any upload begins, then `session-published <id> <url>`, `session-uploaded <id> <url>` when only predictions were sent, or `session-denied <dataset-id>` when the Studio project is read-only — so a caller can tell a read-only project apart from a mistyped flag.

## See also

- [Pipelining](pipelining.md) — the measured pipeline behind the `timing` section, and how to read the bottleneck figures.
- [Tiled Inference (SAHI)](sahi.md) — the `sahi` metrics block and what tiling does to accuracy.
- [Object Detection Metrics](../../models/validation/metrics/detection/index.md) and [Segmentation Metrics](../../models/validation/metrics/segmentation.md) — what the metrics themselves mean.
- [Connecting to EdgeFirst Studio](../studio/connecting.md) — credentials for the publishing steps, including token-based authentication for CI.
