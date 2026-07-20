# Roo+ Custom Modes Integration

This directory is a **git submodule** pointing to the [`Custom-Modes-Roo-Code`](https://github.com/jtgsystems/Custom-Modes-Roo-Code) repository (forked at [`xavier-arosemena/Custom-Modes-Roo-Code`](https://github.com/xavier-arosemena/Custom-Modes-Roo-Code)).

It provides **233** specialized AI agent configurations, with **90 curated modes** automatically pre-loaded into Roo+'s [`.roomodes`](/.roomodes) file.

## What's Inside

| Path | Contents |
|------|----------|
| [`agents/`](agents/) | 233 agent YAML files organized by category (90 curated) |
| [`vs-code/`](vs-code/) | Upstream conversion scripts |
| [`manifest.json`](manifest.json) | **Curation manifest** — controls which agents appear in `.roomodes` |

## Update Workflow

When the upstream repository receives updates:

```bash
# 1. Pull latest from submodule
cd custom-modes && git checkout main && git pull origin main && cd ..

# 2. Regenerate .roomodes
pnpm run sync:custom-modes
```

Or use the combined command:

```bash
pnpm run custom-modes:update
```

## Curation

The [`manifest.json`](manifest.json) file controls which agents are included in [`.roomodes`](/.roomodes). The current curation selects exactly **90 modes**:

- **`includeCategories`**: Set to `"all"` to include every agent in that category directory (currently empty — all curation is via individual slugs)
- **`includeSlugs`**: List specific agent slugs to include individually
- **`excludeSlugs`**: List agent slugs to exclude (overrides both of the above)

### Adding a new agent

1. Find the agent's `slug` in its YAML file under [`agents/`](agents/)
2. Add the slug to `includeSlugs` in [`manifest.json`](manifest.json)
3. Run `pnpm run sync:custom-modes`

### Removing an agent

1. Add the agent's `slug` to `excludeSlugs` in [`manifest.json`](manifest.json)
2. Run `pnpm run sync:custom-modes`

## Manual Import via Roo Code UI

You can also import individual agents directly through the Roo Code UI:

1. Open the mode selector in VS Code
2. Click "Import Mode"
3. Select the agent YAML file from [`agents/`](agents/)
4. The agent is added to your global custom modes

## Contributing Back Upstream

If you improve an agent configuration or add a new one:

1. Commit changes within this submodule: `cd custom-modes && git add ... && git commit`
2. Push to your fork: `git push origin main`
3. Open a PR to [`jtgsystems/Custom-Modes-Roo-Code`](https://github.com/jtgsystems/Custom-Modes-Roo-Code)

## First-Time Clone

When cloning Roo+ for the first time, initialize the submodule:

```bash
git submodule update --init --recursive
```
