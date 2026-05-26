# On Target Validation

User-managed validation runs the model on a real edge device and publishes the per-image predictions plus a detailed performance trace back to EdgeFirst Studio for accuracy and timing analysis. It is the right choice when you need to know how the model **actually behaves** on the hardware it will deploy to — not on a cloud instance.

The on-target tool for this workflow is the **[EdgeFirst Profiler](../../../profiler/index.md)**.

For an alternative cloud-only flow, see [On Cloud Validation](managed.md). The managed flow provisions an EC2 instance and runs the model there — fast to set up, but the latency numbers will not reflect the deployment target.

## Choose your path

Both paths produce the same Studio validation session and the same set of accuracy charts. The difference is **where the validation session is created**:

| If you... | Read |
|---|---|
| Want to create the session in the Studio web UI, then run the profiler on the device | [Validation from Studio](../../../profiler/studio/from_studio.md) |
| Want to browse training sessions inside the profiler TUI and create the session in place | [Validation from the Profiler](../../../profiler/studio/from_profiler.md) |

## Installation and connection

| Topic | Read |
|---|---|
| Install the profiler on the target board | [Installation guides](../../../profiler/installation/index.md) (per target) |
| Sign in to EdgeFirst Studio | [Connecting to EdgeFirst Studio](../../../profiler/studio/connecting.md) |
| Five-minute first profiling run | [Quick Start](../../../profiler/quickstart.md) |

## What the profiler produces

Every validation run publishes two artifacts to the Studio session:

- **`predictions.parquet`** — per-image predictions in EdgeFirst Dataset Format. EdgeFirst Studio consumes them to compute mAP and mIoU.
- **`trace.pftrace`** — a detailed timing trace covering the entire pipeline (decode → preprocess → inference → postprocess → NMS), per-operator backend timing (ORT nodes, TFLite ops, Neutron ticks, TensorRT layers, Hailo contexts), and system-metric counters (CPU, memory, temperature).

The trace is rendered in Studio's trace viewer directly from the session card.

## Comparing runs

Two completed sessions can be opened side-by-side from the Model Experiments dashboard. See [Validation Sessions](../../../studio/models.md#validation-sessions) for the comparison view.

## Next steps

Once you have validated your model, see [model deployment](../../deployment/studio.md) for the deployment paths to EdgeFirst Studio, the [PC](../../deployment/pc/index.md), [embedded targets](../../deployment/launcher.md), the [Maivin](../../deployment/maivin.md), and the [Raivin](../../deployment/2d_raivin.md).
