"""Validate a notebook by running all code cells via exec().

Usage:
    python nb_validate.py <notebook.ipynb> [--cwd <dir>] [--verbose] [--traceback]

Exits 0 on success, 1 on any cell failure. Uses a shared exec_globals dict
across all cells to mimic Jupyter's shared namespace.

The --cwd flag changes directory before execution, which is useful for testing
CWD-dependent imports (see Import Robustness Rule 3 in SKILL.md).

The --verbose flag prints each cell as it executes.
The --traceback flag prints full tracebacks on failure.
"""

import argparse
import os
import sys
import traceback
from pathlib import Path

import nbformat


class ValidationError(Exception):
    """Raised when a notebook cell fails during exec() validation."""

    def __init__(self, cell_index: int, source: str, error: Exception) -> None:
        self.cell_index = cell_index
        self.source = source
        self.error = error
        super().__init__(f"Cell {cell_index} FAILED: {error}")


def validate_notebook(
    nb_path: str,
    cwd: str | None = None,
    verbose: bool = False,
    show_traceback: bool = False,
) -> tuple[int, list[ValidationError]]:
    """Validate a notebook by executing all code cells via exec().

    Returns (executed_count, errors) so callers can decide how to handle
    failures without sys.exit.
    """
    resolved = Path(nb_path).resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Notebook not found: {resolved}")

    if cwd:
        os.chdir(cwd)
        if verbose:
            print(f"CWD set to: {cwd}")

    try:
        nb = nbformat.read(resolved, as_version=4)
    except Exception as e:
        raise ValueError(f"Error reading notebook: {e}") from e

    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    if not code_cells:
        return 0, []

    exec_globals: dict = {"__name__": "__main__"}
    executed = 0
    errors: list[ValidationError] = []

    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue

        source = cell.source.strip()
        if not source:
            if verbose:
                print(f"Cell {i}: (empty, skipped)")
            continue

        executed += 1
        if verbose:
            preview = source.split("\n")[0][:60]
            print(f"Cell {i}: {preview}...")

        try:
            exec(cell.source, exec_globals)
        except Exception as e:
            errors.append(ValidationError(i, cell.source, e))
            if show_traceback:
                traceback.print_exc()
            break

    return executed, errors


def _print_error(err: ValidationError) -> None:
    print(f"\nCell {err.cell_index} FAILED: {err.error}")
    print(f"\n--- Cell {err.cell_index} source ---")
    for line_no, line in enumerate(err.source.split("\n"), 1):
        print(f"  {line_no:3d} | {line}")
    print("---")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate notebook cells via exec()",
    )
    parser.add_argument("notebook", help="Path to .ipynb file")
    parser.add_argument("--cwd", help="Change to this directory before executing")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print progress for each cell",
    )
    parser.add_argument(
        "--traceback",
        action="store_true",
        help="Print full tracebacks on failure",
    )
    args = parser.parse_args()

    try:
        executed, errors = validate_notebook(
            args.notebook, args.cwd, args.verbose, args.traceback,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if errors:
        for err in errors:
            _print_error(err)
        sys.exit(1)

    if executed == 0:
        print("Warning: no code cells found in notebook", file=sys.stderr)
        return

    cwd_info = f" (CWD = {args.cwd})" if args.cwd else ""
    print(f"All {executed} code cells executed successfully{cwd_info}")


if __name__ == "__main__":
    main()
