# Python Tutorials

Hands-on tutorials for the `edgefirst_client` Python API. Each tutorial maps to a numbered script in the [EdgeFirst Client repository](https://github.com/EdgeFirstAI/client/tree/main/examples). Paired Jupyter notebooks (`.ipynb`) cover the same material.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install edgefirst-client tqdm pillow jupyter pandas pyarrow

edgefirst-client login
git clone https://github.com/EdgeFirstAI/client.git
cd client
python examples/01_authentication.py
```

The library comes from the PyPI wheel in your virtual environment, not from the cloned repository source tree.

## Authentication

```bash
edgefirst-client login
python examples/01_authentication.py
```

`login` prompts for username and password interactively. For automation, use `STUDIO_TOKEN` or `STUDIO_USERNAME` / `STUDIO_PASSWORD` environment variables.

## Environment variables

| Variable | Purpose |
|----------|---------|
| `STUDIO_TOKEN` | Direct authentication token |
| `STUDIO_USERNAME` / `STUDIO_PASSWORD` | Login credentials |
| `STUDIO_SERVER` | Server instance (`saas`, `test`, `stage`; default `saas`) |
| `EXAMPLES_PROJECT_NAME` | Project for sandbox writes (06, 07); default: first project |
| `SKIP_CLEANUP` | Set to `1` to keep ephemeral datasets after tutorials 06/07 |

## Tutorial index

| Tutorial | CLI commands | Python API |
|----------|--------------|------------|
| [1. Authentication](01_authentication.md) | `login`, `logout`, `token` | `Client()`, `FileTokenStorage`, `verify_token` |
| [2. Explore dataset](02_explore_dataset.md) | `dataset ds-145f --annotation-sets --labels --groups` | `dataset`, `annotation_sets`, `labels`, `groups` |
| [3. Fetch annotations](03_fetch_annotations.md) | `download-annotations` | `samples`, `annotations` |
| [4. Polars dataframe](04_polars_dataframe.md) | `download-annotations` → `.arrow` | `samples_dataframe`, `polars.read_ipc` |
| [5. Download dataset](05_download_dataset.md) | `download-dataset` | `download_dataset`, YOLO export |
| [6. Create annotations](06_create_annotations.md) | `upload-dataset` (reference) | `populate_samples` |
| [7. Manage labels](07_manage_labels.md) | `dataset ds-145f --labels` | `add_labels`, `label.set_index` |

All read workflows use the public **Coffee Cup** dataset [`ds-145f`](https://edgefirst.studio/public/datasets/ds-145f/gallery). Write workflows (06, 07) create ephemeral sandbox datasets only.

## IDE support

Inline help in VS Code and Cursor comes from `edgefirst_client.pyi` stubs shipped inside the PyPI wheel. See the [Python API reference](../api/python.md).

## Contributor setup

To build from source with `maturin develop`, see [CONTRIBUTING.md](https://github.com/EdgeFirstAI/client/blob/main/CONTRIBUTING.md) in the client repository.
