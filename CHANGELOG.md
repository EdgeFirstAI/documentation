# Changelog

All notable changes to the EdgeFirst Studio Documentation are recorded in this
file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

Changes are grouped into dated release-candidate (`-rc`) snapshots by the date the
corresponding pull request was opened. None of these snapshots are part of a tagged
release yet; they are listed newest first.

### [2026-08-17-rc]

#### Added

- **Validation and Metrics concept page** (`profiler/concepts/validation.md`): new page documenting on-agent validation as it has worked since profiler 1.10.0 — `--validation off|after|during` and its auto-resolution, ground-truth sources, the `metrics.yaml` document structure (COCO summary metrics, per-class rows, `timing.trace`, `timing.concurrency`, `system`, `sahi`), re-scoring with `--predictions`/`--reprocess`/`--trace`, the `report` command, and the `publish` two-step route for memory-constrained segmentation targets.
- **Tiled Inference (SAHI) concept page** (`profiler/concepts/sahi.md`): new page covering `--sahi`, `--sahi-overlap`, `--sahi-convert`, the dashboard `t` toggle, the detection-only constraint, overlap resolution (model metadata with a 10% fallback since 1.16.0), the per-image tile metrics, and the 1.16.1 advisory that earlier tiled runs with skipped frames understated accuracy.
- **Container Images installation page** (`profiler/installation/docker.md`): new page with the GHCR tag matrix (`core`/`onnx`/`tflite`/`imx95`/`imx8mp`/`cuda`), per-target device flags, the `/config` volume, and output-ownership behavior; cross-linked from the Linux, i.MX, and Jetson pages.
- **Cloud Runs page** (`profiler/studio/cloud.md`): new page for the `dispatch` command, the Studio launch form's model picker and Hardware menu, the EC2-named instance classes, dedicated capacity, the default-class throughput caveat, and `platform.yaml` as the canonical machine record.
- All four pages registered in `profiler/.nav.yml`; new profiler-domain terms added to `docs/assets/known_words.txt` (also sorted and de-duplicated).

#### Changed

- **Profiler section updated from its 1.7.0 baseline to profiler 1.16.1** (all pages under `docs/profiler/`): the profiler computes COCO detection and segmentation metrics on-agent and publishes them to Studio — the section's pages and both mermaid diagrams no longer describe a separate cloud validator producing the metrics (`index.md`, `quickstart.md`, `studio/index.md`, `studio/from_studio.md`, `studio/from_profiler.md`).
- **Pipelining page rewritten for the current depth model** (`profiler/concepts/pipelining.md`): five pipeline stages including Materialize Masks, core-aware CPU inference depths (up to 16 via `--inference-depth`), corrected per-backend auto-depth table (Orin Nano pins, RPi5+Hailo 4, CoreML GPU 3), the 1.16.1 preprocess-depth correction, capture-stage bottleneck reporting (`capture_bound`, compute-bottleneck fields), measured worker-concurrency verdicts, `--serialize-core`, and a summary of the TUNING methodology.
- **Quickstart brought to the 1.16.1 command surface** (`profiler/quickstart.md`): all six subcommands, the five-slider launch dialog with the `s` and `t` shortcuts, the Docker install route, console warnings and `-v/-vv/-vvv`, and the clickable/copyable Studio link on completion.
- **Installation pages corrected per target** (`profiler/installation/*.md`): CUDA on Jetson/L4T replaces the stale "ONNX on Jetson is CPU-only" guidance; the removed CoreML compile cache is no longer documented on macOS; delegate tables gain `gpu` and the `qnn` family (with `qnn-dsp` replacing `qnn-cpu`); the Raspberry Pi page documents the sudo elevation flow and `--output-owner`; the Kinara page leads troubleshooting with the elevated-access requirement and adds the per-layer NPU breakdown; stale `--version 1.0.1` install pins removed; TFLite runtime library corrected to `libtensorflow-lite.so` with `TFLITE_LIBRARY_PATH`; Hailo batching documented as under development (runs per-frame today).
- **Studio integration pages corrected** (`profiler/studio/*.md`): the removed `--no-validate` flag replaced with `--validation off`; token-based CI authentication (`--token`/`--url`, `TOKEN`/`URL`) documented; `--training-session` artifact listing behavior corrected; the `publish` command documented; session re-run flag semantics, dataset-cache locking, and re-scoring workflows added.

#### Fixed

- **Host section no longer documents a username field** (`models/metadata.md`):
  the schema-v2 `host.username` field (e.g. `john.doe`) has been replaced with
  `host.organization` to match the ModelPack and Ultralytics trainer changes —
  training sessions and organization names are safe to embed in `edgefirst.json`,
  but individual usernames are not.

### [2026-06-24-rc]

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
  - Four workflow video assets (MP4) added under `getting_started/assets/workflows/`.
- **`video()` mkdocs-macro** (`macros.py`): renders an autoplaying, looping, muted
  inline `<video>` that behaves like a GIF; resolves the `<source>` URL via
  `get_relative_url` so it works under `use_directory_urls` and the versioned
  (mike) deployment, where MkDocs does not rewrite raw `<source>` URLs.
- **AGTG tutorial video** (`getting_started/assets/workflows/AGTG-tutorial.mp4`):
  new asset demonstrating the annotation workflow.
- **Jetson Orin Static IP and Wi-Fi Access Point guides**
  (`platforms/quickstart/jetson_orin/configuration/static_ip.md`,
  `wifi_ap.md`): new Configuration pages (wrapping the
  `discrete/platforms/orin_static_ip.md` and `orin_wifi_accesspoint.md`
  fragments) with matching `.nav.yml` entries.

#### Changed

- **Mermaid diagram node colors** (`getting_started/workflows/index.md`,
  `platforms/index.md`): inline `classDef` fills now use a 50% alpha (8-digit hex)
  so persona, journey, and platform diagrams stay legible in both the light and
  slate (dark) schemes.
- **Workflow GIFs converted to MP4**: six animated GIFs (auto-labelling,
  model-optimization, 3D perception, profiler, AGTG-tutorial, and
  `perception/dev/examples` boxes2d tracking) re-encoded as H.264 MP4 via the new
  `video()` macro, shrinking the documentation media payload from ~156 MB to
  ~8.8 MB to keep the GitHub Pages deploy within its size/time limits.
- **`*.mp4` and `*.gif` tracked with Git LFS** (`.gitattributes`) to manage large
  media assets efficiently and avoid GitHub file size warnings; stale
  individual model-file LFS rules removed.
- **Spelling standardized to American English** across the docs tree
  (`colour`/`grey`/`centre`/`honour` -> `color`/`gray`/`center`/`honor` in
  the calibration, metadata, profiler, and Foxglove pages) to match the
  spellcheck `en-GB_to_en-US` dictionary.
- **`assets/known_words.txt` reorganized**: sorted case-insensitively and
  de-duplicated for predictable diffs and easier maintenance.

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
- **Authored typos**: `AGTG Sibebar` -> `AGTG Sidebar` (`studio/agtg.md`),
  `coffeecups` -> `coffee cups` (`platforms/quickstart/imx8mplus/deploy.md`),
  and a curly-apostrophe `you’ve` normalized to `you've` in the Orin
  static-IP guide (it was being miscounted as the misspelling `youve`).
- **Broken `export-dataset` anchor** (`studio/datasets/index.md`): repointed
  to the local heading and removed a dangling cross-tutorial link.
- **Em-dash false positives** (`platforms/configuration/index.md`): spaced the
  em-dashes so adjacent words are no longer merged into unknown tokens.

#### Removed

- **Unused model assets removed**: duplicate
  `models/modelpack/assets/coffeecup-modelpack-multitask-t-1f54.{onnx,tflite}` and
  unreferenced `models/ultralytics/assets/yolov8s-seg_full_integer_quant*.tflite`.
- **Genuine misspellings removed from `assets/known_words.txt`** (`cameara`,
  `coud`, `dopper`, `reprensentations`, `sufficent`) so the spellchecker keeps
  flagging them. These originate in the mkdocstrings-generated
  `perception/api/*.md` pages and still require a fix upstream in the
  `edgefirst.schemas` package.

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
  for you?" section with four autoplaying looping videos (auto-labelling,
  model-optimization, 3D perception, profiler).
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
