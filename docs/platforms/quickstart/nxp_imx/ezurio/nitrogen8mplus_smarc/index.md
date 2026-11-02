# Nitrogen8M Plus SMARC

{{ figure("../assets/nitrogen8mp_smarc.png", "Nitrogen8M Plus SMARC", "50%") }}

The [Nitrogen8M Plus SMARC](https://www.ezurio.com/system-on-module/nxp-imx8/nitrogen8m-plus-smarc) is a system-on-module (SOM) from Ezurio for building and evaluating vision-based edge AI applications. It is built on the [NXP i.MX 8M Plus](https://www.nxp.com/products/i.MX8MPLUS) processor, which includes a neural processing unit delivering up to 2.3 TOPS. The [EdgeFirst Perception Middleware](../../../../../perception/index.md) leverages the NPU to enable real-time edge perception workflows from data capture through deployment.

## System Architecture

The module follows the SMARC 2.2 standard (82 mm x 50 mm) and pairs the i.MX 8M Plus with LPDDR4 memory, eMMC storage, an NXP PMIC, on-module Ethernet PHYs and a USB hub controller. Optional Wi-Fi 6/6E and Bluetooth 5.3/5.4 are available through Ezurio's Sona wireless modules. It can be used with Ezurio's Universal SMARC Carrier, which turns it into a single board computer, or with a custom carrier.

| Feature | Specification |
|---------|---------------|
| Processor | 4x Cortex-A53 @ 1.8 GHz, 1x Cortex-M7 @ 800 MHz |
| AI Accelerator | NPU, up to 2.3 TOPS |
| Memory | 2 GB or 4 GB LPDDR4 (up to 8 GB with MOQ) |
| Storage | 16 GB eMMC |
| Display | MIPI-DSI, HDMI, LVDS; up to 3 displays |
| Camera | 2x MIPI-CSI |
| Networking | 2x Gigabit Ethernet, optional Wi-Fi 6/6E and Bluetooth 5.3/5.4 |
| Other Interfaces | 2x USB 3.0/2.0, 2x USB 2.0, PCIe, 2x CAN/CAN FD, SDIO, I2C, SPI, UART, I2S |
| Operating Temperature | -40 °C to +85 °C |

The module runs a Linux operating system built with Yocto or Buildroot using [Ezurio's EZ BSP](https://www.ezurio.com/software/ez-bsp), which adds secure boot and security-focused BSP releases. Zephyr RTOS and FreeRTOS are also supported for the Cortex-M7 core.

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, our collection of applications and libraries used to implement the perception stack. The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../../../perception/index.md).

## Resources

- [Nitrogen8M Plus SMARC product page](https://www.ezurio.com/system-on-module/nxp-imx8/nitrogen8m-plus-smarc)
- [Getting Started guide](https://lairdcp.github.io/guides/nitrogen8mp-smarc-user-guide/1.0/Getting_Started.html)
- [Documentation and software downloads](https://www.ezurio.com/support/series/nitrogen8m-plus-smarc)
