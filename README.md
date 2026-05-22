# jupyter-notebook skill

Agent Skill for creating reliable, well-structured Jupyter notebooks with AI coding agents. Works with any [Agent Skills](https://agentskills.io)-compatible tool.

## The problem

AI agents are bad at writing Jupyter notebooks. Not because they can't write code, but because notebooks have properties that defeat the typical agent workflow:

- **The agent can't see its own output.** Charts, HTML tables, and interactive widgets are opaque. The agent writes markdown describing results it never verified.
- **Notebooks share mutable state across cells.** Editing one cell can silently break downstream cells or invalidate markdown in other sections.
- **Imports break unpredictably.** The working directory differs between validation, Jupyter, and the agent's own execution environment.
- **Figures vanish in exports.** Matplotlib's Agg backend and missing static exports produce empty PDFs.

Existing notebook skills focus on mechanical operations — scaffolding, converting, reading JSON. None of them address these reliability problems.

## What this skill does differently

This skill teaches the agent a disciplined workflow that prevents defects at the source:

- **Write-Run-Describe rule** — the agent runs code first, reads the actual output, then writes markdown to match. No more "8 clusters" when the code outputs 12.
- **AI-readable output** — every code cell emits `print()` output the agent can verify. No bare `df` expressions or invisible rich displays.
- **Data tables before charts** — the agent prints the underlying data before plotting, so it can verify what the visualization shows.
- **Full-notebook review after edits** — re-run and re-read the entire notebook after any code change to catch cascading failures.
- **Import robustness** — project root discovery and sibling imports that work across all execution environments.
- **PDF-ready output** — context-aware `display()`, embedded figures, CSS formatting for clean exports.
- **Validated execution** — `exec()`-based runner with multi-CWD testing to catch environment-specific failures.

## What this skill does not cover

This skill is focused on **notebook reliability**. For other notebook tasks, consider pairing it with:

| Need | Recommendation |
|------|---------------|
| Scaffold new notebooks from templates | [openai/skills](https://github.com/openai/skills) `jupyter-notebook` |
| Interact with a live Jupyter kernel | [hamelsmu/hamelnb](https://github.com/hamelsmu/hamelnb) `live-kernel` |
| Clean up and refactor messy notebooks | [Dexploarer/claudius-skills](https://github.com/Dexploarer/claudius-skills) `jupyter-assistant` |
| Convert notebooks to marimo | [marimo-team/skills](https://github.com/marimo-team/skills) `jupyter-to-marimo` |

## Install

### The easy way: ask your AI

Most AI coding agents can install skills for you. Clone or download this repo, then open your agent and say:

> Add the skill in the `jupyter-notebook/` folder of this repo.

Your agent knows where its own skills directory lives and will copy it to the right place. This works for opencode, Claude Code, Google Antigravity CLI, Mistral Vibe, and any other [Agent Skills](https://agentskills.io)-compatible tool.

### The manual way: per-tool paths

If you prefer to install manually, copy the `jupyter-notebook/` folder into your tool's skills directory:

| Tool | Project-level | Global |
|------|--------------|--------|
| **opencode** | `.opencode/skills/` | `~/.config/opencode/skills/` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` |
| **Google Antigravity CLI** | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` |
| **Mistral Vibe** | `.vibe/skills/` | `~/.vibe/skills/` |

For any other tool following the [Agent Skills specification](https://agentskills.io/specification), the pattern is the same:

```
<skills-dir>/jupyter-notebook/SKILL.md
```

### Install from Git (Antigravity CLI)

```bash
antigravity skills install https://github.com/antquinonez/jupyter-notebook-skill.git --path jupyter-notebook
```

## Skill structure

```
jupyter-notebook/
└── SKILL.md       # Metadata + full instructions
```

## License

MIT
