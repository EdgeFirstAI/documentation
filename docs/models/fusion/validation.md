# Validating Fusion Models

This page will provide a walk-through on using DVE for validating the performance of Fusion models that have been trained, through the [QuickStart Guide](../../getting_started/index.md) or [Training Fusion](training.md). This page will focus only on the validation of Fusion models.

1. Select *Validator* from the tool options.

    <figure markdown="span">
    ![Validator Tool](../assets/validation/validator-tool.jpg){ align=center }
    <figcaption>Tool Options</figcaption>
    </figure>

2. Specify the project to run validation at the center of the top menu bar.

    <figure markdown="span">
    ![Project Selection](../assets/validation/validator-project-selection.jpg){ align=center }
    <figcaption>Project Selection</figcaption>
    </figure>

3. Create a new validation session by clicking the *create* button on the top right of the page.

    <figure markdown="span">
    ![Create New Session](../assets/validation/create-button.jpg){ align=center }
    <figcaption>Create New Session</figcaption>
    </figure>

4. Configure the settings on the left panel by specifying the name of the validation session, the model file to validate, and the dataset to deploy. Next configure the settings on the right panel by specifying the validation parameters. 

    > *Note:* 
    > *Additional information on these parameters are provided by hovering over the info button.* 

    > *Note:*
    > *The only augmentation available for this type of validation is `blur`. See [Vision Augmentations](../augmentations.md) for further details.*

    <figure markdown="span">
    ![Validation Options](../assets/validation/fusion-validation-options.jpg){ align=center }
    <figcaption>Validation Options</figcaption>
    </figure>

5. Start the session by clicking the *START SESSION* button on the bottom right.

    <figure markdown="span">
    ![Start Session](../assets/validation/start-session.jpg){ align=center }
    <figcaption>Start the Session</figcaption>
    </figure>

6. The validation session has now started while the progress is tracked on the left panel and additional information and status is shown on the right panel.  

    <figure markdown="span">
    ![Validation Session](../assets/validation/fusion-validation-session.jpg){ align=center }
    <figcaption>Validation Session</figcaption>
    </figure>

7. Once completed, the status will be shown as complete.

    <figure markdown="span">
    ![Completed Session](../assets/validation/fusion-completed-session.jpg){ align=center }
    <figcaption>Completed Session</figcaption>
    </figure>

8. The metrics are shown by clicking the plots button on the top left of the session card.

    <figure markdown="span">
    ![Validation Metrics](../assets/validation/fusion-validation-metrics.jpg){ align=center }
    <figcaption>Validation Metrics</figcaption>
    </figure>

    The metrics provides the precision, recall, F1, and IoU scores of the model at the specified window sizes. Additional charts are provided for the precision vs. recall and bird’s eye view heatmaps describing where the model performs well and where the model makes errors. 
    
    > *Note:*
    > *See [Metrics](../metrics.md) for further details.*

9. It is also possible to compare validation metrics for multiple sessions. This is done by checking the checkboxes on the top left of the session cards.

    <figure markdown="span">
    ![Comparing Sessions](../assets/validation/fusion-selecting-sessions.jpg){ align=center }
    <figcaption>Comparing Sessions</figcaption>
    </figure>

    Compare the validation sessions by clicking the *COMPARE VALIDATE SESSION* button on the top left. This will display the validation metrics side by side for the specified validation sessions.

    <figure markdown="span">
    ![Metrics Side-by-Side](../assets/validation/fusion-metrics-side-by-side.jpg){ align=center }
    <figcaption>Metrics Side-by-Side</figcaption>
    </figure>
