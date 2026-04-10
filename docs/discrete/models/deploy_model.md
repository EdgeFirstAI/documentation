# Deploy the Model

Once you have validated your trained model, you can deploy the model in the browser using EdgeFirst Studio.  You can follow these steps either on a PC or a mobile device connected to EdgeFirst Studio in a browser.  Please note that the browser will use the camera on your device to run model inference.

From the training session card, you can run the model for inference by clicking the "Run Model" button on the top right of the page.

{{ figure("/models/assets/deployment/run-model-button.jpg", "Run Model Button") }}

You will be given the option for either live inference or inference from a file upload.  Go ahead and demo the live inference feed by clicking the "Live" option.

{{ figure("/models/assets/deployment/live-inference-option.jpg", "Live Inference Option") }}

You should now see the live inference feed on your browser running the trained model.

{{ figure("/models/assets/deployment/studio-runner-live-inference.jpg", "Live Inference") }}

You can also find more examples of deploying the model across different platforms.  Here is a checklist of supported devices.  We support [validation on specific targets](../../models/validation/vision/user_managed.md) and live video inference with links provided below.  

| Platform                                                               | On Target Validation | Live Video | In Development |
|------------------------------------------------------------------------|----------------------|------------|----------------|
| [EdgeFirst Studio](../../models/deployment/studio.md)                  | ✅                  | ✅         |                |
| [PC / Linux](../../models/deployment/pc/index.md)                      | ✅                  | ✅         |                |
| Mac/MacOS                                                              |                      |            | ✅ (untested)  |
| [Maivin](../../platforms/quickstart/maivin/deploy.md)                  | ✅                  | ✅         | ✅             |
| [Raivin Fusion](../../platforms/quickstart/raivin/deploy.md)           |                      | ✅         | ✅             |
| [i.MX 8M Plus EVK](../../platforms/quickstart/imx8mplus/deploy.md)     | ✅                  |             | ✅ (native runner) |
| [i.MX 95 EVK](../../platforms/quickstart/imx95/deploy.md)              | ✅                  |             | ✅ (native runner) |
| [NVIDIA Jetson Orin](../../platforms/quickstart/jetson_orin/deploy.md) | ✅                  |             | ✅ (native runner) |
| [Raspberry Pi](../../platforms/quickstart/raspberrypi/deploy.md)       |                      |            | ✅ (untested)   |

!!! note "Additional Platforms"

    Certain platforms are still under development and support for platforms beyond these listed will be available soon.  [Let us know](mailto:support@edgefirst.ai) which platform you'd like to see supported next!
    