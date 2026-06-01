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


def validate_notebook(
    nb_path: str,
    cwd: str | None = None,
    verbose: bool = False,
    show_traceback: bool = False,
) -> None:
    resolved = Path(nb_path).resolve()
    if not resolved.is_file():
        print(f"Error: notebook not found: {resolved}", file=sys.stderr)
        sys.exit(1)

    if cwd:
        os.chdir(cwd)
        if verbose:
            print(f"CWD set to: {cwd}")

    # Validate notebook structure before executing
    try:
        nb = nbformat.read(resolved, as_version=4)
    except Exception as e:
        print(f"Error reading notebook: {e}", file=sys.stderr)
        sys.exit(1)

    # Warn on empty notebooks
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    if not code_cells:
        print("Warning: no code cells found in notebook", file=sys.stderr)
        return

    exec_globals: dict = {"__name__": "__main__"}
    executed = 0

    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue

        # Skip empty code cells
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
            print(f"\nCell {i} FAILED: {e}")
            # Show the failing cell source for context
            print(f"\n--- Cell {i} source ---")
            for line_no, line in enumerate(cell.source.split("\n"), 1):
                print(f"  {line_no:3d} | {line}")
            print("---")
            if show_traceback:
                traceback.print_exc()
            sys.exit(1)

    cwd_info = f" (CWD = {cwd})" if cwd else ""
    print(f"All {executed} code cells executed successfully{cwd_info}")


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
    validate_notebook(args.notebook, args.cwd, args.verbose, args.traceback)


if __name__ == "__main__":
    main()
