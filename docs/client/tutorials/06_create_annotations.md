# Tutorial 6: Create Annotations

Create an annotated sample in an ephemeral sandbox dataset using `populate_samples`.

**CLI alternative:** `upload-dataset` with an Arrow manifest — see [Dataset import](../import.md).

!!! warning "Sandbox dataset"
    This tutorial writes to a temporary dataset in your project. It never modifies the public Coffee Cup dataset (`ds-145f`). Set `SKIP_CLEANUP=1` to keep the dataset for inspection.

## Prerequisites

- Complete [Tutorial 5](05_download_dataset.md)
- A writable project (not the read-only Sample Project)
- `pip install pillow`

## Steps

### 1. Create a sandbox dataset

```python
from examples import COFFEE_CUP_DATASET_ID, get_client, resolve_project

client = get_client()
project = resolve_project(client)

dataset_id = client.create_dataset(
    str(project.id),
    "Example Populate ABC123",
    "DE-2762 examples: populate_samples sandbox",
)
annotation_set_id = client.create_annotation_set(
    dataset_id, "Default", "Example annotation set",
)
```

### 2. Build a sample with a bounding box

```python
from edgefirst_client import Annotation, Box2d, Sample, SampleFile
from PIL import Image, ImageDraw
from pathlib import Path

# Create a test image with a red circle
image_path = Path("target/example_artifacts/example.png")
# ... draw image and compute normalized bbox (nx, ny, nw, nh) ...

sample = Sample()
sample.set_image_name("example.png")
sample.add_file(SampleFile("image", str(image_path)))

annotation = Annotation()
annotation.set_label("circle")
annotation.set_object_id("circle-1")
annotation.set_box2d(Box2d(nx, ny, nw, nh))
sample.add_annotation(annotation)
```

### 3. Upload with populate_samples

```python
results = client.populate_samples(
    dataset_id,
    annotation_set_id,
    [sample],
    progress=lambda c, t: print(f"  Upload {c}/{t}"),
)
print(f"Uploaded: {results[0].uuid}")
```

### 4. Verify and clean up

```python
fetched = client.samples(dataset_id, annotation_set_id)
# assert round-trip ...

client.delete_dataset(dataset_id)  # unless SKIP_CLEANUP=1
```

Coffee Cup is read as a reference only at the start of the script to show label naming conventions.

## Source

Full script: [06_create_annotations.py](https://github.com/EdgeFirstAI/client/blob/main/examples/06_create_annotations.py)

---

**Previous:** [Tutorial 5](05_download_dataset.md) · **Next:** [Tutorial 7: Manage labels](07_manage_labels.md)
