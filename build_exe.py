"""Build a Windows executable with PyInstaller.

Usage:
    python build_exe.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys


def main() -> int:
    pyinstaller = shutil.which("pyinstaller")
    if not pyinstaller:
        print("PyInstaller is not installed. Install with: pip install pyinstaller")
        return 1

    cmd = [
        pyinstaller,
        "--noconfirm",
        "--windowed",
        "--name",
        "AnimaticBuilder",
        "--paths",
        "src",
        "src/animatic_builder/__main__.py",
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("Build complete. Executable is in dist/AnimaticBuilder/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
