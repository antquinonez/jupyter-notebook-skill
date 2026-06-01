"""Minimal generator script template for creating notebooks.

This is a starting point for generator scripts. The pattern:

  1. Define notebook structure with nbformat using code()/md() helpers
  2. Write the .ipynb to disk (no outputs yet)
  3. Run nb_execute.py to populate outputs via a real kernel

Copy and adapt this script:
    cp nb_template.py scripts/_nb_my_notebook.py

Run it to generate the .ipynb:
    python scripts/_nb_my_notebook.py

Then execute to populate outputs:
    python scripts/nb_execute.py examples/my_notebook/my_notebook.ipynb

Adjust the output path, cell content, and imports to match your project.
See SKILL.md "Generator Scripts" for the full pattern.
"""

from pathlib import Path

import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.cells = []


def code(s):
    """Append a code cell to the notebook."""
    nb.cells.append(nbf.v4.new_code_cell(s))


def md(s):
    """Append a markdown cell to the notebook."""
    nb.cells.append(nbf.v4.new_markdown_cell(s))


# --- Title and setup ---

md("""\
# Notebook Title

Description of what this notebook demonstrates.

<div class="page-break"></div>

---
""")

# Standard setup cell: find project root, add to sys.path, load .env
code("""\
import sys
from pathlib import Path

_cwd = Path().resolve()
_project_root = _cwd
for _p in [_cwd, *list(_cwd.parents)]:
    if (_p / 'pyproject.toml').is_file():
        _project_root = _p
        break

if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Load environment variables if .env exists
try:
    from dotenv import load_dotenv  # noqa: E402
    load_dotenv()
except ImportError:
    pass

# Add your imports here
print("Setup complete")
""")

# --- Step 1: example section ---

md("""\
<div class="page-break"></div>

---

## Step 1: Title

Description of this step.
""")

code("""\
# Your code here
print("Hello from notebook!")
""")

# --- Summary ---

md("""\
## Summary

- Point 1
- Point 2
""")

# --- Write the notebook to disk ---

output_path = Path("examples/my_notebook/my_notebook.ipynb")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w") as f:
    nbf.write(nb, f)

print(f"Created {output_path}")
