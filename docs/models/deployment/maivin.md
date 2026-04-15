# Deploying to the Maivin

Now that you have validated your Vision Model either [On Cloud](../validation/vision/managed.md) or [On Target](../validation/vision/user_managed.md), this guide will walk you through deploying Vision models on a [Maivin Platform](../../platforms/quickstart/maivin/index.md).  

{{ figure("../../platforms/assets/maivin-2.png", "Maivin", "50%") }}

{% include-markdown "discrete/models/deploy_on_maivin.md" heading-offset=0 %}

## Next Steps

In this tutorial, you have fetched the trained and validated model from EdgeFirst Studio, copied the model in the Maivin, configured the Maivin model services, and ran inference on the model in the device.  You have seen the model running live using the Maivin's camera and ran a Maivin MCAP recording to capture the model inference in the frames that can be visualized using Foxglove Studio.

See our [developer guide](../../perception/dev/examples/model.md) for examples to query the model outputs using Rust or Python.

For more examples on deploying ModelPack in other platforms, see other [User Workflows](../../getting_started/workflows/index.md).
