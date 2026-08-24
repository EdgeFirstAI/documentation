# Container Images

Pre-built EdgeFirst Profiler images are published to `ghcr.io/edgefirstai/profiler-cli` on the GitHub Container Registry with every release. Each variant bundles the profiler binary plus a matching inference runtime, so no Python environment, installer script, or runtime library install is needed on the host — pull the image and run.

## Tag matrix

| Tag | Architectures | Contents | When to use |
| --- | ------------- | -------- | ----------- |
| `core` | amd64 + arm64 | Binary only, no inference runtime | Base image (`FROM`) for bringing your own runtime |
| `onnx` | amd64 + arm64 | CPU ONNX Runtime | CPU ONNX inference, CI, development |
| `tflite` | amd64 + arm64 | TFLite C++ runtime (`libtensorflow-lite.so`) | CPU TFLite inference |
| `imx95` | arm64 only | `tflite` plus the Neutron delegate and driver (eIQ SDK 3.0.1) | NXP i.MX 95 Neutron NPU |
| `imx8mp` | arm64 only | `tflite` plus the VX delegate and Vivante OpenVX stack | NXP i.MX 8M Plus VSI NPU |
| `cuda` | amd64 + arm64 | GPU ONNX Runtime with CUDA 12.6 / cuDNN 9 | NVIDIA discrete GPU (amd64) or Jetson (arm64) |
| `latest` | amd64 + arm64 | Alias for `onnx` | **CPU only** |

These are moving aliases that track the newest release. To pin a release, use the immutable `VERSION-VARIANT` form (for example `1.16.1-onnx`); the bare `VERSION` tag pins that release's CPU `onnx` image.

!!! warning "`onnx` / `latest` is CPU-only"
    The default image runs inference on the CPU ONNX Runtime execution provider. Throughput measured on the `onnx` or `latest` tag does not reflect GPU performance — GPU measurement requires the `cuda` tag.

## Persistent state and file ownership

The container keeps its persistent state — the download cache and the EdgeFirst Studio auth token — under `/config`. Mount a volume there so logins and cached datasets survive across runs; the examples below use a named volume called `edgefirst`.

The images run as **root by default**, so NPU/GPU device access and real-time scheduling work without extra flags. Results written to a bind-mounted working directory are reassigned to that directory's owner automatically, so they come out owned by your user; override the target owner with `--output-owner <uid:gid|username>` or the `EDGEFIRST_OUTPUT_OWNER` environment variable. To run unprivileged instead, pass `--user "$(id -u):$(id -g)"`.

## Running the dashboard

The default invocation launches the interactive terminal dashboard. The `-it` flags are required for the TUI:

```sh
docker run -it --rm -v edgefirst:/config ghcr.io/edgefirstai/profiler-cli:onnx
```

Press `F2` to connect to EdgeFirst Studio and pull models and validation sessions — the login token is stored in the named volume and reused across runs.

## Running a validation from the command line

To profile local files non-interactively, bind-mount a working directory as `/workdir` and pass paths relative to it:

```sh
docker run --rm \
  -v edgefirst:/config -v "$PWD":/workdir \
  ghcr.io/edgefirstai/profiler-cli:onnx \
  validate --model /workdir/model.onnx --images /workdir/val --output /workdir/results
```

The same form works with every variant — add the device or GPU flags for your target from the table below.

## Per-target device flags

| Target | Tag | Extra `docker run` flags |
| ------ | --- | ------------------------ |
| NVIDIA discrete GPU (amd64) | `cuda` | `--gpus all` (requires `nvidia-container-toolkit` on the host) |
| NVIDIA Jetson / Orin (arm64) | `cuda` | `--runtime nvidia` (the L4T container stack does not support `--gpus`) |
| NXP i.MX 95 Neutron NPU | `imx95` | `--device /dev/neutron0` plus the board's DMA-heap node (`ls /dev/dma_heap/`), or `--privileged` |
| NXP i.MX 8M Plus VSI NPU | `imx8mp` | `--device /dev/galcore` plus the board's DMA-heap node, or `--privileged` |

On the NXP targets, `--privileged` is the simplest and currently recommended way to grant the NPU device, the DMA heaps, and the GPU used for decode and preprocessing in one flag. The i.MX 95 image bundles the Neutron delegate and driver, but the matching Neutron firmware must be installed on the **host** — the kernel loads it from the host filesystem, not from inside the container.

Real-time inference scheduling needs `CAP_SYS_NICE`: it is included in `--privileged`, or grant it alone with `--cap-add SYS_NICE`. Without it the run still works at normal scheduling priority.

See the per-target pages for the runtime details behind each variant: [Linux](linux.md), [NVIDIA Jetson Orin](jetson_orin.md), [NXP i.MX 95](imx95.md), and [NXP i.MX 8M Plus](imx8mplus.md).
