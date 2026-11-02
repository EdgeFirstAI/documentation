# Nitrogen95 SMARC

{{ figure("../assets/nitrogen95_smarc.png", "Nitrogen95 SMARC", "50%") }}

The [Nitrogen95 SMARC](https://www.ezurio.com/system-on-module/nxp-imx9/nitrogen95-smarc) is a system-on-module (SOM) from Ezurio for building and evaluating vision-based edge AI applications. It is built on the [NXP i.MX 95](https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-9-applications-processors/i-mx-95-applications-processors:IMX95) application processor, which includes the eIQ Neutron NPU delivering up to 2 TOPS. The [EdgeFirst Perception Middleware](../../../../../perception/index.md) leverages the Neutron delegate to enable real-time edge perception workflows from data capture through deployment.

## System Architecture

The module follows the SMARC 2.2 standard (82 mm x 50 mm) and pairs the i.MX 95 with LPDDR5 memory, eMMC storage, an NXP PMIC and on-module Ethernet PHYs. Pre-certified Wi-Fi 6/6E and Bluetooth 5.4 are available through Ezurio's Sona wireless modules. It can be used with Ezurio's Universal SMARC Carrier, which turns it into a single board computer, or with a custom carrier. The Nitrogen95 shares the carrier board ecosystem of Ezurio's Nitrogen93, so the same carrier can be reused across modules.

| Feature | Specification |
|---------|---------------|
| Processor | 6x Cortex-A55 @ up to 1.8 GHz, 1x Cortex-M7 @ 800 MHz, 1x Cortex-M33 @ 333 MHz |
| AI Accelerator | eIQ Neutron NPU, up to 2 TOPS |
| Memory | 4 GB, 8 GB or 16 GB LPDDR5 |
| Storage | 16 GB eMMC |
| Display | Up to 3 independent displays, up to 4K |
| Camera | 2x 4-lane MIPI-CSI-2, integrated ISP (500 MP/s), video encode/decode up to 4K60p |
| Networking | 2x Gigabit Ethernet (IEEE 1588, TSN), 1x 10 Gigabit Ethernet, optional Wi-Fi 6/6E and Bluetooth 5.4 |
| Other Interfaces | 2x PCIe Gen3, 2x USB 3.1 Gen1, 3x USB 2.0, 2x CAN-FD, SDIO/eMMC, UART, I2C, SPI, I2S |
| Operating Temperature | 0 °C to +70 °C or -40 °C to +85 °C |

The module runs a Linux operating system built with Yocto or Buildroot using [Ezurio's EZ BSP](https://www.ezurio.com/software/ez-bsp), which adds secure boot and security-focused BSP releases. Android and QNX are also supported on the Cortex-A55 cores, and FreeRTOS on the Cortex-M7 and Cortex-M33.

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, our collection of applications and libraries used to implement the perception stack. The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../../../perception/index.md).

## Resources

- [Nitrogen95 SMARC product page](https://www.ezurio.com/system-on-module/nxp-imx9/nitrogen95-smarc)
- [Datasheet](https://www.ezurio.com/documentation/datasheet-nitrogen95-smarc)
- [Documentation and software downloads](https://www.ezurio.com/support/series/nitrogen95-smarc)
