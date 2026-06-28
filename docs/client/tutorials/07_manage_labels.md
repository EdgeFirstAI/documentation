# Tutorial 7: Manage Labels

Reproduce non-contiguous label indices from Coffee Cup on an ephemeral sandbox dataset.

**CLI reference:**

```bash
edgefirst-client dataset ds-145f --labels
```

!!! warning "Sandbox dataset"
    Coffee Cup (`ds-145f`) is read-only. This tutorial creates a temporary dataset to demonstrate `add_labels` and `set_index`.

## Prerequisites

- Complete [Tutorial 6](06_create_annotations.md)
- A writable project

## Steps

### 1. Inspect Coffee Cup label indices

```python
from examples import COFFEE_CUP_DATASET_ID, get_client

client = get_client()
source_labels = client.labels(COFFEE_CUP_DATASET_ID)

for label in source_labels[:8]:
    print(f"  index={label.index} name={label.name!r}")

indices = sorted({int(label.index) for label in source_labels})
if indices != list(range(len(indices))):
    print("  (non-contiguous indices — typical for Coffee Cup on SaaS)")
```

### 2. Create a sandbox dataset with matching indices

```python
from examples import resolve_project

project = resolve_project(client)
dataset_id = client.create_dataset(
    str(project.id), "Example Labels ABC123",
    "DE-2762 examples: label index sandbox",
)

subset = source_labels[:5]
names = [label.name for label in subset]
indices_to_set = [int(label.index) for label in subset]

client.add_labels(dataset_id, names, indices_to_set)
```

### 3. Update a label index

```python
created = client.labels(dataset_id)
target = created[0]
new_index = 9000 + int(target.index)
target.set_index(client, new_index)
client.update_label(target)
```

### 4. Clean up

```python
client.delete_dataset(dataset_id)  # unless SKIP_CLEANUP=1
```

## Source

Full script: [07_manage_labels.py](https://github.com/EdgeFirstAI/client/blob/main/examples/07_manage_labels.py)

---

**Previous:** [Tutorial 6](06_create_annotations.md) · **Back to:** [Tutorial index](index.md)
