from __future__ import annotations

import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load(path: str | Path | None = None) -> dict:
    p = Path(path) if path else ROOT / "config.yaml"
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def env(name: str, default: str = "") -> str:
    """Читает .env (если есть) и переменные окружения."""
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                if k.strip() == name and v.strip():
                    return v.strip()
    return os.environ.get(name, default)
