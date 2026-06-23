# EdgeFirst Client

The **EdgeFirst Client** (`edgefirst-client`) is the official command-line application and library for [EdgeFirst Studio](../studio/index.md). It provides programmatic and command-line access to datasets, annotations, training sessions, snapshots, and model artifacts.

One install delivers everything:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install edgefirst-client
edgefirst-client login
```

The PyPI wheel bundles the `edgefirst-client` CLI executable and the `edgefirst_client` Python module. No Rust toolchain is required for end users.

## Language bindings

| Binding | Install / docs | Notes |
|---------|----------------|-------|
| **Python** | `pip install edgefirst-client` | Primary target for tutorials and API reference in this manual |
| **Rust** | [crates.io](https://crates.io/crates/edgefirst-client) · [docs.rs](https://docs.rs/edgefirst-client/latest/edgefirst_client/) | Core library; powers the CLI and all bindings |
| **Swift / iOS** | [APPLE.md on GitHub](https://github.com/EdgeFirstAI/client/blob/main/APPLE.md) | UniFFI bindings over the Rust core |
| **Kotlin / Android** | [ANDROID.md on GitHub](https://github.com/EdgeFirstAI/client/blob/main/ANDROID.md) | UniFFI bindings over the Rust core |

## Tutorial dataset

The Python tutorials use the public **Coffee Cup** dataset [`ds-145f`](https://edgefirst.studio/public/datasets/ds-145f/gallery) on SaaS. Read-only examples never modify this dataset. Write examples (tutorials 06 and 07) create ephemeral sandbox datasets in your project.

See the [Coffee Cup dataset zoo](../datasets/coffeecup/index.md) for background on the classes and use cases.

## Reading order

1. **[Command-line interface](cli/index.md)** — install, authenticate, Coffee Cup quick commands, MCAP snapshot workflow
2. **[Dataset import](import.md)** — COCO/LVIS, EdgeFirst Dataset Format, and custom Python imports
3. **[Python tutorials](tutorials/index.md)** — seven hands-on scripts aligned with the [client repository examples](https://github.com/EdgeFirstAI/client/tree/main/examples)
4. **[API reference](api/index.md)** — Python API (generated) and Rust API (docs.rs)

## Related documentation

- [EdgeFirst Dataset Format](../datasets/format/index.md) — Arrow schema used by upload and export commands
- [Studio Snapshots](../studio/snapshots.md) — UI workflow for snapshot create and restore
- [GitHub repository](https://github.com/EdgeFirstAI/client) — source, issues, contributor setup

!!! tip "Included with EdgeFirst Middleware"

    On edge devices, `edgefirst-client` is installed as part of the standard EdgeFirst Middleware installation. Use `edgefirst-client version` to confirm connectivity to EdgeFirst Studio.
