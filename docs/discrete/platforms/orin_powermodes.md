# Set the Power Mode

You can set the board to 25W and disable any power savings by running the following commands. 

```shell
$ sudo nvpmodel -m 1
$ sudo jetson_clocks
```

| Power Mode | Code |
|------------|------|
| 7W         | 3    |
| 15W        | 0    |
| 25W        | 1    |
| MAXN       | 2    | 

!!! info
    These commands have to be set each time the board boots up as it defaults to run power savings.
    
    * You can find more information on the various power modes by entering `cat /etc/nvpmodel.conf`
    * You can see the current power mode set with `sudo nvpmodel -q`

## Power Savings

The command `sudo jetson_clocks` disables any power savings. You can find the differences in the device performance using `tegrastats`.

**Without** `sudo jetson_clocks`

```shell
$ tegrastats
04-27-2026 14:59:41 RAM 775/7620MB (lfb 3x4MB) SWAP 0/3810MB (cached 0MB) CPU [1%@729,0%@729,0%@729,0%@729,0%@729,0%@729] GR3D_FREQ 0% cpu@48.468C soc2@47.531C soc0@48.062C gpu@48.562C tj@49.156C soc1@49.156C VDD_IN 4761mW/4778mW VDD_CPU_GPU_CV 515mW/501mW VDD_SOC 1428mW/1428mW 
04-27-2026 14:59:42 RAM 775/7620MB (lfb 3x4MB) SWAP 0/3810MB (cached 0MB) CPU [0%@729,0%@729,0%@729,0%@729,0%@729,0%@729] GR3D_FREQ 0% cpu@48.625C soc2@47.468C soc0@48C gpu@48.593C tj@49.218C soc1@49.218C VDD_IN 4761mW/4777mW VDD_CPU_GPU_CV 515mW/502mW VDD_SOC 1428mW/1428mW 
04-27-2026 14:59:43 RAM 775/7620MB (lfb 3x4MB) SWAP 0/3810MB (cached 0MB) CPU [0%@729,0%@729,0%@729,0%@729,0%@729,0%@729] GR3D_FREQ 0% cpu@48.562C soc2@47.531C soc0@47.968C gpu@48.5C tj@49.062C soc1@49.062C VDD_IN 4761mW/4777mW VDD_CPU_GPU_CV 515mW/502mW VDD_SOC 1428mW/1428mW
```

**With** `sudo jetson_clocks`

```shell
$ tegrastats
04-27-2026 15:00:54 RAM 779/7620MB (lfb 2x4MB) SWAP 0/3810MB (cached 0MB) CPU [0%@1344,0%@1344,0%@1344,0%@1344,0%@1344,0%@1344] GR3D_FREQ 0% cpu@50.125C soc2@49.125C soc0@49.25C gpu@50.562C tj@50.562C soc1@50.437C VDD_IN 6626mW/6625mW VDD_CPU_GPU_CV 1228mW/1230mW VDD_SOC 2380mW/2380mW 
04-27-2026 15:00:55 RAM 779/7620MB (lfb 2x4MB) SWAP 0/3810MB (cached 0MB) CPU [0%@1344,0%@1344,0%@1344,0%@1344,0%@1344,0%@1344] GR3D_FREQ 0% cpu@50.093C soc2@49.312C soc0@49.343C gpu@50.593C tj@50.593C soc1@50.406C VDD_IN 6626mW/6625mW VDD_CPU_GPU_CV 1228mW/1230mW VDD_SOC 2380mW/2380mW 
04-27-2026 15:00:56 RAM 779/7620MB (lfb 2x4MB) SWAP 0/3810MB (cached 0MB) CPU [0%@1344,0%@1344,0%@1344,0%@1344,0%@1344,0%@1344] GR3D_FREQ 0% cpu@49.812C soc2@49.187C soc0@49.437C gpu@50.562C tj@50.562C soc1@50.468C VDD_IN 6626mW/6625mW VDD_CPU_GPU_CV 1228mW/1230mW VDD_SOC 2380mW/2380mW
```

| Metric               | Without `sudo jetson_clocks`     | With `sudo jetson_clocks`          |
|----------------------|----------------------------------|------------------------------------|
| CPU Frequency        | ~729 MHz (idle scaling)          | ~1.34 GHz (locked)                 |
| Total Power (VDD_IN) | ~4760 mW (~4.7 W)                | ~6626 mW (~6.6 W)                  |
| CPU/GPU/CV Rail      | ~515 mW                          | ~1228 mW (>2× increase)            |
| SOC Rail             | ~1428 mW                         | ~2380 mW                           |
| Temperature          | ~48–49 °C                        | ~50–51 °C                          |