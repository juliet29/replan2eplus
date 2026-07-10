from pathlib import Path

import tomli_w


def get_or_make_folder_path(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_toml(item: dict, folder_path: Path, file_stem: str) -> None:
    path = folder_path / f"{file_stem}.toml"
    with open(path, "wb") as f:
        tomli_w.dump(item, f)
