# Fusion Benchmarks

This page provides a summary of the benchmarks gathered for Fusion models across various 3D datasets.

=== "Raivin Ultra Short"

    ## Raivin Ultra Short

    The Raivin Ultra Short dataset is an in house Fusion dataset created using a Raivin Platform with 3D bounding box annotations formulated using Radar or LiDAR PCDs.  The dataset is comprised of both indoor and outdoor scenes of people annotations.     

    **Table: Fusion on Raivin Ultra Short - (480x270) - ONNX - (50 epochs)**

    | Model                       | Kernel Size | Precision | Recall | IoU   | F1    |
    |-----------------------------|-------------|-----------|--------|-------|-------|
    | fusion-ultra-short-480x270  | 1           | 0.757     | 0.739  | 0.597 | 0.748 |
    |                             | 3           | 0.851     | 0.831  | 0.725 | 0.841 |

    **Table: Fusion on Raivin Ultra Short - (480x270) - TFLite - (50 epochs)**

    | Model                       | Kernel Size | Precision | Recall | IoU   | F1    |
    |-----------------------------|-------------|-----------|--------|-------|-------|
    | fusion-ultra-short-480x270  | 1           | 0.757     | 0.738  | 0.597 | 0.748 |
    |                             | 3           | 0.851     | 0.830  | 0.725 | 0.841 |

    Visit the full **Raivin Ultra Short** dataset [Benchmark here](../../datasets/raivin_ultra_short/index.md).
