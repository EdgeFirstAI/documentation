After [training a **Vision** model](../../models/training/vision.md) in EdgeFirst Studio, you can deploy the ONNX model in any device connected to a browser with access to a camera.  This can be your phone or your PC as an example.  This guide will show you the steps for deploying the model using EdgeFirst Studio.

!!! note "ONNX models only"
    Live browser-based model running only supports **ONNX** format. To validate or profile models in other formats (TFLite, Neutron, Hailo, TensorRT, etc.) on real hardware, use the [EdgeFirst Profiler](../../profiler/index.md).

Navigate to the training session you wish to deploy by going back to the "Projects" page by clicking the "Projects" button at the top left of the page.

{{ figure("/studio/assets/navigation/projects-button.jpg", "Go to Projects Page") }}

Click on the model experiments of your project.

{{ figure("/models/assets/validation/model-experiments.jpg", "Model Experiments Page") }}

Click on the training sessions of your experiment.

{{ figure("/models/assets/validation/training-sessions.jpg", "Training Sessions") }}

Click on the selected training session.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Session Details") }}

Click the "Run Model" button on the top right of the page.

{{ figure("/getting_started/assets/run_model/trainer_details_page.png", "Run Model Button") }}

## Live Inference

You will be given the option for either live inference or inference from a file upload.  Go ahead and demo the live inference feed by clicking the "Live" option.

{{ figure("/models/assets/deployment/live-inference-option.jpg", "Live Inference Option") }}

You should now see the live inference feed on your browser running the trained model.

{{ figure("/models/assets/deployment/studio-runner-live-inference.jpg", "Live Inference") }}

## Image Inference

Alternatively, you can also select the "Upload" option where you can select any image in your filesystem to pass to the model for inference.

{{ figure("/models/assets/deployment/image-inference-option.jpg", "Image Inference Option") }}

Select an image from the filesystem to run inference.

{{ figure("/models/assets/deployment/select-image.jpg", "Select Image") }}

You should now see the image with the model inference displayed in EdgeFirst Studio.

{{ figure("/models/assets/deployment/studio-runner-image-inference.jpg", "Image Inference") }}
