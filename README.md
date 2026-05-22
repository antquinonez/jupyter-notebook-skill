# jupyter-notebook skill

Agent Skill for creating reliable, well-structured Jupyter notebooks with AI coding agents. Prevents the most common defects: stale markdown, unverifiable output, broken imports, and missing figures.

Based on the [Agent Skills](https://agentskills.io) open standard. Works with any compatible agent.

## What it covers

- **nbformat workflow** — generate and edit `.ipynb` files programmatically, never by hand-editing JSON
- **Write-Run-Describe rule** — run code first, write markdown second, verify agreement
- **AI-readable output** — every code cell emits `print()` or `display()` output the agent can verify
- **Visualization best practices** — print data tables before plotting, use plotly/seaborn over raw matplotlib
- **Import robustness** — project root discovery, sibling imports, multi-CWD validation
- **PDF/HTML export** — embedded figures, CSS formatting, context-aware `display()`
- **Full validation** — `exec()`-based notebook runner with multi-CWD testing

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
antigravity skills install https://github.com/YOUR-USER/ff-jupyter-skill.git --path jupyter-notebook
```

## Skill structure

```
jupyter-notebook/
└── SKILL.md       # Metadata + full instructions
```

## License

MIT
