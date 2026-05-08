# Deploying to Embedded Targets

This guide will walk you through installing the EdgeFirst Middleware in "user-mode" on a target device.  If you're using a [Maivin](maivin.md) or [Raivin](3d_raivin.md) refer to their deployment guides instead.

{{ figure("../../platforms/assets/imx8mpevk-no-bg.png", "NXP i.MX 8M Plus EVK") }}

{% include-markdown "discrete/models/deploy_on_target.md" %}

## Next Steps

In this tutorial, you have fetched the trained and validated model from EdgeFirst Studio, copied the model to the EVK and ran the model live using the EdgeFirst Live application and the EVK's camera.

See our [developer guide](../../perception/dev/examples/model.md) for examples to query the model outputs using Rust or Python.

For more examples on deploying ModelPack in other platforms, see the [User Workflows](../../getting_started/workflows/index.md).
