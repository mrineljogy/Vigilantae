"""Run the repository's syntax and unit-test checks locally or in CI."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    completed = subprocess.run([sys.executable, *args], cwd=ROOT, check=False)
    if completed.returncode:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    run("-m", "compileall", "-q", "Home.py", "mobile_app.py", "pages", "scripts", "tests")
    run("-m", "unittest", "discover", "-s", "tests", "-v")
    print("\nVerification passed.")
