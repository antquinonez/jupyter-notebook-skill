"""Execute a notebook via nbconvert --execute, embedding outputs in the file.

Usage:
    python nb_execute.py <notebook.ipynb> [--timeout 120] [--output <path>]

Runs the notebook inside a real IPython kernel via nbconvert, which handles
async code, IPython display, and other features that exec() cannot. The
executed outputs (print output, display data, errors) are written back into
the .ipynb file.

Uses an empty JUPYTER_CONFIG_DIR to bypass broken global configs (e.g.,
~/.jupyter/jupyter_nbconvert_config.json referencing missing packages).
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def execute_notebook(
    nb_path: str,
    timeout: int = 120,
    output: str | None = None,
) -> None:
    resolved = Path(nb_path).resolve()
    if not resolved.is_file():
        print(f"Error: notebook not found: {resolved}", file=sys.stderr)
        sys.exit(1)

    # Use a temp directory that we clean up after execution.
    # This avoids polluting /tmp with leftover empty_jupyter_config_* dirs.
    config_dir = tempfile.mkdtemp(prefix="empty_jupyter_config_")
    try:
        # --output determines the filename nbconvert writes to. By default
        # it writes to the same directory as the input, overwriting it.
        output_name = output if output else resolved.name

        cmd = [
            sys.executable,
            "-m", "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            f"--ExecutePreprocessor.timeout={timeout}",
            str(resolved),
            "--output", output_name,
        ]

        env = {**os.environ, "JUPYTER_CONFIG_DIR": config_dir}

        result = subprocess.run(
            cmd, env=env, capture_output=True, text=True, check=False,
        )

        if result.returncode != 0:
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            if result.stdout:
                print(result.stdout)
            sys.exit(1)

        # Report the output location
        out_path = resolved.parent / output_name
        print(f"Executed: {out_path}")
    finally:
        # Always clean up the temp config dir
        shutil.rmtree(config_dir, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execute notebook via nbconvert with output embedding",
    )
    parser.add_argument("notebook", help="Path to .ipynb file")
    parser.add_argument(
        "--timeout", type=int, default=120,
        help="Execution timeout in seconds (default: 120)",
    )
    parser.add_argument(
        "--output",
        help="Output filename (default: overwrite input file)",
    )
    args = parser.parse_args()
    execute_notebook(args.notebook, args.timeout, args.output)


if __name__ == "__main__":
    main()
