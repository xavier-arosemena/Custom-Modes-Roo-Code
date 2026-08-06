# Per-mode configs (canonical catalog)

This directory is the **single canonical mode catalog** for the Roo+ project.

Each YAML here contains one entry under `customModes:` — the schema consumed by
`scripts/sync-custom-modes.mjs` in the parent repo. Add/edit one file per mode.

The legacy monolithic `custom_modes.yaml`, the flat `agents/` catalog and the
`vs-code/converted_modes.d/` derivative set have been **removed**; `custom_modes.d/`
is the source of truth. The parent repo regenerates `.roomodes`,
`src/assets/marketplace/pre-installed-modes.yml` and `src/assets/marketplace/modes.yml`
from this directory with:

```
node scripts/sync-custom-modes.mjs
```
