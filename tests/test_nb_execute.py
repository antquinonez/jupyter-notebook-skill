from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("papermill")  # noqa: E402

import nbformat as nbf  # noqa: E402

from conftest import make_notebook, write_notebook  # noqa: E402
from nb_execute import ExecutionError, execute_notebook  # noqa: E402


class TestSuccessfulExecution:
    def test_embeds_outputs(self, tmp_path: Path) -> None:
        nb = make_notebook([("code", 'print("hello papermill")')])
        path = write_notebook(nb, tmp_path / "simple.ipynb")

        result = execute_notebook(str(path), timeout=30)
        assert result == str(path.resolve())

        executed = nbf.read(str(path), as_version=4)
        code_cells = [c for c in executed.cells if c.cell_type == "code"]
        assert len(code_cells) == 1
        assert len(code_cells[0].outputs) > 0
        assert any("hello papermill" in str(o) for o in code_cells[0].outputs)

    def test_shared_state_across_cells(self, tmp_path: Path) -> None:
        nb = make_notebook([
            ("code", "x = 42"),
            ("code", "y = x * 2"),
            ("code", 'print(f"result: {y}")'),
        ])
        path = write_notebook(nb, tmp_path / "shared.ipynb")

        execute_notebook(str(path), timeout=30)
        executed = nbf.read(str(path), as_version=4)
        code_cells = [c for c in executed.cells if c.cell_type == "code"]
        assert any("result: 84" in str(o) for o in code_cells[2].outputs)

    def test_markdown_cells_preserved(self, tmp_path: Path) -> None:
        nb = make_notebook([
            ("markdown", "# Title\n"),
            ("code", 'print("ok")'),
            ("markdown", "## Section\n"),
        ])
        path = write_notebook(nb, tmp_path / "mixed.ipynb")

        execute_notebook(str(path), timeout=30)
        executed = nbf.read(str(path), as_version=4)
        md_cells = [c for c in executed.cells if c.cell_type == "markdown"]
        assert md_cells[0].source == "# Title\n"
        assert md_cells[1].source == "## Section\n"


class TestErrorReporting:
    def test_reports_cell_number(self, tmp_path: Path) -> None:
        nb = make_notebook([
            ("code", 'print("ok")'),
            ("code", 'raise ValueError("boom")'),
        ])
        path = write_notebook(nb, tmp_path / "fails.ipynb")

        with pytest.raises(ExecutionError) as exc_info:
            execute_notebook(str(path), timeout=30)

        assert exc_info.value.exec_count == 2
        assert exc_info.value.ename == "ValueError"
        assert "boom" in exc_info.value.evalue

    def test_import_error_reports_correctly(self, tmp_path: Path) -> None:
        nb = make_notebook([("code", "import nonexistent_module_xyz")])
        path = write_notebook(nb, tmp_path / "import_err.ipynb")

        with pytest.raises(ExecutionError) as exc_info:
            execute_notebook(str(path), timeout=30)

        assert exc_info.value.ename == "ModuleNotFoundError"

    def test_syntax_error_reports_correctly(self, tmp_path: Path) -> None:
        nb = make_notebook([("code", "def (")])
        path = write_notebook(nb, tmp_path / "syntax_err.ipynb")

        with pytest.raises(ExecutionError) as exc_info:
            execute_notebook(str(path), timeout=30)

        assert "SyntaxError" in exc_info.value.ename
