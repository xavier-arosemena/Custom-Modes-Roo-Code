# Roo+ Custom Modes Integration

This directory is a **git submodule** pointing to the [`Custom-Modes-Roo-Code`](https://github.com/jtgsystems/Custom-Modes-Roo-Code) repository (forked at [`xavier-arosemena/Custom-Modes-Roo-Code`](https://github.com/xavier-arosemena/Custom-Modes-Roo-Code)).

It provides the **single canonical mode catalog** for Roo+: **301 specialized modes** in [`custom_modes.d/`](custom_modes.d/), of which **90 curated modes** are automatically pre-loaded into Roo+'s [`.roomodes`](/.roomodes) file.

## Canonical Model

Roo+ uses **one canonical catalog** and **two user-facing lists**:

| Layer | Location | Contents |
|-------|----------|----------|
| **Canonical catalog** | [`custom_modes.d/`](custom_modes.d/) | All **301 modes**, organized as `<category>/<slug>.yaml` (each file wraps a `customModes:` array) |
| **List 1 — Preloaded** | [`.roomodes`](/.roomodes) + [`pre-installed-modes.yml`](/src/assets/marketplace/pre-installed-modes.yml) | **90 curated modes**, selected by [`manifest.json`](manifest.json) |
| **List 2 — Marketplace** | [`modes.yml`](/src/assets/marketplace/modes.yml) | **301 items** = the full 301-mode catalog |

The built-in Roo+ modes (`architect`, `code`, `ask`, `debug`, `orchestrator`) are **excluded from all lists** — they are provided by the extension core and are never shipped from this catalog.

## What's Inside

| Path | Contents |
|------|----------|
| [`custom_modes.d/`](custom_modes.d/) | **Canonical catalog** — 301 mode YAML files organized by category (90 curated) |
| [`manifest.json`](manifest.json) | **Curation manifest** — controls which of the 301 modes are pre-loaded |
| [`AGENT_CATALOG.md`](AGENT_CATALOG.md) | Full per-mode listing (slug, name, category, description, pre-load status) |

The legacy `agents/` catalog, `vs-code/` conversion tooling, the monolithic `custom_modes.yaml`, the split `.roomodes.00–10` batch artifacts, and `passing_slugs.txt` have been **removed**. [`custom_modes.d/`](custom_modes.d/) is the single source of truth.

## Sync Pipeline

[`custom_modes.d/`](custom_modes.d/) is the source of truth. The sync pipeline (run from the parent repo root) regenerates all user-facing artifacts:

```bash
# 1. Regenerate .roomodes, pre-installed-modes.yml, and modes.yml from custom_modes.d/ + manifest.json
node scripts/sync-custom-modes.mjs

# 2. Regenerate AGENT_CATALOG.md
node scripts/generate-catalog.mjs
```

| Command (from the parent repo) | Regenerates |
|-------------------------------|-------------|
| `pnpm run sync:custom-modes` | `.roomodes`, `src/assets/marketplace/pre-installed-modes.yml`, `src/assets/marketplace/modes.yml` |
| `pnpm run custom-modes:catalog` | `custom-modes/AGENT_CATALOG.md` |
| `pnpm run custom-modes:update` | Pulls the submodule, then runs `sync:custom-modes` |

## Curation

The [`manifest.json`](manifest.json) file controls which of the 301 catalog modes are pre-loaded. The current curation selects exactly **90 modes**:

- **`includeCategories`**: Set to `"all"` to include every mode in that category directory (currently empty — all curation is via individual slugs)
- **`includeSlugs`**: List specific mode slugs to include individually
- **`excludeSlugs`**: List mode slugs to exclude (overrides both of the above)

### Adding a new mode

1. Create or edit the mode's YAML at [`custom_modes.d/<category>/<slug>.yaml`](custom_modes.d/) (wrapped in a `customModes:` array)
2. To pre-load it, add the mode's `slug` to `includeSlugs` in [`manifest.json`](manifest.json)
3. Run `node scripts/sync-custom-modes.mjs` from the parent repo

### Removing a pre-loaded mode

1. Add the mode's `slug` to `excludeSlugs` in [`manifest.json`](manifest.json)
2. Run `node scripts/sync-custom-modes.mjs` from the parent repo

## Manual Import via Roo Code UI

You can also import any catalog mode directly through the Roo Code UI:

1. Open the mode selector in VS Code
2. Click "Import Mode"
3. Select the mode YAML file from [`custom_modes.d/`](custom_modes.d/)
4. The mode is added to your global custom modes

## Contributing Back Upstream

If you improve a mode configuration or add a new one:

1. Commit changes within this submodule: `cd custom-modes && git add ... && git commit`
2. Push to your fork: `git push origin main`
3. Open a PR to [`jtgsystems/Custom-Modes-Roo-Code`](https://github.com/jtgsystems/Custom-Modes-Roo-Code)

## First-Time Clone

When cloning Roo+ for the first time, initialize the submodule:

```bash
git submodule update --init --recursive
```
