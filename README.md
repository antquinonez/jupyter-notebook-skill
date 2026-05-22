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
- **Analytical honesty** — negative results get less space, executive summaries argue rather than summarize
- **Full validation** — `exec()`-based notebook runner with multi-CWD testing

## Install

Clone this repo, then install the skill for your agent:

### opencode

```bash
# Option A: Project-level
cp -r jupyter-notebook .opencode/skills/jupyter-notebook

# Option B: Global
cp -r jupyter-notebook ~/.config/opencode/skills/jupyter-notebook

# Option C: Reference via config (opencode.json)
# Add to "skills.paths" the parent directory containing jupyter-notebook/
```

### Claude Code

```bash
# Option A: Project-level
cp -r jupyter-notebook .claude/skills/jupyter-notebook

# Option B: Global
cp -r jupyter-notebook ~/.claude/skills/jupyter-notebook
```

### Google Antigravity CLI (formerly Gemini CLI)

```bash
# Option A: Project-level
cp -r jupyter-notebook .gemini/skills/jupyter-notebook
# or the interoperable alias:
cp -r jupyter-notebook .agents/skills/jupyter-notebook

# Option B: Global
cp -r jupyter-notebook ~/.gemini/skills/jupyter-notebook
# or:
cp -r jupyter-notebook ~/.agents/skills/jupyter-notebook

# Option C: Install from Git
antigravity skills install https://github.com/YOUR-USER/ff-jupyter-skill.git --path jupyter-notebook
```

### Mistral Vibe

```bash
# Option A: Project-level
cp -r jupyter-notebook .vibe/skills/jupyter-notebook

# Option B: Global
cp -r jupyter-notebook ~/.vibe/skills/jupyter-notebook
```

### Other compatible agents

Any tool that follows the [Agent Skills specification](https://agentskills.io/specification) will discover skills in their respective skills directory. The format is always the same:

```
<skills-dir>/jupyter-notebook/SKILL.md
```

## Skill structure

```
jupyter-notebook/
└── SKILL.md       # Metadata + full instructions
```

## License

MIT
