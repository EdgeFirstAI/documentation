# Tutorial 3: Fetch Annotations

Fetch annotated samples from Coffee Cup using the object-oriented `samples` API and the flat `annotations` API.

**CLI equivalent:**

```bash
edgefirst-client download-annotations <as-id> out.json --groups train,val
```

## Prerequisites

- Complete [Tutorial 2](02_explore_dataset.md)
- `pip install tqdm`

## Steps

### 1. Resolve the annotation set

```python
from examples import COFFEE_CUP_DATASET_ID, get_client, progress_bar
from edgefirst_client import AnnotationType, FileType
from tqdm import tqdm

client = get_client()
dataset = client.dataset(COFFEE_CUP_DATASET_ID)
annotation_set_id = client.annotation_sets(dataset.id)[0].id
```

### 2. Fetch samples with progress

```python
groups = ["train", "val"]
with tqdm(total=0, desc="Fetching samples") as bar:
    samples = client.samples(
        dataset_id=dataset.id,
        annotation_set_id=annotation_set_id,
        annotation_types=[AnnotationType.Box2d],
        groups=groups,
        types=[FileType.Image],
        progress=lambda c, t: progress_bar(c, t, bar),
    )

print(f"Fetched {len(samples)} samples")
annotated = [s for s in samples if s.annotations]
print(f"Samples with annotations: {len(annotated)}")
```

### 3. Inspect the first annotated sample

```python
if annotated:
    sample = annotated[0]
    for ann in sample.annotations[:3]:
        box = ann.box2d
        if box:
            print(f"  label={ann.label!r} cx={box.cx:.4f} cy={box.cy:.4f}")
```

### 4. Alternative: flat annotations API

```python
with tqdm(total=0, desc="Flat annotations") as bar:
    flat = client.annotations(
        annotation_set_id=annotation_set_id,
        groups=["val"],
        annotation_types=[AnnotationType.Box2d],
        progress=lambda c, t: progress_bar(c, t, bar),
    )
print(f"Flat annotations (val): {len(flat)} rows")
```

## Source

Full script: [03_fetch_annotations.py](https://github.com/EdgeFirstAI/client/blob/main/examples/03_fetch_annotations.py)

---

**Previous:** [Tutorial 2](02_explore_dataset.md) · **Next:** [Tutorial 4: Polars dataframe](04_polars_dataframe.md)
