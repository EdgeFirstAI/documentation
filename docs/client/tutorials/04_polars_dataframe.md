# Tutorial 4: Polars Dataframe

Analyze Coffee Cup annotations with Polars — via CLI Arrow export or the native `samples_dataframe` API.

**CLI equivalent:**

```bash
edgefirst-client download-annotations <as-id> coffee_cup.arrow --groups val
```

## Prerequisites

- Complete [Tutorial 3](03_fetch_annotations.md)
- `pip install polars pandas pyarrow` (pandas optional)

## Steps

### 1. Export annotations with the CLI (optional)

```python
import subprocess
from pathlib import Path

arrow_path = Path("coffee_cup.arrow")
subprocess.run([
    "edgefirst-client", "download-annotations",
    "<as-id>", str(arrow_path), "--groups", "val",
], check=True)
```

Set `SKIP_CLI_DOWNLOAD=1` to skip this step if the Arrow file already exists.

### 2. Load Arrow in Polars

```python
import polars as pl

df_cli = pl.read_ipc(arrow_path)
print(f"CLI Arrow: {df_cli.shape[0]} rows")
if "label" in df_cli.columns:
    counts = df_cli.group_by("label").len().sort("len", descending=True)
    print(counts.head(5))
```

### 3. Use the native API

```python
from examples import COFFEE_CUP_DATASET_ID, get_client

client = get_client()
dataset = client.dataset(COFFEE_CUP_DATASET_ID)
annotation_set_id = client.annotation_sets(dataset.id)[0].id

df_api = client.samples_dataframe(
    dataset.id, annotation_set_id, ["val"], [], None,
)
print(f"API samples_dataframe: {df_api.shape[0]} rows")
```

See the [EdgeFirst Dataset Format schema](../../datasets/format/schema.md) for column definitions.

## Source

Full script: [04_polars_dataframe.py](https://github.com/EdgeFirstAI/client/blob/main/examples/04_polars_dataframe.py)

---

**Previous:** [Tutorial 3](03_fetch_annotations.md) · **Next:** [Tutorial 5: Download dataset](05_download_dataset.md)
