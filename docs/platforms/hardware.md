# Hardware

The Maivin Perception Platform is available in two configurations: Maivin and Raivin.  The Maivin configuration is a vision-only platform while the Raivin configuration includes an [integrated radar module](./radar.md).  The Raivin configuration is built on the core Maivin configuration and both run the same software stack.  The Raivin configuration also runs the additional radar and sensor fusion software.

The Maivin configuration provides a vision-based perception stack for use in harsh environments, providing an IP66/67 waterproof enclosure and connectors.  The Maivin platform is built on the NXP i.MX 8M Plus processor which includes a 2 TOPS AI accelerator.  The EdgeFirst Perception Middleware leverages the AI-accelerator enabling this vision sensor to be deployed in the field to deliver real-time edge perception applications.

The Raivin configuration further extends the perception capabilities of the platform through the addition of the integrated radar module.  The EdgeFirst Perception Middleware is augmented for Raivin configurations with the RadarExp Fusion Model which provides low-level radar data fusion with the vision data.  The low-level radar data is reprensented as the range and doppler data cube, the RadarExp module fuses this data with the vision data to provide a more robust perception stack.  The traditional point-cloud data from the radar is also available for use by the Raivin perception stack, and is especially useful for augmenting the object detection and tracking capabilities through the additional parameters offered by the point cloud data.  

Further details on the Fusion Model can be found in the EdgeFirst Perception Developer Guide.  Details of annotating datasets for
training can be found in the Deep View Enterprise User Manual.

## Hardware Features

- Small, optimized form factor for easy deployment for true application testing with enclosure.
- 2 board architecture with Processor Board, and Images Sensor board.  Allows different image sensors to be used.
- 12-24V power input with protection for flexible installations. 
- Flexible communications options including RS-485, Ethernet, and Wi-Fi.
- M.2 PCIe and USB expansion interface:
  - Wireless LAN modem support
  - Additional AI accelerator support
- Expansion memory support via SD Card
- Internal UART console debug interface
- GNSS receiver
- Inertial Measurement Unit (IMU)
- Protected Input/Output for connection to external devices.
- Rugged waterproof enclosure for outdoor installations. Ready for field installation.
- M12 waterproof circular connectors for Power/Communications
- Waterproof RJ45 for Ethernet


## Hardware Specifications


## Electrical Specifications


## Mechanical Specifications

![Maivin Mechanical Drawing](static/mechanical.png){align=center}

## Connectors

