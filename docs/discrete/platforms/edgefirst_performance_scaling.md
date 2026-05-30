# CPU Performance Scaling

There are various CPU performance modes available on the platform which can be set by accessing the terminal on the device.

```shell
$ cat /sys/devices/system/cpu/cpufreq/policy0/scaling_available_governors
conservative ondemand userspace powersave performance schedutil
```

| Mode          | Behavior                                                      | Tradeoff                         |
|---------------|---------------------------------------------------------------|----------------------------------|
| performance   | Locks CPU at maximum frequency                                | 🔥 highest power, lowest latency |
| powersave     | Locks CPU at minimum frequency                                | 🐢 lowest power, slowest         |
| schedutil     | Scheduler-driven dynamic scaling (modern default)             | ⚖️ balanced, efficient           |
| ondemand      | Quickly ramps up on load, drops when idle                     | ⚡ responsive but older approach |
| conservative  | Slowly increases/decreases frequency                          | 🌿 smoother, but slower response |
| userspace     | Manual control from user-space programs                       | 🛠️ full control, more work       |

To see the current performance mode, run this command.

```shell
$ cat /sys/devices/system/cpu/cpufreq/policy0/scaling_governor
performance
```

To see the clock frequency limits, run these commands.

```shell
$ cat /sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq # Current CPU frequency
1600000
$ cat /sys/devices/system/cpu/cpufreq/policy0/scaling_max_freq # Max CPU frequency
1600000
$ cat /sys/devices/system/cpu/cpufreq/policy0/scaling_min_freq # Min CPU frequency
1200000
```

If you want maximum performance from the device, you can set the device to `performance` mode which runs the CPU cluster at the highest available frequency.

```shell
$ echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor
performance
```

You can find more information on CPU Performance Scaling [here](https://docs.kernel.org/admin-guide/pm/cpufreq.html).
