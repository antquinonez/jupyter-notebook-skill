from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "skills" / "jupyter-notebook" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def make_notebook(cells: list[tuple[str, str]]) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    for cell_type, source in cells:
        if cell_type == "code":
            nb.cells.append(nbf.v4.new_code_cell(source))
        else:
            nb.cells.append(nbf.v4.new_markdown_cell(source))
    return nb


def write_notebook(nb: nbf.NotebookNode, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        nbf.write(nb, f)
    return path


@pytest.fixture
def tmp_nb_dir(tmp_path: Path) -> Path:
    return tmp_path / "notebooks"


@pytest.fixture
def valid_notebook(tmp_nb_dir: Path) -> Path:
    nb = make_notebook([
        ("markdown", "# Valid Notebook\n"),
        ("code", 'x = 42\nprint(f"x = {x}")'),
        ("code", 'y = x * 2\nprint(f"y = {y}")'),
        ("markdown", "## Results\n"),
        ("code", 'print(f"Sum: {x + y}")'),
    ])
    return write_notebook(nb, tmp_nb_dir / "valid.ipynb")


@pytest.fixture
def error_cell_notebook(tmp_nb_dir: Path) -> Path:
    nb = make_notebook([
        ("code", 'a = 1\nprint(f"a = {a}")'),
        ("code", 'b = 2\nprint(f"b = {b}")'),
        ("code", 'raise ValueError("deliberate error")'),
        ("code", 'print("never reached")'),
    ])
    return write_notebook(nb, tmp_nb_dir / "error_cell.ipynb")


@pytest.fixture
def empty_code_cells_notebook(tmp_nb_dir: Path) -> Path:
    nb = make_notebook([
        ("code", 'print("first")'),
        ("code", ""),
        ("code", "   \n  \n"),
        ("code", 'print("last")'),
    ])
    return write_notebook(nb, tmp_nb_dir / "empty_cells.ipynb")


@pytest.fixture
def markdown_only_notebook(tmp_nb_dir: Path) -> Path:
    nb = make_notebook([
        ("markdown", "# No Code Here\n"),
        ("markdown", "Just text.\n"),
    ])
    return write_notebook(nb, tmp_nb_dir / "markdown_only.ipynb")


@pytest.fixture
def shared_state_notebook(tmp_nb_dir: Path) -> Path:
    nb = make_notebook([
        ("code", 'shared_list = [1, 2, 3]'),
        ("code", 'shared_list.append(4)'),
        ("code", 'print(f"list: {shared_list}")\nassert shared_list == [1, 2, 3, 4]'),
    ])
    return write_notebook(nb, tmp_nb_dir / "shared_state.ipynb")


@pytest.fixture
def triple_quote_notebook(tmp_nb_dir: Path) -> Path:
    nb = make_notebook([
        ("code", 'yaml_content = """\nname: test\nvalue: 42\n"""\nprint(yaml_content.strip())'),
    ])
    return write_notebook(nb, tmp_nb_dir / "triple_quote.ipynb")


@pytest.fixture
def fstring_notebook(tmp_nb_dir: Path) -> Path:
    nb = make_notebook([
        ("code", 'name = "world"\nprint(f"hello {name}")'),
        ("code", 'data = {"key": "value"}\nprint(f"data: {data}")'),
    ])
    return write_notebook(nb, tmp_nb_dir / "fstring.ipynb")


@pytest.fixture
def nonlocal_notebook(tmp_nb_dir: Path) -> Path:
    """Notebook that uses a generator script pattern with helper functions."""
    nb = nbf.v4.new_notebook()
    nb.cells = []

    def code(s):
        nb.cells.append(nbf.v4.new_code_cell(s))

    def md(s):
        nb.cells.append(nbf.v4.new_markdown_cell(s))

    md("# Generated Notebook\n")
    code("x = 10\ny = 20\nprint(x + y)")
    md("## Done\n")
    return write_notebook(nb, tmp_nb_dir / "generated.ipynb")
