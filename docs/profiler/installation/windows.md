# Windows

The EdgeFirst Profiler ships an **x86_64** binary for Windows. As on macOS, the supported scope is ONNX-model development and EdgeFirst Studio workflow — the vendor accelerator backends are Linux-only.

!!! note "Windows release status"
    Standalone Windows binaries are published on the [profiler-cli releases page](https://github.com/EdgeFirstAI/profiler-cli/releases). If you hit an "asset not found" error on `install.ps1`, confirm the release tag has a `windows-x86_64.zip` artifact.

## Install

=== "Python (pip)"

    ```powershell
    pip install edgefirst-profiler
    ```

=== "Platform installer"

    Open PowerShell and run:

    ```powershell
    irm https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.ps1 | iex
    ```

    The installer detects whether PowerShell is elevated:

    - **Elevated:** installs to `%ProgramFiles%\edgefirst-profiler\` and updates the system `PATH`.
    - **Non-elevated:** installs to `%LOCALAPPDATA%\Programs\edgefirst-profiler\` and updates the user `PATH`.

    Pin a specific release:

    ```powershell
    & ([scriptblock]::Create((irm https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.ps1))) -Version 1.0.1
    ```

Confirm in a **new** PowerShell window (so `PATH` is reloaded):

```powershell
edgefirst-profiler --version
```

## ONNX Runtime

The default backend dlopens `onnxruntime.dll`. The simplest install is `pip install onnxruntime` inside the same virtual environment you used for `edgefirst-profiler`. Alternatively, download a Windows release of ONNX Runtime from [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime/releases) and place `onnxruntime.dll` somewhere on `PATH`.

## Terminal UI

The TUI uses Unicode box-drawing and Braille characters. On Windows 10+ the default Terminal app renders these correctly; use **Windows Terminal** rather than the legacy `conhost` for the cleanest output.

```powershell
edgefirst-profiler
```

## What is not supported on Windows

The same list as macOS — TFLite, Neutron / VSI delegates, Ara-2, Hailo, and TensorRT are Linux/edge-only. For validation against those backends, run the profiler on the target board itself, or on a Linux host with the relevant runtime libraries installed.

## Troubleshooting

**The installer reports "execution policy restricts running this script."**

Run PowerShell with a process-scoped policy bypass:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
irm https://raw.githubusercontent.com/EdgeFirstAI/profiler-cli/main/install.ps1 | iex
```

**`edgefirst-profiler` is not found after install.**

Open a new PowerShell window so the updated `PATH` is picked up. If the binary is still not found, check the install directory printed by the installer and add it to your `PATH` manually via **System Properties → Environment Variables**.
