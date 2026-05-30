# Pipelining

The EdgeFirst Profiler runs a multi-stage measurement pipeline on every frame: image **decode**, **preprocess**, **inference**, **postprocess**, and **output encoding**. Each stage exercises a different part of the system — CPU, host memory, bus transfers, NPU/GPU — and on a typical edge target the stages take substantially different amounts of time. *Pipelining* is the profiler's mechanism for overlapping those stages across frames so the slowest stage sets throughput, instead of the sum of all stage times setting it.

This page explains the conceptual model, the `--pipeline-depth` flag that controls it, and how each supported backend constrains it.

## Pipeline stages

Every frame travels through the same sequence of stages, in order:

| Stage | Hardware | What it does |
| ----- | -------- | ------------ |
| **decode** | CPU (libjpeg / hardware codec) | Read the encoded image file, decode to pixels |
| **preprocess** | CPU + DMA | Resize, color-convert, quantize into the input tensor |
| **inference** | NPU / GPU / CPU | Run the model |
| **postprocess** | CPU | Score-threshold, box decode, NMS, mask decode |
| **output** | CPU + disk | Write predictions to the in-memory Parquet buffer; periodically flush |

The `pycocotools`-style accuracy metrics are computed off-device in EdgeFirst Studio after the run completes — they are not part of the on-device pipeline.

## Sequential execution (`--pipeline-depth 1`)

With `--pipeline-depth 1` the profiler runs each stage on the current frame before starting any stage on the next frame. Each piece of hardware sits idle while the others work:

{{ figure("../assets/pipeline-sequential.png", "Sequential execution — one frame at a time, each stage idle while the others run. The NPU here is the bottleneck at 4.4 ms but only contributes 4.4 / 18.9 = 23% of the wall-clock per frame.") }}

In this mode wall-clock latency equals the sum of all stage times and throughput equals 1 / latency. Sequential mode is the cheapest configuration in memory and the easiest to reason about — every millisecond of wall-clock time is attributable to exactly one stage.

Use sequential mode when:

- You are measuring the **pure inference latency** of a model without confounding pipeline-overlap effects.
- You are diagnosing **which stage is the bottleneck** — sequential timing is the cleanest reference.
- The platform's backend supports only depth 1 (see the table below) — the profiler clamps automatically and prints `Pipeline depth: 1 (sequential)` at run start.

## Pipelined execution (`--pipeline-depth 2`, default)

With depth ≥ 2 multiple frames are in flight through the pipeline at once: while one frame is in inference, the next frame is being preprocessed, the previous frame is being postprocessed, and so on. Every stage can be active simultaneously on different frames, and the slowest stage sets the throughput floor:

{{ figure("../assets/pipeline-overlap.png", "Pipelined execution at depth 2 — three frames overlap in time. Per-frame latency is unchanged (18.9 ms) but throughput is now bottleneck-bound at 4.4 ms/frame (≈227 FPS) instead of 18.9 ms/frame.") }}

The important property: **pipelining does not reduce the latency of any single frame** — that critical path is unchanged. It increases throughput by converting "sum of stage times per frame" into "max of stage times per frame". For deployment profiling on real workloads the throughput number is almost always the more useful one.

Default depth is 2. Higher depths give more overlap headroom (useful when stage durations are uneven) at the cost of memory — each additional slot keeps another in-flight frame's worth of buffers alive.

## Backend limits and auto-clamping

Each inference backend has a maximum pipeline depth determined by how many concurrent inference clients the hardware can serve. The profiler clamps `--pipeline-depth` to that maximum at startup:

| Backend | Default max depth |
| ------- | ----------------: |
| ONNX Runtime (CPU / CUDA / CoreML) | 2 |
| TFLite XNNPACK | 2 |
| TFLite Neutron (i.MX 95) | 2 |
| **TFLite VxDelegate** (i.MX 8M Plus VSI NPU) | **1** |
| Ara-2 (Kinara) | 2 |
| HailoRT (Hailo-8 / 8L) | 2 |
| TensorRT (Jetson) | 2 |

The VSI NPU on the i.MX 8M Plus serves only one inference client at a time, so on that target the profiler runs as sequential regardless of what the user requests.

### Neutron — preprocess and inference serialize

On i.MX 95 with the Neutron delegate the trace viewer shows preprocess and inference slices touching back-to-back rather than overlapping, even though depth 2 is in effect. Decode and postprocess still overlap freely, so throughput still benefits from pipelining — but the preprocess → inference critical path behaves more like depth 1 than depth 2.

## How pipelining appears in the trace viewer

Open the Perfetto trace for any validation session in Studio (the **Profile** tab on the session card). At depth ≥ 2 you will see frames overlapping across the stage tracks — the same picture as the overlap diagram above, but with real timing.

{{ figure("../assets/studio-trace-pipelining.png", "Studio trace viewer at depth 2 — four pipeline stages are active simultaneously, each on a different frame.") }}

The four overlays on the trace above map directly to the pipeline stages, with each box covering a different frame in flight at the same instant:

- **0 — JPEG Decode**: the CPU decoder reading the next image file off disk.
- **1 — OpenGL Pre-processing**: hardware-accelerated resize / color-convert / quantize via `edgefirst-hal`, writing into the input tensor.
- **2 — NPU Inference**: the accelerator running `invoke()` on the already-preprocessed frame from the previous slot.
- **3 — Model Decoder**: postprocessing (box decode, NMS, mask decode) of the frame whose inference just completed.

Reading vertically at any point on the time axis shows what the profiler is doing concurrently — four frames in different stages of completion. Reading horizontally along any one track shows how that stage performs on consecutive frames.

At depth 1, all stage tracks line up sequentially per frame: the next frame's decode slice does not start until the previous frame's last stage finishes.

A common diagnostic flow:

1. Run once at the platform's default depth (likely 2).
2. Compare end-to-end throughput (`Session Report`) against the inference-only mean.
3. If throughput is much lower than `1 / inference_mean`, the bottleneck is on a CPU stage — switch to sequential mode to confirm which one, then look at decode (large images) or postprocess (low confidence threshold producing many candidates).

## CLI

```sh
edgefirst-profiler validate --session-id v-XXXX --pipeline-depth 1
edgefirst-profiler validate --session-id v-XXXX --pipeline-depth 2   # default
edgefirst-profiler validate --session-id v-XXXX --pipeline-depth 4   # auto-clamped to backend max
```

The chosen depth and the clamped mode are printed once at run start:

```text
Pipeline depth: 2 (pipelined)
```

or

```text
Pipeline depth: 1 (sequential)
```

## See also

- [i.MX 8M Plus — Pipeline depth](../installation/imx8mplus.md#pipeline-depth) — the VSI delegate's auto-clamp to depth 1.
- [Validation from Studio — Session Report](../studio/from_studio.md#what-the-run-looks-like) — the per-stage timing breakdown printed to stdout on completion.
