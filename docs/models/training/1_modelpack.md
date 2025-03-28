# Modelpack

This page will provide a walk-through on using DVE for training Vision models using Modelpack.

1. Select *Trainer* from the tool options. 

    <figure markdown="span">
    ![Trainer Tool](../../assets/models/training/trainer-tool.jpg){ align=center }
    <figcaption>Tool Options</figcaption>
    </figure>

2. Specify the project to run training at the center of the top menu bar.

    <figure markdown="span">
    ![Project Selection](../../assets/models/training/trainer-project-selection.jpg){ align=center }
    <figcaption>Project Selection</figcaption>
    </figure>

3. Create a new training session by clicking the *create* button on the top right.

    <figure markdown="span">
	![Create New Session](../../assets/models/validation/create-button.jpg){ align=center }
	<figcaption>Create New Session</figcaption>
	</figure>

4. Configure the settings on the left panel by specifying *Trainer Type* to *Modelpack* and provide additional configurations for the name of the session and the dataset to deploy. Next configure the settings on the right panel by specifying training parameters. By default a segmentation model will be trained, however, object detection or multi-task based models are possible variations. 

    > *Note:* 
	> *Additional information on these parameters are provided by hovering over the info button.* 

    > *Note:*
    > *For more information on available vision augmentation please see [Vision Augmentations](../augmentations.md).*

    <figure markdown="span">
    ![Training Options](../../assets/models/training/modelpack-training-options.jpg){ align=center }
    <figcaption>Training Options</figcaption>
    </figure>

5. Start the session by clicking the *START SESSION* button on the bottom right.

    <figure markdown="span">
	![Start Session](../../assets/models/validation/start-session.jpg){ align=center }
	<figcaption>Start the Session</figcaption>
	</figure>

6. The training session has now started while the progress is tracked on the left panel and additional information and status is shown on the right panel.

    <figure markdown="span">
    ![Training Session](../../assets/models/training/modelpack-training-session.jpg){ align=center }
    <figcaption>Training Session</figcaption>
    </figure>

7. Once completed, the status will be shown as complete.

    <figure markdown="span">
    ![Completed Session](../../assets/models/training/modelpack-completed-session.jpg){ align=center }
    <figcaption>Completed Session</figcaption>
    </figure>

8. The training metrics are shown by clicking the plots button on the top left of the session card. 

    <figure markdown="span">
    ![Training Metrics](../../assets/models/training/modelpack-training-metrics.jpg){ align=center }
    <figcaption>Training Metrics</figcaption>
    </figure>

9. The trained Keras, TFLite, and RTM models can be found and downloaded by clicking on the maximize button next to the plots button on the top right of the session card. This will open a new dialog with the session details and the models are placed on the top right which can then be downloaded.

    <figure markdown="span">
    ![Session Details](../../assets/models/training/modelpack-session-details.jpg){ align=center }
    <figcaption>Session Details</figcaption>
    </figure>

10. Now you have generated your Vision model, follow these [next steps](../validation/1_modelpack.md) for validating your Vision model.