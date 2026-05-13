#!/usr/bin/env python3
"""Fetch Last.fm chart.getTopArtists and/or geo.getTopArtists into separate CSV files."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import Any

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pull Last.fm chart and/or geo top artists into separate CSV files."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Number of artists to fetch per endpoint/country (default: 50)",
    )
    parser.add_argument(
        "--outdir",
        default=".",
        help="Output directory for CSV files (default: current directory)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--global-only",
        action="store_true",
        help="Only fetch chart.getTopArtists (one CSV)",
    )
    mode.add_argument(
        "--geo-only",
        action="store_true",
        help="Only fetch geo.getTopArtists (one CSV)",
    )
    return parser.parse_args()


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fetch_artists_for_method(
    method: str, params: dict[str, Any], limit: int
) -> list[dict[str, Any]]:
    from lastfm_api import lastfm_call

    if limit <= 0:
        return []

    per_page = min(200, limit)
    page = 1
    remaining = limit
    rows: list[dict[str, Any]] = []

    while remaining > 0:
        req_params = dict(params)
        req_params.update(
            {
                "limit": min(per_page, remaining),
                "page": page,
            }
        )
        payload = lastfm_call(method, req_params)

        artists_block = payload.get("artists", {})
        artists = artists_block.get("artist", [])
        if not artists:
            break

        if isinstance(artists, dict):
            artists = [artists]

        for i, item in enumerate(artists, start=len(rows) + 1):
            attrs = item.get("@attr", {})
            rows.append(
                {
                    "rank": _to_int(attrs.get("rank"), default=i),
                    "name": item.get("name", ""),
                    "playcount": _to_int(item.get("playcount")),
                    "listeners": _to_int(item.get("listeners")),
                    "mbid": item.get("mbid", ""),
                    "url": item.get("url", ""),
                }
            )

        remaining = limit - len(rows)
        page += 1

        if len(artists) < per_page:
            break

    return rows[:limit]


def fetch_global_top_artists(limit: int) -> list[dict[str, Any]]:
    return _fetch_artists_for_method("chart.gettopartists", {}, limit)


def _country_name_candidates() -> list[str]:
    try:
        import pycountry  # pyright: ignore[reportMissingImports]
    except ImportError as exc:
        raise RuntimeError(
            "pycountry is required to discover all country names. Install it with:\n"
            "  pip install pycountry"
        ) from exc

    names: set[str] = set()
    for country in pycountry.countries:
        name = getattr(country, "name", "")
        if name:
            names.add(name)
        official = getattr(country, "official_name", "")
        if official:
            names.add(official)

    # Common aliases that Last.fm often expects instead of official naming.
    names.update(
        {
            "United States",
            "Russia",
            "South Korea",
            "North Korea",
            "Vietnam",
            "Iran",
            "Bolivia",
            "Syria",
            "Venezuela",
            "Tanzania",
            "Moldova",
            "Czech Republic",
            "Taiwan",
        }
    )

    return sorted(names)


def fetch_geo_top_artists_all_countries(limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for country in _country_name_candidates():
        try:
            country_rows = _fetch_artists_for_method(
                "geo.gettopartists", {"country": country}, limit
            )
        except RuntimeError:
            # Skip countries Last.fm does not recognize.
            continue

        if not country_rows:
            continue

        for row in country_rows:
            row["country"] = country
            rows.append(row)

    return rows


def _outdir_path(outdir: str) -> Path:
    path = Path(outdir).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_chart_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["rank", "name", "playcount", "listeners", "mbid", "url"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_geo_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["country", "rank", "name", "playcount", "listeners", "mbid", "url"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = _outdir_path(args.outdir)

    if not args.geo_only:
        chart_rows = fetch_global_top_artists(args.limit)
        chart_path = base / f"lastfm_chart_top_artists_{ts}.csv"
        write_chart_csv(chart_path, chart_rows)
        print(f"Wrote {len(chart_rows)} rows to {chart_path}")

    if not args.global_only:
        geo_rows = fetch_geo_top_artists_all_countries(args.limit)
        geo_path = base / f"lastfm_geo_top_artists_{ts}.csv"
        write_geo_csv(geo_path, geo_rows)
        print(f"Wrote {len(geo_rows)} rows to {geo_path}")


if __name__ == "__main__":
    main()
