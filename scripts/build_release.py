#!/usr/bin/env python3
"""Build a deterministic ZIP release for sharing andashi."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "plugins/andashi/.codex-plugin/plugin.json"
DIST = ROOT / "dist"
EXCLUDED_PARTS = {".git", "dist", "__pycache__", ".pytest_cache", ".venv"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".DS_Store"}


def release_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        if not path.is_file() or path.suffix in EXCLUDED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.as_posix())


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], check=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    version = manifest["version"]
    archive_root = f"andashi-{version}"
    DIST.mkdir(exist_ok=True)
    output = DIST / f"andashi-{version}.zip"

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in release_files():
            relative = source.relative_to(ROOT)
            info = zipfile.ZipInfo(f"{archive_root}/{relative.as_posix()}")
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes(), compresslevel=9)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    checksum = output.with_suffix(output.suffix + ".sha256")
    checksum.write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    print(output)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
