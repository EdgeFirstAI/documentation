# Tiled Inference (SAHI)

Small objects disappear when a high-resolution frame is squeezed into a fixed model input. A 3840-pixel-wide frame letterboxed into a 640×640 input shrinks by a factor of six in each dimension, so a pedestrian that occupied 40 pixels in the original occupies fewer than seven in the tensor the model actually sees — below the size any detector can reliably work with.

**SAHI** (Slicing Aided Hyper Inference) avoids the squeeze. Instead of downscaling the whole frame, the profiler covers it with a grid of overlapping crops, each exactly the model input size, runs inference on every crop at native resolution, then merges the per-tile detections back into full-image coordinates. Objects that were too small to survive the letterboxed downscale are now full-sized within their tile.

The cost is proportional: a frame that plans nine tiles runs nine inferences instead of one.

## Enabling it

=== "CLI"

    ```sh
    edgefirst-profiler validate --model model.onnx --images ./val/ --sahi
    ```

=== "Dashboard"

    Press `t` in the launch dialog before starting the run. The dialog shows the current state as `Tiling: on/off`.

The dashboard toggle only flips tiling on and off. Overlap and convert shape still come from the flags, the model's metadata, or the platform default, as described below.

!!! warning "Detection models only"

    SAHI merges per-tile detections, so it needs a detection head to merge. Running it against a segmentation model fails at startup with a clear error rather than partway through the run, as does running it in timing-only mode where no decoder is configured. A run that also sets `--batch-size` greater than 1 has the batch size forced to 1 with a warning, because per-tile expansion and device batch mode are incompatible.

## Tile overlap

Tiles overlap so that an object landing on a seam still falls wholly inside at least one tile. The ratio resolves in this order, highest priority first:

1. `--sahi-overlap <ratio>`, which must be in the range `[0.0, 1.0)`.
2. The model's own embedded `validation.tiled_overlap` metadata, when present.
3. A fallback of **0.1** — that is, 10%.

Sweeping the overlap trades throughput against seam coverage. A lower overlap plans fewer tiles per image, so the run is faster and there are fewer duplicate detections to merge away; a higher overlap gives a small object at a tile boundary more chances to land whole inside some tile. Before this flag existed the overlap came only from the model's metadata, so comparing settings meant re-exporting the model.

!!! note "The fallback changed from 20% to 10%"

    Models without embedded tiling metadata previously fell back to a 20% overlap. The fallback is now 10%, which is faster and measured at least as accurate in initial testing. A model that carries its own `validation.tiled_overlap` is unaffected either way.

The per-tile confidence threshold resolves the same way: an explicit `--conf-threshold` set to any non-default value wins, otherwise the model's `validation.tiled_score` metadata, otherwise a fallback of 0.05.

## How tiles reach the model

`--sahi-convert <tiled|full>` selects the shape of the conversion work:

| Shape | What it does |
| ----- | ------------ |
| `tiled` | Color-convert each tile individually from the decoded source — N conversions, no intermediate buffer |
| `full` | Convert the whole frame to RGBA once into a staging buffer, then crop N tiles out of it — one conversion, one full-resolution buffer per in-flight frame |

Both shapes always produce **identical detections**. The choice is a throughput and memory trade-off, not a correctness one: `full` pays a fixed per-frame conversion cost that `tiled` avoids, while `tiled` repeats the pixel-format work N times that `full` does once. Which wins is a function of source resolution and of the platform's convert path.

Left unset, the shape resolves per platform. Every platform currently defaults to `tiled`, because no platform has a measured crossover yet.

## Reading the results

Tiling adds per-image columns to the predictions Parquet on every row — zeros on rows from a run that did not tile:

| Column | Meaning |
| ------ | ------- |
| `sahi_tiles` | Tile count for that image (`0` on a non-tiled row) |
| `sahi_overlap` | The overlap ratio the run used |
| `sahi_e2e_ms` | First tile's preprocess start to merge complete, excluding image load and decode |
| `sahi_window_ms` | First tile's preprocess start to the last tile's decode end — the inner tiled window, always at or below `sahi_e2e_ms` |
| `sahi_merge_ms` | Time spent merging the per-tile detections into the frame's result |

A validating run that actually tiled also gets a `sahi` block in `metrics.yaml`, summarizing tile counts, the end-to-end and merge latency per frame, and the mean per-tile preprocess, inference, and postprocess cost across the run. A run that did not tile omits the block rather than writing an all-zero one. The run report additionally records how many tile conversions fell back off the accelerator during the run.

Every run report now states whether tiled inference was used, whether or not it was.

!!! warning "Re-running a session repeats the flags you pass now"

    Naming an existing validation session runs it again with the flags given at that moment — it does not restore the ones the earlier run used. A re-run that leaves out `--sahi` therefore replaces a tiled run's results with results from a run that did not tile, and the two were previously indistinguishable in the report. Pass `--sahi` again, along with any other pipeline options, when you mean to repeat a tiled run.

!!! warning "Re-run tiled runs measured before 1.16.1"

    On hosts without a zero-copy image path — desktop Linux and the container images — sibling tiles of one frame competed for that frame's single decoded image buffer. The losing tile failed, and a single failed tile abandoned its entire frame. Because a frame with no prediction scores as a complete miss, affected runs report **understated accuracy**, and their measured throughput covered fewer frames than requested.

    A run is affected only if it used `--sahi` **and** reported a non-zero skipped-frame count. Such runs should be re-run. Hosts with a zero-copy convert — the embedded targets, and Apple silicon running the `.fp16.onnx` models — were never affected.

## Effect on the pipeline

Under `--sahi` each decoded frame expands into N tile work items, which flow through preprocess, inference, and model decode via the same concurrent stage pools a normal run uses. The stage geometry is unchanged, but the work per frame multiplies, so the per-stage depth settings matter more rather than less. Tiling is not backend-specific: every backend shares the same expansion and merge path.

## See also

- [Pipelining](pipelining.md) — the stage pools the tiles flow through, and the per-stage depth flags.
- [Validation and Metrics](validation.md) — the `metrics.yaml` document the `sahi` block belongs to.
