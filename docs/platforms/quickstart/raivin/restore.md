# Restore MCAP

!!! tip "Annotation Source for a Fusion Model"
    A fusion model needs 3D boxes.  When you set the restore fields below, choose an auto-generated annotation source that includes 3D boxes so the dataset is annotated as it is restored.

{% include-markdown "discrete/datasets/restore_mcap.md" end="If the snapshot was restored" %}

If the dataset was restored without annotations, or some frames are missing annotations, you will add them in the next step, [Annotate Dataset](annotate.md).

## Next Steps

Once you have restored your MCAP into a dataset, the next step in the Raivin Quick Start guide is to [check and complete its annotations](annotate.md).
