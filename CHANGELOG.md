# Changelog

All notable changes to the EdgeFirst Studio Documentation are recorded in this
file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `mkdocs-redirects` plugin with a `redirect_maps` configuration so previously
  published documentation URLs no longer return 404 after pages were moved or
  renamed. The redirect map covers the model conversion documentation that was
  consolidated under `models/conversion/`:
  - `models/custom/neutron/` and `models/ultralytics/neutron/` →
    `models/conversion/neutron/`
  - `models/ultralytics/quantize/` and `models/modelpack/quantize/` →
    `models/conversion/`
  - `models/conversion/kinara/` → `models/conversion/ara2/` (Kinara converter
    renamed to ARA-2)
  - `models/ultralytics/npu/` and `models/modelpack/npu/` →
    `models/deployment/launcher/` (deprecated NPU on-target demos removed)
