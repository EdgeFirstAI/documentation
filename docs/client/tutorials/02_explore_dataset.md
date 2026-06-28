# Tutorial 2: Explore Dataset

Explore metadata for the public Coffee Cup dataset (`ds-145f`).

**CLI equivalent:**

```bash
edgefirst-client dataset ds-145f --annotation-sets --labels --groups
```

Gallery: [edgefirst.studio/public/datasets/ds-145f/gallery](https://edgefirst.studio/public/datasets/ds-145f/gallery)

## Prerequisites

- Complete [Tutorial 1](01_authentication.md)

## Steps

### 1. Load the dataset

```python
from examples import COFFEE_CUP_DATASET_ID, COFFEE_CUP_GALLERY_URL, get_client

client = get_client()
client.verify_token()

dataset = client.dataset(COFFEE_CUP_DATASET_ID)
print(f"Dataset: {dataset.name} ({dataset.id})")
print(f"Gallery: {COFFEE_CUP_GALLERY_URL}")
```

### 2. List annotation sets, labels, and groups

```python
annotation_sets = client.annotation_sets(dataset.id)
for annset in annotation_sets:
    print(f"  [{annset.id}] {annset.name}")

labels = client.labels(dataset.id)
for label in labels[:10]:
    print(f"  index={label.index} name={label.name!r}")

groups = client.groups(dataset.id)
for group in groups:
    print(f"  {group.name} (id={group.id})")
```

### 3. Count annotated samples

```python
from edgefirst_client import AnnotationType, FileType

count = client.samples_count(
    dataset.id,
    annotation_sets[0].id,
    annotation_types=[AnnotationType.Box2d],
    groups=[],
    types=[FileType.Image],
)
print(f"Sample count (box2d): {count.total}")
```

## Source

Full script: [02_explore_dataset.py](https://github.com/EdgeFirstAI/client/blob/main/examples/02_explore_dataset.py)

---

**Previous:** [Tutorial 1](01_authentication.md) · **Next:** [Tutorial 3: Fetch annotations](03_fetch_annotations.md)
