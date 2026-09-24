"""Package test logs for CI artifact upload."""

from pathlib import Path
from shutil import make_archive


def main() -> None:
    workspace = Path.cwd()
    logs = workspace / "test_logs"
    if not logs.is_dir():
        raise SystemExit(f"Test-log directory not found: {logs}")

    archive = make_archive(str(workspace / "test_logs"), "zip", workspace, "test_logs")


if __name__ == "__main__":
    main()
