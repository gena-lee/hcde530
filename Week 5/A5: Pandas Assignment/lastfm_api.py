"""Last.fm API helper for mp1 notebook — shared import so cells run in any order."""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path


def _parse_env_file(path: Path) -> dict:
    """Parse KEY=VALUE lines (works without python-dotenv)."""
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key:
            out[key] = val
    return out


def _candidate_env_paths() -> list[Path]:
    cwd = Path.cwd()
    paths = [
        cwd / ".env",
        cwd / "Week 5" / "A5: Pandas Assignment" / ".env",
        cwd / "A5: Pandas Assignment" / ".env",
    ]
    for parent in [cwd, *list(cwd.parents)[:10]]:
        paths.append(parent / "Week 5" / "A5: Pandas Assignment" / ".env")
        paths.append(parent / ".env")
    seen: set[Path] = set()
    uniq: list[Path] = []
    for p in paths:
        try:
            rp = p.resolve()
        except OSError:
            continue
        if rp not in seen:
            seen.add(rp)
            uniq.append(p)
    return uniq


def resolve_lastfm_api_key() -> str:
    key = (os.environ.get("LASTFM_API_KEY") or "").strip()
    if key:
        return key
    try:
        from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]

        for p in _candidate_env_paths():
            if p.is_file():
                load_dotenv(p)
                break
        key = (os.environ.get("LASTFM_API_KEY") or "").strip()
        if key:
            return key
    except ImportError:
        pass
    for p in _candidate_env_paths():
        data = _parse_env_file(p)
        key = (data.get("LASTFM_API_KEY") or "").strip()
        if key:
            return key
    raise ValueError(
        "LASTFM_API_KEY is missing or empty. Edit .env in this folder and set:\n"
        "  LASTFM_API_KEY=your_key\n"
        "(no spaces around =). Or: export LASTFM_API_KEY=your_key"
    )


API_KEY = resolve_lastfm_api_key()
BASE = "https://ws.audioscrobbler.com/2.0/"


def lastfm_call(method: str, extra: dict | None = None) -> dict:
    params = {"method": method, "api_key": API_KEY, "format": "json"}
    if extra:
        params.update(extra)
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        payload = json.load(resp)
    err = payload.get("error")
    if err is not None:
        msg = payload.get("message", str(payload))
        raise RuntimeError("Last.fm API error {}: {}".format(err, msg))
    return payload
