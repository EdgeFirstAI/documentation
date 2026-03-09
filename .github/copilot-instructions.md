# Copilot Instructions

This file provides guidance to GitHub Copilot and Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **official unified documentation** for the EdgeFirst suite, published as an MkDocs Material site at https://doc.edgefirst.ai/. It is maintained by Au-Zone Technologies (https://www.edgefirst.ai, also https://www.au-zone.com).

The EdgeFirst suite consists of two major products:

- **EdgeFirst Studio** — A cloud SaaS platform for the complete ML lifecycle: dataset management, annotations, model training, validation, and deployment. It is the central hub of the EdgeFirst ecosystem.
- **EdgeFirst Perception** — An Apache 2.0 open-source suite of software components for embedded edge deployments, hosted at https://github.com/EdgeFirstAI. It implements the optimized runtime for EdgeFirst, with a special focus on EdgeFirst Studio integrations for dataset capture and model deployment.

### Supported Platforms

EdgeFirst Studio and Perception are optimized for edge devices:

- **NXP i.MX 8M Plus** and **NXP i.MX 95** (primary targets)
- **Kinara Ara-2** (now NXP Ara240)
- **NVIDIA Jetson**
- **Raspberry Pi with Hailo-8/8L** accelerators (support in progress)
- Additional platforms are continuously being added

Hardware modules are available at https://www.au-zone.com/edgefirstmodules.

## Common Commands

```bash
# Setup (use a local venv, never install globally)
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Local development server
mkdocs serve                  # http://localhost:8000/

# Spell check (strict mode — runs during CI)
mkdocs build -s

# Versioned deploy with mike (used in CI and for local verification)
mike deploy -r <branch> <version> <alias>
mike serve

# Markdown linting (used in CI)
npx markdownlint-cli2 "docs/**/*.md"
```

## Architecture

### Site Structure

- `mkdocs.yml` — Central configuration: nav structure, plugins, theme, markdown extensions
- `docs/` — All documentation content organized by product area
- `docs/.nav.yml` — Top-level navigation structure (used by `awesome-nav` plugin)
- `docs/discrete/` — Reusable doc fragments included across multiple pages (excluded from direct nav)
- `docs/includes/abbreviations.md` — Global abbreviation definitions (auto-appended to every page)
- `docs/assets/known_words.txt` — Custom dictionary for the spellcheck plugin
- `overrides/main.html` — Jinja2 template override (announcement banner linking back to Studio)
- `docs/stylesheets/extra.css` — EdgeFirst brand colors and theme customizations
- `images_with_layers.pptx` — Source PowerPoint for documentation images with editable layers

### Discrete Documentation Pattern

This is the most important architectural pattern. Reusable content lives in `docs/discrete/` and is included via:

```markdown
{% include-markdown "discrete/models/train_vision.md" heading-offset=0 %}
```

This allows a single source of truth for content that appears in multiple pages. The `include-markdown` plugin handles relative URL rewriting. The `docs/discrete/` directory is excluded from direct site output via `exclude_docs: /discrete` in `mkdocs.yml`.

### Versioned Deployment (mike)

The site uses `mike` for version management. Three branches auto-deploy via CI:

| Branch | Purpose |
|--------|---------|
| `test` | Testing/preview |
| `stage` | Staging |
| `saas` | Production (set as `latest` default) |

CI runs on push to these branches (`.github/workflows/publish.yml`), deploys to GitHub Pages via `gh-pages` branch.

### Key Plugins

- **awesome-nav**: Navigation from `.nav.yml` files
- **include-markdown**: Discrete doc inclusion with `rewrite_relative_urls: true` and `heading_offset: 1`
- **mkdocstrings**: Python API reference generation (used for Perception API docs)
- **spellcheck**: symspellpy + codespell backends with `known_words.txt` dictionary; strict mode only
- **social**: Auto-generates social cards with navy (#3E3371) background

## Conventions

- Filenames must be **lowercase** (no "Projects", use "projects")
- Images go in a local `assets/` subfolder alongside the doc that uses them
- Use descriptive image names (never "image-1")
- No screenshots from private customer data — use Au-Zone/EdgeFirst datasets only
- Use `images_with_layers.pptx` for images that need annotations/drawings (1005x660 for Studio home screenshots)
- Remove unused images from assets folders
- Add new technical terms to `docs/assets/known_words.txt` to pass spellcheck
- New abbreviations should be added to `docs/includes/abbreviations.md`
- Navigation pages use `{% include-markdown %}` for wizard-style flows with prev/next buttons at the bottom
