# Changelog

All notable changes to the EdgeFirst Studio Documentation are recorded in this
file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **EdgeFirst Client section** (`docs/client/`): new top-level documentation for
  `edgefirst-client` (CLI, dataset import pathways, seven Python tutorials, Python
  and Rust API reference). Replaces `perception/studio.md` and
  `perception/api/studio.md`; legacy `datasets/coco/import.md` removed in favour of
  `client/import.md` (COCO/LVIS CLI, EdgeFirst format, conceptual Python imports).
  Redirects added in `mkdocs.yml` (DE-2762).
- **Getting Started index** (`docs/index.md`): product intro, Quick Start workflow
  table, Profiler feature ribbon, free credits tip, and "Is EdgeFirst Studio right
  for you?" section linking to the Tourist workflow.
- **Tourist workflow** (`discrete/workflows/tourist.md`): new "Is EdgeFirst Studio
  for you?" section with four clickable GIFs (auto-labelling, model-optimization,
  3D perception, profiler) linking to their respective documentation sections.
- **Free credits note** added to `index.md`, `getting_started/workflows/index.md`,
  and `studio/user/index.md` (\$50 sign-up credit + \$15/month recurring).
- **Profiler feature ribbon** (`ef-feature-ribbon` CSS component) added to
  `stylesheets/components.css` with dark-mode support and gold left-border accent.
- **"No Training Charts" note** added to `discrete/models/train_ultralytics.md`,
  `models/ultralytics/index.md`, and `models/training/vision.md` explaining that
  sessions with Enable Training disabled produce no epoch-based charts.
- **`validate_vision.md` restructured** to clearly separate cloud validation
  (ONNX/Keras/TFLite only) from on-target profiling, with a routing table and
  link to the Profiler.
- **`studio/models.md`**: ONNX-only note added to the "Running a model" section.
- **Profiler+ workflow** (`discrete/workflows/profiler_plus.md`) rewritten to use
  the Ultralytics training session include and on-target profiler validation steps
  instead of the cloud validation path.
- **Login page** (`getting_started/login.md`): rewrote the transition sentence to
  be more inviting; added PC/phone/camera context and a "Next →" footer link.
- Four workflow GIF assets added under `getting_started/assets/workflows/`.
- **2D annotation guide** (`discrete/datasets/annotate_2d_dataset.md`): enhanced
  with AGTG server launch steps, timeout warning, video playback verification tip,
  and back-to-gallery navigation. New screenshot assets added.
- **Tourist Plus workflow** (`discrete/workflows/tourist_plus.md`): expanded with
  public datasets description and new "Browse Public Experiments" section.
- **Mobile image import screenshot** (`docs/datasets/assets/capture/mobile-image-import-fields.jpg`):
  new asset for uploading images workflow documentation.
- **AGTG tutorial GIF** (`getting_started/assets/workflows/AGTG-tutorial.gif`):
  new animated asset demonstrating annotation workflow.
- **Device compatibility note** added to `recording_on_phone.md` explaining that
  screenshots are Samsung-based and device UIs may vary across manufacturers.
- **Tutorials & Guides hub** (`docs/index.md`): Material grid-cards section linking
  to Dataset Tutorials, Annotations, Model Training, Profiler, User Workflows, and
  Platform Quick Starts to make instructional pages easier to discover.
- **Profiler Quick Start warning** (`profiler/quickstart.md`): note that profiling
  must run against a user-owned project — the Sample Project and any public,
  read-only project will fail with an error.
- **Profiler platform video demos** (`profiler/index.md`): embedded demo videos
  for MacBook, NXP i.MX 95, and NXP Ara240 targets.
- **Fully Automatic AGTG work-in-progress notice**
  (`datasets/tutorials/annotations/automatic.md`): bug admonition flagging fully
  automatic ground truth generation as non-operational and directing users to the
  semi-automatic workflow; expanded the related note in `annotations/index.md`.

### Changed

- **Screenshot updates**: training, validation, and deployment screenshots
  refreshed across `models/assets/training/`, `models/assets/validation/`,
  `getting_started/assets/run_model/`, and `profiler/assets/`.
- **Capture and management screenshots optimized** for web performance across
  `datasets/assets/capture/` and `datasets/assets/management/` directories.
- **Annotation screenshots compressed**: AGTG prompts, segment tool, propagation,
  and annotation set UI screenshots optimized for faster loading.
- **Billing documentation updated** (`studio/user/billing.md`): rewritten for the
  redesigned Monthly Bill view (month/year selector, feature categories, Cost vs
  Charge columns, Net Usage and Grand Total); refreshed `usage-billing-page.jpg`
  and removed the unused `current-usage-section.jpg`.
- **Dataset import tutorial** (`datasets/tutorials/import.md`): converted image
  pairs to side-by-side tables and aligned the steps with the consolidated COCO
  upload flow; added and replaced import screenshots, removing superseded ones.
- **Unused assets removed**: `studio/assets/models/experiments-page.jpg`,
  `datasets/assets/annotations/automatic/agtg-propagation-completed.jpg`, and
  several superseded coco128/coco2017 import screenshots.
- **Screenshots recompressed**: login, forgot-password, navigation help-options,
  and projects screenshots optimized for web performance.
- **Profiler instructions** (`profiler/studio.md`): updated to use COCO dataset
  from the public COCO sample projects for more realistic profiling examples.
- **Studio "Run Pretrained Models"** (`studio/models.md`): added missing
  screenshots for improved user clarity and step-by-step guidance.
- **Workflow documentation clarified** in `discrete/datasets/uploading_*.md` and
  workflow files for improved user guidance.
- **GIF files tracked with Git LFS** (`.gitattributes` updated) to manage large
  animated assets efficiently and avoid GitHub file size warnings.
- `models/assets/deployment/run-model-button.jpg` removed (unused asset).
- `getting_started/assets/workflows/dataset-groups.jpg` removed (outdated asset).
- `getting_started/workflows/index.md` free credits note dollar signs escaped to
  prevent arithmatex from rendering them as math delimiters.

- Model Zoo callout admonition added to all five converter pages
  (`tflite`, `neutron`, `tensorrt`, `ara2`, `hailo`) directing users to the
  [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models)
  for the latest supported model list, platform-specific validation results, and
  benchmark numbers.

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
