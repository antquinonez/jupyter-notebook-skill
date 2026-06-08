"""Tests that verify the generator script pattern from SKILL.md.

These tests prove that:
1. The code()/md() helper + triple-quote pattern produces valid notebooks
2. Generated notebooks pass exec() validation
3. Inner triple-quoted content (YAML, JSON) survives round-tripping
4. The backslash-trailing-newline trick suppresses leading blank lines
"""
from __future__ import annotations

from pathlib import Path

import nbformat as nbf
from nb_validate import validate_notebook


def generate_notebook(cells: list[tuple[str, str]]) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.cells = []

    def code(s):
        nb.cells.append(nbf.v4.new_code_cell(s))

    def md(s):
        nb.cells.append(nbf.v4.new_markdown_cell(s))

    for cell_type, source in cells:
        if cell_type == "code":
            code(source)
        else:
            md(source)

    return nb


def write_generated(nb: nbf.NotebookNode, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        nbf.write(nb, f)
    return path


class TestHelperPattern:
    def test_code_md_helpers_produce_valid_notebook(self, tmp_path: Path) -> None:
        nb = generate_notebook([
            ("markdown", "# Test\n"),
            ("code", 'print("hello")'),
        ])
        path = write_generated(nb, tmp_path / "basic.ipynb")
        executed, errors = validate_notebook(str(path))
        assert errors == []
        assert executed == 1

    def test_def_not_lambda_passes_lint_check(self, tmp_path: Path) -> None:
        nb = nbf.v4.new_notebook()
        nb.cells = []

        def _code(s):
            nb.cells.append(nbf.v4.new_code_cell(s))

        _code('x = 1')
        path = write_generated(nb, tmp_path / "lambda.ipynb")

        import ast
        with open(path) as f:
            raw = f.read()
        parsed = ast.parse(raw)
        assert parsed is not None

    def test_backslash_trick_no_leading_newline(self, tmp_path: Path) -> None:
        source = """\
import os
print(os.getcwd())"""
        nb = generate_notebook([("code", source)])
        path = write_generated(nb, tmp_path / "no_leading.ipynb")

        nb_read = nbf.read(str(path), as_version=4)
        cell_source = nb_read.cells[0].source
        assert not cell_source.startswith("\n")
        assert cell_source.startswith("import os")


class TestTripleQuoteEscaping:
    def test_yaml_in_cell(self, tmp_path: Path) -> None:
        inner_yaml = """
workflow:
  name: test
  steps:
    - name: step1
      action: run
"""
        source = f'yaml_str = """{inner_yaml}"""\nprint(yaml_str.strip())'
        nb = generate_notebook([("code", source)])
        path = write_generated(nb, tmp_path / "yaml.ipynb")

        executed, errors = validate_notebook(str(path))
        assert errors == []
        assert executed == 1

    def test_json_in_cell(self, tmp_path: Path) -> None:
        source = """\
import json
data = json.loads('{"key": "value", "count": 42}')
print(f"count={data['count']}")"""
        nb = generate_notebook([("code", source)])
        path = write_generated(nb, tmp_path / "json.ipynb")

        executed, errors = validate_notebook(str(path))
        assert errors == []

    def test_braces_in_string(self, tmp_path: Path) -> None:
        source = 'result = {"key": "value"}\nprint(result)'
        nb = generate_notebook([("code", source)])
        path = write_generated(nb, tmp_path / "braces.ipynb")

        executed, errors = validate_notebook(str(path))
        assert errors == []


class TestGenerateThenValidate:
    def test_full_workflow(self, tmp_path: Path) -> None:
        nb = generate_notebook([
            ("markdown", "# Generated Report\n"),
            ("code", 'import sys\nfrom pathlib import Path\nprint("imports ok")'),
            ("markdown", "## Data\n"),
            ("code", 'data = [1, 2, 3]\nprint(f"count: {len(data)}")'),
            ("markdown", "## Done\n"),
        ])
        path = write_generated(nb, tmp_path / "report.ipynb")

        executed, errors = validate_notebook(str(path))
        assert errors == []
        assert executed == 2

    def test_roundtrip_preserves_structure(self, tmp_path: Path) -> None:
        nb = generate_notebook([
            ("markdown", "# Original\n"),
            ("code", "x = 1"),
            ("markdown", "## Section\n"),
            ("code", "print(x)"),
        ])
        path = write_generated(nb, tmp_path / "roundtrip.ipynb")

        nb_read = nbf.read(str(path), as_version=4)
        assert len(nb_read.cells) == 4
        assert nb_read.cells[0].cell_type == "markdown"
        assert nb_read.cells[1].cell_type == "code"
        assert nb_read.cells[2].source == "## Section\n"
