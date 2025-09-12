# Ultralytics

The EdgeFirst Studio Model Zoo includes the [Ultralytics](https://docs.ultralytics.com/) YOLO which is a popular implementation of the ubiquitous YOLO architecture for one-shot detection models, and capable of being applied to various other tasks such as instance segmentation.  This document describes the integration into EdgeFirst Studio, supported features, and optimized deployment strategies.  For further details of the Ultralytics implementation of the YOLO architecture, please refer to their documentation.

Our Model Zoo ecosystem provides a collection of models to be re-trained through EdgeFirst Studio and deployed to a wide range of devices using a consistent workflow to achieve the best performance and latency at the edge.

## Getting Started

YOLOv8 and YOLOv11 can be trained now in Edgefirst Studio using a Graphical User Interface by following four simple steps:

=== "Select Framework"

    <h2 id="select-framework" style="display: none;"></h2>

    1. Select **Ultralytics** within the available training frameworks.

    ![Select Ultralytics Training Framework](../assets/ultralytics/ultralytics-train-01.png){ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [Next → 2. Name Session](#name-session){ .md-button .md-button--primary }
    </div>

=== "Name Session"

    <h2 id="name-session" style="display: none;"></h2>

    2. Set a **name** and **description** *(optional)* for the training session.

    ![Set Name and Description](../assets/ultralytics/ultralytics-train-02.png){ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [Select Framework ← Back](#select-framework){ .md-button }
    [Next → 3. Select Dataset](#select-dataset){ .md-button .md-button--primary }
    </div>

=== "Select Dataset"

    <h2 id="select-dataset" style="display: none;"></h2>

    3. Choose your **dataset**.

    ![Select a Dataset](../assets/ultralytics/ultralytics-train-03.png){ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [Name Session ← Back](#name-session){ .md-button }
    [Next → 4. Configure & Train](#train){ .md-button .md-button--primary }
    </div>

=== "Train"

    <h2 id="train" style="display: none;"></h2>

    4. **Configure model parameters** (architecture, input size, epochs, etc.) and start **Training**.

    ![Configure and Train](../assets/ultralytics/ultralytics-train-04.png){ align=center }

    <div class="wizard-actions" style="max-width: fit-content; margin-left: auto; margin-right: auto;" markdown>
    [Select Dataset ← Back](#select-dataset){ .md-button }
    [Next → 1. Select Framework](#select-framework){ .md-button  .md-button--primary }
    </div>

!!! note "Important"
    Datasets and default weights are handled internally by Edgefirst Studio.  There’s no need to migrate or store data locally.

## License

Ultralytics YOLO is covered by the GNU AGPL-3.0 license which allows for free use of this model within the constraints of the license.  Ultralytics offers [commercial licensing options](https://www.ultralytics.com/license).
