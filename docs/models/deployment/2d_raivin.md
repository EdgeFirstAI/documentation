# Deploying to the Raivin (Vision)

Now that you have validated your Vision Model from either a [managed](../validation/vision/managed.md) or [user-managed](../validation/vision/user_managed.md) session, this guide will walk you through deploying Vision models on a [Raivin Platform](../../platforms/quickstart/raivin/index.md).

!!! note "3D Applications"
    The Raivin is also capable of deploying Fusion models for 3D perception by following this [guide](3d_raivin.md).

{{ figure("../../platforms/assets/raivin.png", "Raivin", "50%") }}

{% include-markdown "discrete/models/deploy_on_raivin.md" heading-offset=0 %}

## Next Steps

In this tutorial, you have fetched the trained and validated model from EdgeFirst Studio, copied the model in the Raivin, configured the Raivin model services, and ran inference on the model in the device.  You have seen the model running live using the Raivin's camera and Radar module, and ran a Raivin MCAP recording to capture the model inferences in the frame that can be visualized using Foxglove Studio.

See our [developer guide](../../perception/dev/examples/model.md) for examples to query the model outputs using Rust or Python.

For more examples on deploying ModelPack in other platforms, see other [User Workflows](../../getting_started/workflows/index.md).
