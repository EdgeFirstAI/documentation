
# Radar Settings (Raivin-only)

This page configures the radar publishing service that interacts with the Raivin's integrated [DRVEGRD-169 radar module][radar] from [smartmicro][smart].  With the exception of the H.264 Bitrate and maybe camera or stream sizes, it is not recommended that you change these settings.

{{ figure("../assets/configuration/configuration-radarpub.png", "Radar Settings page") }}

!!! tip
    These values are stored in the `/etc/default/radarpub` file on the device and can be hand-edited.  This is not recommended.

## Log Level

Log level for the application, relevant sub-filters are radarpub and drvegrd refer to [RUST_LOG documentation][rustlog] for details.

## Center Frequency

Radar center frequency band.  The low option is required when using the ultra-short FREQUENCY_SWEEP option. Options are 'low', 'medium', and 'high'.

## Frequency Sweep

The frequency sweep controls the detection range of the radar.  The following breakdown gives a general range at which a vehicle-type object should be detected.

- ultra-short: 9m (requires CENTER_FREQUENCY="low")
- short: 19m
- medium: 56m
- long: 130m

!!! note
    Ultra-short range (in Frequency Sweep) only works with Low Center frequency.

## Range Toggle

The range-toggle mode allows the radar to alternate between various frequency sweep configurations.  Applications must handle range toggling as targets will not be consistent between messages as the frequency alternates.

!!! warning
    The radar cube model does NOT currently handle alternating frequencies as it requires the dataset to be captured at a specific frequency sweep config.

Options are 'off', 'short-medium', 'short-long', 'medium-long', 'long-ultra-short', 'medium-ultra-short', and 'short-ultra-short'.

## Detection Sensitivity

The detection sensitivity only affects the radar target list (point-cloud) and controls the sensitivity to recognize a target.  The default is 'medium', the 'low' and 'high' sensitivity options will result in less and more targets, respectively.

## Enable Cube

Enable streaming the low-level radar cube.  This can be used by the low-level radar fusion model or to record MCAP files for the purpose of training this model.  The radar cube capture consumes approximately 240mbps bandwidth over the private Raivin ethernet connection and approximately 75% of one of the CPU cores, enable it when required but otherwise should be left disabled.

## Clustering Options

The following settings enables and configures clustering the radar targets.

### Clustering

Enable clustering the radar targets into the `/radar/clusters` topic.

### Window Size

Temporal clustering of the radar targets using the window size.  The window size is the number of frames to cluster, each frame representing 55ms.  The window clustering is a rolling window so it does not incur any additional latency.

### Clustering EPS

The epsilon value to be used for Density-Based Spatial Clustering and Application with Noise (DBSCAN) clustering. Higher values mean points further from each other can be clustered together.

### Clustering Parameter Scale

Clustering DBSCAN parameter scaling. Parameter order is x, y, z, speed. Set the appropriate axis to 0 to ignore that axis. Default setting of `[0.5 1.0 0.0 0.0]` means that only xy distances are taken into account.

### Clustering Point Limit

The minimum number of points per cluster for DBSCAN clustering.

[radar]: https://www.smartmicro.com/automotive-radar/drvegrd-line#c20151
[smart]: https://www.smartmicro.com/
[rustlog]: https://docs.rs/env_logger/latest/env_logger/#enabling-logging
