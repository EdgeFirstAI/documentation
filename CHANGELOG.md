# Changelog

All notable changes to the EdgeFirst Studio Documentation are recorded in this
file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

Changes are grouped into dated release-candidate (`-rc`) snapshots by the date the
corresponding pull request was opened. None of these snapshots are part of a tagged
release yet; they are listed newest first.

### [2026-06-23-rc]

#### Added

- **Explore Public Datasets section** (`discrete/workflows/tourist.md`): documents the
  landing page **Public Datasets** button and the Public Projects gallery it opens
  (Trending/Most Recent), with a table of the available public projects (Sample Projects,
  COCO Detection, COCO Instance Segmentation) and a tip on copying read-only projects to
  build on them. New `public-datasets-button.jpg` asset added.
- **Studio Apps dashboard expanded** (`studio/apps.md`): reframed the page as a
  catalog, clarified that apps are launched from their workflow (not the Apps
  page), and added per-app sections for the EdgeFirst Profiler, Validator, and the
  TFLite, Neutron, TensorRT, Ara2, and Hailo Converter Apps with links to their
  conversion pages; refreshed `apps-page.png`.
- **Browser Support section** (`studio/index.md`): recommends Chromium-based
  browsers and adds a bug admonition noting Firefox sliders are not yet operational.
- **Markdown Lint section** (`README.md`): documents running
  `npx --yes markdownlint-cli2@0.13.0 "docs/**/*.md"` locally, what it checks
  (the rules in `.markdownlint.json`), and why it mirrors the CI lint step.
- **Markdownlint configuration** (`.markdownlint.json`): tuned the rule set to the
  project's MkDocs Material conventions — 4-space nested-list indent (`MD007`),
  an `allowed_elements` list for the inline HTML the docs rely on (`MD033`), and
  disabling rules that conflict by design (e.g. `MD013`, `MD025`, `MD029`,
  `MD034`, `MD036`, `MD041`, `MD046`, `MD051`, `MD060`).

#### Changed

- **Mermaid diagram node colors** (`getting_started/workflows/index.md`,
  `platforms/index.md`): inline `classDef` fills now use a 50% alpha (8-digit hex)
  so persona, journey, and platform diagrams stay legible in both the light and
  slate (dark) schemes.

#### Fixed

- **Dark-mode admonition titles** (`stylesheets/extra.css`): note, tip, info, and
  warning title bars now use translucent brand-hued tints under the slate scheme
  so the near-white title text no longer washes out on the light pastel backgrounds.
- **Markdown lint violations** across the docs tree: standardised nested lists to
  4-space indentation, stripped trailing whitespace (including CRLF files),
  inserted required blank lines around lists, replaced raw `<img>` tags with the
  `figure()` macro in `models/fusion/index.md`, wrapped a bare placeholder token
  in `discrete/platforms/orin_static_ip.md`, and filled the determinable empty
  Foxglove example links in `perception/topics/camera.md` and
  `perception/topics/lidar.md`. Remaining empty links are genuine placeholders
  with no target yet, and the lint step stays non-blocking in CI.
- **Git LFS assets in published docs** (`.github/workflows/publish.yml`): the
  deploy workflow now checks out with `lfs: true`, so LFS-tracked images and GIFs
  resolve correctly on the published site instead of rendering as pointer files.

### [2026-06-19-rc]

#### Added

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

#### Changed

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

### [2026-06-18-rc]

#### Added

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

#### Changed

- **Capture and management screenshots optimized** for web performance across
  `datasets/assets/capture/` and `datasets/assets/management/` directories.
- **Annotation screenshots compressed**: AGTG prompts, segment tool, propagation,
  and annotation set UI screenshots optimized for faster loading.
- **Profiler instructions** (`profiler/studio.md`): updated to use COCO dataset
  from the public COCO sample projects for more realistic profiling examples.
- **Studio "Run Pretrained Models"** (`studio/models.md`): added missing
  screenshots for improved user clarity and step-by-step guidance.
- **Workflow documentation clarified** in `discrete/datasets/uploading_*.md` and
  workflow files for improved user guidance.
- **GIF files tracked with Git LFS** (`.gitattributes` updated) to manage large
  animated assets efficiently and avoid GitHub file size warnings.
- `getting_started/assets/workflows/dataset-groups.jpg` removed (outdated asset).

### [2026-06-17-rc]

#### Added

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

#### Changed

- **Screenshot updates**: training, validation, and deployment screenshots
  refreshed across `models/assets/training/`, `models/assets/validation/`,
  `getting_started/assets/run_model/`, and `profiler/assets/`.
- `models/assets/deployment/run-model-button.jpg` removed (unused asset).
- `getting_started/workflows/index.md` free credits note dollar signs escaped to
  prevent arithmatex from rendering them as math delimiters.

### [2026-06-12-rc]

#### Added

- Model Zoo callout admonition added to all five converter pages
  (`tflite`, `neutron`, `tensorrt`, `ara2`, `hailo`) directing users to the
  [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models)
  for the latest supported model list, platform-specific validation results, and
  benchmark numbers.

### [2026-06-02-rc]

#### Added

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
