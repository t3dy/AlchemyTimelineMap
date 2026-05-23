# ALCHEMYTIMELINEMAP

An interactive timeline and map of alchemy and chemistry — 500 events spanning Late Antiquity through the early modern period. Europe, North Africa, Middle East.

**Website:** https://t3dy.github.io/AlchemyTimelineMap/

---

## Start Here

- **New to the project?** Read [`CLAUDE.md`](CLAUDE.md) (400 words — mission, routing, invariants)
- **What's built?** Read [`PHASESTATUS.md`](PHASESTATUS.md) (the only source of truth for project state)
- **Writing content?** Use [`AGENT_LOADING_STRATEGY.md`](AGENT_LOADING_STRATEGY.md) for the exact reading path for your task

## Key Directories

| Path | Purpose |
|------|---------|
| `docs/agents/` | Task-specific execution prompts and routing |
| `archive/` | Superseded files — historical record only |
| `scripts/` | Python pipeline (idempotent, SQLite-backed) |
| `staging/` | Agent output awaiting validation and ingestion |
| `site/` | Generated static HTML/CSS/JS |

## Technology

SQLite → Python pipeline → static HTML/CSS/JS → GitHub Pages. No frameworks, no runtime dependencies.

---

*Last updated: 2026-05-23*
