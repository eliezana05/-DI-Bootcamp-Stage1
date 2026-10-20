"""Run all nine exercises in order: python3 exercises.py."""

from pathlib import Path
import runpy


def main():
    # Each file can also be run on its own.
    folder = Path(__file__).parent
    for exercise in sorted(folder.glob("[0-9][0-9]_*.py")):
        runpy.run_path(str(exercise), run_name="__main__")


if __name__ == "__main__":
    main()
