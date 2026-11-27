# Tiled Inference (SAHI)

Small objects disappear when a high-resolution frame is squeezed into a fixed model input. A 3840-pixel-wide frame letterboxed into a 640×640 input shrinks by a factor of six in each dimension, so a pedestrian that occupied 40 pixels in the original occupies fewer than seven in the tensor the model actually sees — below the size any detector can reliably work with.

**SAHI** (Slicing Aided Hyper Inference) avoids the squeeze. Instead of downscaling the whole frame, the profiler covers it with a grid of overlapping crops, each exactly the model input size, runs inference on every crop at native resolution, then merges the per-tile detections back into full-image coordinates. Objects that were too small to survive the letterboxed downscale are now full-sized within their tile.

The cost is proportional: a frame that plans nine tiles runs nine inferences instead of one.

Tiling works best with a model trained on native-resolution tiles. EdgeFirst Studio trains such models and records how to deploy them in the model's [`tiling` metadata](../../models/metadata.md#tiling); see [Training for Small Objects (SAHI)](../../models/training/sahi.md).

## Enabling it

The profiler decides whether to tile from the model and the `--sahi` flag:

| Model | Without `--sahi` | With `--sahi` |
| ----- | ---------------- | ------------- |
| `tiling.mode: tiled` in its metadata | Tiled | Tiled |
| `tiling.mode: whole_frame`, or no `tiling` section | One inference per frame | Tiled at the model's input size |

A tile-trained model exported for tiled deployment is therefore tiled automatically, whether the run is launched from Studio, from the dashboard or from the command line, and whether the metadata is embedded in the model or in an `edgefirst.json` sidecar. The setup log reports it as `SAHI tiled inference: enabled by the model's tiling metadata (tiled deployment)`. Tiling cannot be turned off for such a model; to deploy its weights in one inference per frame, re-export them whole-frame as described in [Deploying a Tile-Trained Model](../../models/training/sahi.md#deploying-a-tile-trained-model).

`--sahi` tiles any other detection model, including one that was not trained with tiles:

=== "CLI"

    ```sh
    edgefirst-profiler validate --model model.onnx --images ./val/ --sahi
    ```

=== "Dashboard"

    Press `t` in the launch dialog before starting the run. The dialog shows `Tiling: on`, or `Tiling: auto (on for tiled models)` when `--sahi` is not set.

The Studio launch form of the profiler has no tiling option: a Studio run tiles exactly when the selected artifact's metadata declares `tiling.mode: tiled`. The dashboard toggle only sets `--sahi`. Overlap, thresholds and convert shape still come from the flags, the model's metadata, or the platform default, as described below.

!!! warning "Detection models only"

    SAHI merges per-tile detections, so it needs a detection head to merge. Running it against a segmentation model fails at startup with a clear error rather than partway through the run, as does running it in timing-only mode where no decoder is configured. An instance segmentation model can be tiled as a detection model with `--task detect`. A run that tiles with `--batch-size` greater than 1 has the batch size forced to 1 with a warning, because per-tile expansion and device batch mode are incompatible.

## Tile overlap

Tiles overlap so that an object landing on a seam still falls wholly inside at least one tile. The ratio resolves in this order, highest priority first:

1. `--sahi-overlap <ratio>`, which must be in the range `[0.0, 1.0)`.
2. The model's `validation.tiled_overlap` metadata, when present.
3. The model's `tiling.grid.min_overlap` metadata, when present.
4. A fallback of **0.1** — that is, 10%.

Sweeping the overlap trades throughput against seam coverage. A lower overlap plans fewer tiles per image, so the run is faster and there are fewer duplicate detections to merge away; a higher overlap gives a small object at a tile boundary more chances to land whole inside some tile.

The per-tile thresholds resolve the same way:

| Threshold | Resolution order |
| --------- | ---------------- |
| Per-tile confidence | `--conf-threshold` when given, then `validation.tiled_score`, then `tiling.per_tile.score`, then **0.05** |
| Per-tile NMS IoU | `--iou-threshold` when given, then `validation.iou`, then `tiling.per_tile.iou`, then **0.5** |

A metadata value outside its valid range is ignored with a warning. The setup log prints the resolved values as `SAHI tiled inference: overlap=…, per-tile conf=…, per-tile nms iou=…`.

## Grid and merge

The tiles follow the EvenDist grid of the [metadata contract](../../models/metadata.md#grid): tile origins spread evenly across each axis so that every seam overlaps by at least the overlap ratio, with the tile size equal to the model's input size. When the frame is smaller than the tile along an axis, the profiler stretches the crop to the tile.

Each tile's detections are filtered with class-aware NMS, lifted into frame coordinates, and merged across tiles: boxes of the same class are grouped by IoS, the intersection over the smaller box, at 0.5, and the highest-scoring box of each group is kept, up to 300 detections per frame. These are the recommended values of the [merge contract](../../models/metadata.md#merge); the profiler applies them whatever the model's `tiling.merge` and `tiling.per_tile.nms` say, and it does not run the optional `tiling.full_frame` pass.

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

A validating run that actually tiled also gets a `sahi` block in `metrics.yaml`: the image count, the overlap, the tiles per image, the end-to-end, window and merge latency per frame, and the mean per-tile preprocess, inference, and postprocess cost across the run. A run that did not tile omits the block rather than writing an all-zero one. The run report additionally records how many tile conversions fell back off the accelerator during the run.

Every run report now states whether tiled inference was used, whether or not it was.

!!! warning "Re-running a session repeats the flags you pass now"

    Naming an existing validation session runs it again with the flags given at that moment — it does not restore the ones the earlier run used. A model with `tiling.mode: tiled` is tiled on every run, but a model tiled only because of `--sahi` is not: a re-run that leaves out `--sahi` replaces the tiled results with untiled ones. Pass `--sahi` again, along with `--sahi-overlap`, the thresholds and any other pipeline options, when you mean to repeat such a run.

!!! warning "Tiled runs measured with older profiler releases"

    Re-run tiled results measured with older releases before comparing them with new ones:

    - Before 1.16.1, tiled runs on hosts without a zero-copy image path (desktop Linux and the container images) could drop frames, understating accuracy. Affected runs report a non-zero skipped-frame count.
    - Before 1.17.0, tiled throughput was understated and per-tile NMS ran at IoU 0.7.
    - Before 1.18.0, tile-trained models ran with a per-tile score floor of 0.05 instead of their `tiling.per_tile.score`.
    - Before 1.20.0, models whose input normalization is not 0 to 1 scored lower when tiled.

## Effect on the pipeline

When the run tiles, each decoded frame expands into N tile work items, which flow through preprocess, inference, and model decode via the same concurrent stage pools a normal run uses. The stage geometry is unchanged, but the work per frame multiplies, so the per-stage depth settings matter more rather than less. Tiling is not backend-specific: every backend shares the same expansion and merge path.

## See also

- [Training for Small Objects (SAHI)](../../models/training/sahi.md) — training tile-trained models in EdgeFirst Studio and choosing between tiled and whole-frame deployment.
- [Model Metadata: Tiling](../../models/metadata.md#tiling) — the `tiling` section, grid and merge contract.
- [Pipelining](pipelining.md) — the stage pools the tiles flow through, and the per-stage depth flags.
- [Validation and Metrics](validation.md) — the `metrics.yaml` document the `sahi` block belongs to.
