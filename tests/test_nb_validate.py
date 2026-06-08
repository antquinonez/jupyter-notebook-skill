from __future__ import annotations

import os
from pathlib import Path

import pytest
from nb_validate import validate_notebook


class TestValidNotebook:
    def test_passes_with_no_errors(self, valid_notebook: Path) -> None:
        executed, errors = validate_notebook(str(valid_notebook))
        assert errors == []
        assert executed == 3

    def test_shared_namespace_across_cells(self, shared_state_notebook: Path) -> None:
        executed, errors = validate_notebook(str(shared_state_notebook))
        assert errors == []
        assert executed == 3

    def test_triple_quote_strings(self, triple_quote_notebook: Path) -> None:
        executed, errors = validate_notebook(str(triple_quote_notebook))
        assert errors == []
        assert executed == 1

    def test_fstring_cells(self, fstring_notebook: Path) -> None:
        executed, errors = validate_notebook(str(fstring_notebook))
        assert errors == []
        assert executed == 2

    def test_generator_pattern_notebook(self, nonlocal_notebook: Path) -> None:
        executed, errors = validate_notebook(str(nonlocal_notebook))
        assert errors == []
        assert executed == 1


class TestErrorHandling:
    def test_reports_cell_index(self, error_cell_notebook: Path) -> None:
        executed, errors = validate_notebook(str(error_cell_notebook))
        assert len(errors) == 1
        assert errors[0].cell_index == 2
        assert "deliberate error" in str(errors[0].error)

    def test_stops_at_first_error(self, error_cell_notebook: Path) -> None:
        executed, errors = validate_notebook(str(error_cell_notebook))
        assert executed == 3
        assert len(errors) == 1

    def test_error_contains_source(self, error_cell_notebook: Path) -> None:
        _, errors = validate_notebook(str(error_cell_notebook))
        assert "deliberate error" in errors[0].source


class TestEdgeCases:
    def test_empty_code_cells_skipped(self, empty_code_cells_notebook: Path) -> None:
        executed, errors = validate_notebook(str(empty_code_cells_notebook))
        assert errors == []
        assert executed == 2

    def test_markdown_only_returns_zero_executed(self, markdown_only_notebook: Path) -> None:
        executed, errors = validate_notebook(str(markdown_only_notebook))
        assert errors == []
        assert executed == 0

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="Notebook not found"):
            validate_notebook(str(tmp_path / "nonexistent.ipynb"))

    def test_invalid_json_raises(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.ipynb"
        bad.write_text("not valid json {{{")
        with pytest.raises(ValueError, match="Error reading notebook"):
            validate_notebook(str(bad))


class TestCwdFlag:
    def test_cwd_changes_directory(self, valid_notebook: Path, tmp_path: Path) -> None:
        original = os.getcwd()
        target = str(tmp_path)
        try:
            validate_notebook(str(valid_notebook), cwd=target)
            assert os.getcwd() == target
        finally:
            os.chdir(original)

    def test_cwd_notebook_still_executes(self, valid_notebook: Path, tmp_path: Path) -> None:
        executed, errors = validate_notebook(str(valid_notebook), cwd=str(tmp_path))
        assert errors == []
        assert executed == 3
