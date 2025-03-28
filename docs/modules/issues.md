# Known Issues

### "SSL peer certificate or SSH remote key was not OK" during `ostree pull`
If you update the `ethernet0` network interface without a reboot and try to run an `ostree pull` command, you may get the following error:
```
error: While fetching https://maivin.deepviewml.com/ostree/summary.sig: [60] SSL peer certificate or SSH remote key was not OK
```
If so, reboot the system with the `sudo reboot` command.  This should address the issue.
