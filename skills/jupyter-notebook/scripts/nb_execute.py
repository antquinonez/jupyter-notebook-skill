"""Execute a notebook via papermill, embedding outputs in the file.

Usage:
    python nb_execute.py <notebook.ipynb> [--timeout 120] [--kernel python3]

Overwrites the input file with the executed version (outputs embedded).
Papermill is preferred over nbconvert for execution because:
  - Auto-detects kernels with -k fallback (defaults to python3)
  - Reports which cell failed with full traceback
  - Ignores broken ~/.jupyter/ config (no JUPYTER_CONFIG_DIR bypass needed)
"""

import argparse
import os
import sys

import papermill as pm


class ExecutionError(Exception):
    """Raised when a notebook cell fails during papermill execution."""

    def __init__(self, exec_count: int, ename: str, evalue: str) -> None:
        self.exec_count = exec_count
        self.ename = ename
        self.evalue = evalue
        super().__init__(f"Cell [{exec_count}] FAILED: {ename} {evalue}")


def execute_notebook(
    nb_path: str, timeout: int = 120, kernel: str = "python3",
) -> str:
    """Execute a notebook via papermill, returning the output path.

    Raises ExecutionError on cell failure so callers can handle it
    without sys.exit.
    """
    resolved = os.path.abspath(nb_path)

    try:
        pm.execute_notebook(
            resolved,
            resolved,
            kernel_name=kernel,
            execution_timeout=timeout,
        )
    except pm.PapermillExecutionError as e:
        raise ExecutionError(e.exec_count, e.ename, e.evalue) from e

    return resolved


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute notebook via papermill with output embedding"
    )
    parser.add_argument("notebook", help="Path to .ipynb file")
    parser.add_argument(
        "--timeout", type=int, default=120, help="Execution timeout in seconds"
    )
    parser.add_argument(
        "--kernel", default="python3", help="Kernel name (default: python3)"
    )
    args = parser.parse_args()

    try:
        output = execute_notebook(args.notebook, args.timeout, args.kernel)
    except ExecutionError as e:
        print(f"Cell [{e.exec_count}] FAILED:", file=sys.stderr)
        print(e.ename, e.evalue, file=sys.stderr)
        sys.exit(1)

    print(f"Executed: {output}")


if __name__ == "__main__":
    main()
