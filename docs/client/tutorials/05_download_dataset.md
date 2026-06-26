# Tutorial 5: Download Dataset

Download Coffee Cup images and export YOLO-format label files.

**CLI equivalent:**

```bash
edgefirst-client download-dataset ds-145f --groups val --types image --output ./images/
```

## Prerequisites

- Complete [Tutorial 4](04_polars_dataframe.md)
- `pip install tqdm`

## Steps

### 1. Download images via the Python API

```python
from examples import COFFEE_CUP_DATASET_ID, get_client, progress_bar
from edgefirst_client import AnnotationType, FileType
from tqdm import tqdm

client = get_client()
dataset = client.dataset(COFFEE_CUP_DATASET_ID)
annotation_set_id = client.annotation_sets(dataset.id)[0].id
output = "./coffee_cup_val"

with tqdm(total=0, desc="Downloading") as bar:
    client.download_dataset(
        dataset.id,
        output,
        groups=["val"],
        types=[FileType.Image],
        progress=lambda c, t: progress_bar(c, t, bar),
    )
```

### 2. Write YOLO Darknet labels

The script fetches annotations and writes `.txt` files with normalized center coordinates:

```python
def save_yolo_annotation(path, annotations):
    with open(path, "w", encoding="utf-8") as handle:
        for ann in annotations:
            if ann.box2d is not None:
                box = ann.box2d
                handle.write(
                    f"{ann.label_index} {box.cx} {box.cy} "
                    f"{box.width} {box.height}\n"
                )
```

This produces a Darknet-compatible layout alongside downloaded images.

## Source

Full script: [05_download_dataset.py](https://github.com/EdgeFirstAI/client/blob/main/examples/05_download_dataset.py)

---

**Previous:** [Tutorial 4](04_polars_dataframe.md) · **Next:** [Tutorial 6: Create annotations](06_create_annotations.md)
