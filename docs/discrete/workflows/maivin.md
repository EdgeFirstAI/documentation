# Capture with an EdgeFirst Platform

If you have an EdgeFirst Platform, follow this tutorial to see how to capture and upload datasets into EdgeFirst Studio.  Use your browser to connect to the Web UI of the remote device, enter the following URL `https://<hostname>/`.

!!! note
    Replace `<hostname>` with the hostname of your device.

You will be greeted with the Maivin [Web UI Main Page](../../platforms/quickstart/maivin/webui.md) page.

{{ figure("/platforms/assets/setup/ui-maivinMain.png", "Web UI Main Page") }}

{% include-markdown "discrete/datasets/recording_mcap_on_device.md" heading-offset=1 %}

{% include-markdown "discrete/datasets/downloading_mcap_from_device.md" heading-offset=1 %}

{% include-markdown "discrete/datasets/uploading_mcap_to_studio.md" heading-offset=1 %}

{% include-markdown "discrete/datasets/restore_snapshot.md" heading-offset=0 %}

Next [navigate to the gallery](../../datasets/tutorials/management.md#view-dataset) of the dataset by clicking on the image preview on the dataset card.  To correct any mistakes from the auto-annotation process, follow the tutorials described under [manual annotations](../../datasets/tutorials/annotations/manual.md#manual-2d-annotations).

Finally, [split the dataset](../../datasets/tutorials/management.md#split-dataset) into training and validation groups.

{% include-markdown "discrete/models/train_vision.md" heading-offset=0 %}
{% include-markdown "discrete/models/validate_vision.md" heading-offset=0 %}
{% include-markdown "discrete/models/deploy_model.md" heading-offset=0 %}
