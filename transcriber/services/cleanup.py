from pathlib import Path
import shutil


def safe_unlink(path: str | Path) -> None:
    path = Path(path)
    try:
        if path.exists() and path.is_file():
            path.unlink()
    except Exception:
        pass


def safe_rmdir_if_empty(path: str | Path) -> None:
    path = Path(path)
    try:
        if path.exists() and path.is_dir():
            path.rmdir()
    except Exception:
        pass


def safe_rmtree(path: str | Path) -> None:
    path = Path(path)
    try:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
    except Exception:
        pass
