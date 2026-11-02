# phyFLEX-i.MX 8M Plus Libra

{{ figure("../assets/phytec_imx8mp-libra.png", "phyFLEX-i.MX 8M Plus Libra", "50%") }}

The phyFLEX Libra i.MX 8M Plus is a development kit from PHYTEC for building and evaluating vision-based edge AI applications. It is built around the [phyFLEX-i.MX 8M Plus FPSC](https://www.phytec.eu/en/produkte/system-on-modules/phyflex-imx-8m-plus-fpsc/) system-on-module (SOM), which uses the [NXP i.MX 8M Plus](https://www.nxp.com/products/i.MX8MPLUS) application processor with an integrated NPU delivering 2.3 TOPS. The [EdgeFirst Perception Middleware](../../../../../perception/index.md) leverages the NPU to enable real-time edge perception workflows from data capture through deployment.

## System Architecture

The phyFLEX-i.MX 8M Plus FPSC is a compact module (40 mm x 37 mm x 3 mm) with up to four Cortex-A53 cores and a Cortex-M7 core for real-time tasks. The on-chip image signal processor supports cameras up to 12 megapixels, and the video unit provides 1080p60 H.265/H.264 encode and decode. The module follows the FPSC standard, so it is pin-compatible with other phyFLEX modules.

| Feature | Specification |
|---------|---------------|
| Processor | Up to 4x Cortex-A53 @ 1.8 GHz, 1x Cortex-M7 @ 800 MHz |
| AI Accelerator | NPU, 2.3 TOPS, with Tensilica HiFi 4 DSP |
| Memory | Up to 8 GB LPDDR4 |
| Storage | Up to 64 GB eMMC |
| Display | LVDS, HDMI, MIPI-DSI |
| Camera | MIPI-CSI, ISP supporting up to 12 megapixels |
| Networking | Dual Gigabit Ethernet with TSN |
| Other Interfaces | USB 3.0, PCIe 3.0, CAN FD |
| Operating Temperature | -40 °C to +85 °C |
| Longevity | 2035 |

The module runs a Linux operating system based on PHYTEC's [phyBSP](https://www.phytec.eu/en/leistungen/phybsp/), which provides a Yocto-based BSP.

Central to the EdgeFirst Platforms is the EdgeFirst Perception Middleware, our collection of applications and libraries used to implement the perception stack. The details of the low-level libraries are covered in the [EdgeFirst Perception Developer Guide](../../../../../perception/index.md).

## Resources

- [phyFLEX-i.MX 8M Plus FPSC product page](https://www.phytec.eu/en/produkte/system-on-modules/phyflex-imx-8m-plus-fpsc/)
- [Data sheet](https://www.phytec.eu/en/fileadmin/phytec_base/pdfs/flyer/Flyer_phyFLEX-i.MX_8M_Plus_FPSC_en_v2.0_2026-01.pdf)
- [phyFLEX-i.MX 8M Plus development kit](https://www.phytec.de/produkte/development-kits/phyflex-imx-8m-plus-kit/)
