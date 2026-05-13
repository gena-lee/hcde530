#!/usr/bin/env python3
"""Build mp1_data_snapshot.json — offline cache for MP1 notebook data (no API key in output)."""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Same folder as lastfm_api / notebook
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from lastfm_api import lastfm_call  # noqa: E402

OUT_PATH = _ROOT / "mp1_data_snapshot.json"


def _json_safe_records(df: pd.DataFrame) -> tuple[list[str], list[dict]]:
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[c]):
            df[c] = df[c].astype(str)
    records = json.loads(
        df.to_json(orient="records", date_format="iso", default_handler=str)
    )
    columns = list(df.columns)
    return columns, records


def _dataset_block(
    df: pd.DataFrame,
    *,
    role: str,
    source: str,
    notes: str = "",
) -> dict:
    cols, recs = _json_safe_records(df)
    return {
        "role": role,
        "source": source,
        "notes": notes,
        "columns": cols,
        "records": recs,
    }


def fetch_rq1_geo() -> pd.DataFrame:
    COUNTRY_QUERY = [
        ("United States", ["United States", "United States of America"]),
        ("Brazil", ["Brazil"]),
        ("South Korea", ["Korea, Republic of", "South Korea"]),
    ]
    LIMIT = 20
    parts: list[pd.DataFrame] = []
    for label, country_options in COUNTRY_QUERY:
        payload = None
        used_param = None
        for country_param in country_options:
            try:
                payload = lastfm_call(
                    "geo.gettopartists",
                    {"country": country_param, "limit": LIMIT},
                )
                used_param = country_param
                break
            except RuntimeError as exc:
                err_text = str(exc)
                if "error 6" in err_text and "country param invalid" in err_text:
                    continue
                raise
        if payload is None:
            raise RuntimeError(
                "Could not resolve country name for {!r}. Tried: {}".format(
                    label, country_options
                )
            )

        artists = payload["topartists"]["artist"]
        if isinstance(artists, dict):
            artists = [artists]
        chunk = pd.json_normalize(artists)
        chunk.insert(0, "country_label", label)
        chunk.insert(1, "country_param", used_param)
        parts.append(chunk)
        time.sleep(0.3)

    geo_top_artists = pd.concat(parts, ignore_index=True)
    df = geo_top_artists.copy()
    if "listeners" in df.columns:
        df["listeners"] = pd.to_numeric(df["listeners"], errors="coerce")
    return df


def rq1_derived(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    _df = df.copy()
    _df["rank"] = _df.groupby("country_label", sort=False).cumcount() + 1
    TOP_N = 10
    names_by_country = (
        _df.pivot(index="rank", columns="country_label", values="name")
        .head(TOP_N)
        .reset_index()
    )

    def jaccard(a: set, b: set) -> float:
        if not a and not b:
            return 1.0
        union = a | b
        if not union:
            return 0.0
        return len(a & b) / len(union)

    _sets = {
        label: set(df.loc[df["country_label"].eq(label), "name"].astype(str))
        for label in sorted(df["country_label"].unique())
    }
    countries = list(_sets.keys())

    pair_rows = []
    for i, c1 in enumerate(countries):
        for c2 in countries[i + 1 :]:
            pair_rows.append(
                {
                    "profile_country_a": c1,
                    "profile_country_b": c2,
                    "overlap_artists": len(_sets[c1] & _sets[c2]),
                    "jaccard_similarity": round(jaccard(_sets[c1], _sets[c2]), 4),
                }
            )
    pairwise_df = pd.DataFrame(pair_rows)

    unique_rows = []
    for c in countries:
        others = (
            set.union(*[_sets[o] for o in countries if o != c])
            if len(countries) > 1
            else set()
        )
        only_here = sorted(_sets[c] - others)
        unique_rows.append(
            {
                "profile_country": c,
                "artists_only_on_this_chart": len(only_here),
                "examples": ", ".join(only_here[:8])
                + ("..." if len(only_here) > 8 else ""),
            }
        )
    unique_df = pd.DataFrame(unique_rows)

    all_three = sorted(set.intersection(*_sets.values()) if len(_sets) >= 1 else set())
    overlap_meta = pd.DataFrame(
        [
            {
                "key": "artists_on_all_three_charts",
                "count": len(all_three),
                "names_csv": ", ".join(all_three),
            }
        ]
    )

    return {
        "names_by_country": names_by_country,
        "pairwise_df": pairwise_df,
        "unique_df": unique_df,
        "rq1_overlap_summary": overlap_meta,
    }


def fetch_rq2_tags() -> pd.DataFrame:
    LIMIT_TAGS = 50
    payload = lastfm_call("chart.gettoptags", {"limit": LIMIT_TAGS})
    tags_raw = payload["tags"]["tag"]
    if isinstance(tags_raw, dict):
        tags_raw = [tags_raw]
    tags_df = pd.json_normalize(tags_raw)
    for col in ("reach", "taggings"):
        if col in tags_df.columns:
            tags_df[col] = pd.to_numeric(tags_df[col], errors="coerce")
    tags_df = tags_df.sort_values("reach", ascending=False, na_position="last").reset_index(
        drop=True
    )
    return tags_df


def fetch_rq3_chart() -> pd.DataFrame:
    RQ3_TARGET_N = 100
    RQ3_PAGE_SIZE = 50
    _chart_parts: list[pd.DataFrame] = []
    _page = 1
    while sum(len(p) for p in _chart_parts) < RQ3_TARGET_N:
        payload = lastfm_call(
            "chart.gettopartists",
            {"limit": RQ3_PAGE_SIZE, "page": _page},
        )
        artists_raw = payload["artists"]["artist"]
        if isinstance(artists_raw, dict):
            artists_raw = [artists_raw]
        if not artists_raw:
            break
        _chart_parts.append(pd.json_normalize(artists_raw))
        _page += 1
        if len(artists_raw) < RQ3_PAGE_SIZE:
            break

    chart100_raw = pd.concat(_chart_parts, ignore_index=True).head(RQ3_TARGET_N)
    _name = chart100_raw["name"].astype(str).str.strip()
    if "mbid" in chart100_raw.columns:
        _mbid = chart100_raw["mbid"].astype(str).str.strip()
        _mbid = _mbid.replace({"nan": "", "None": ""})
    else:
        _mbid = pd.Series([""] * len(chart100_raw))
    chart100_raw = chart100_raw.copy()
    chart100_raw["_dedupe_key"] = _mbid.where(_mbid.ne(""), _name.str.lower())
    chart100_df = chart100_raw.drop_duplicates(subset=["_dedupe_key"], keep="first").drop(
        columns=["_dedupe_key"]
    )
    return chart100_df.reset_index(drop=True)


def _pick_artist_params(row: pd.Series) -> dict:
    mbid = row.get("mbid")
    if mbid is None or (isinstance(mbid, float) and pd.isna(mbid)):
        mbid = ""
    else:
        mbid = str(mbid).strip()
    if mbid and mbid.lower() != "nan":
        return {"mbid": mbid}
    return {"artist": str(row["name"]).strip()}


def _parse_play_listeners(info_payload: dict) -> tuple[float | None, float | None]:
    a = info_payload.get("artist") or {}
    pc = a.get("playcount")
    ls = a.get("listeners")
    stats = a.get("stats") or {}
    if pc is None:
        pc = stats.get("playcount")
    if ls is None:
        ls = stats.get("listeners")
    pc_n = pd.to_numeric(pc, errors="coerce")
    ls_n = pd.to_numeric(ls, errors="coerce")
    return pc_n, ls_n


def _primary_genre_tag(tags_payload: dict) -> str | None:
    tt = tags_payload.get("toptags") or {}
    raw = tt.get("tag")
    if raw is None:
        return None
    if isinstance(raw, dict):
        raw = [raw]
    if not raw:
        return None
    first = raw[0]
    if isinstance(first, dict):
        return first.get("name")
    return None


def fetch_rq3_enriched(chart100_df: pd.DataFrame) -> pd.DataFrame:
    RQ3_API_DELAY = 0.25
    _rows: list[dict] = []
    for _, row in chart100_df.iterrows():
        params_base = _pick_artist_params(row)
        time.sleep(RQ3_API_DELAY)
        try:
            info_pl = lastfm_call("artist.getinfo", params_base)
            playcount, listeners = _parse_play_listeners(info_pl)
        except RuntimeError:
            continue

        if listeners is None or listeners <= 0 or pd.isna(listeners):
            continue
        if playcount is None or pd.isna(playcount):
            playcount = 0.0

        time.sleep(RQ3_API_DELAY)
        try:
            tags_pl = lastfm_call("artist.gettoptags", params_base)
            gtag = _primary_genre_tag(tags_pl)
        except RuntimeError:
            continue

        if not gtag:
            continue

        ratio = float(playcount) / float(listeners)
        _rows.append(
            {
                "name": row["name"],
                "mbid": row.get("mbid"),
                "playcount": float(playcount),
                "listeners": float(listeners),
                "play_per_listener": ratio,
                "genre_tag": str(gtag),
            }
        )

    return pd.DataFrame(_rows)


def rq3_genre_summary(rq3_artists_df: pd.DataFrame) -> pd.DataFrame:
    MIN_ARTISTS_PER_TAG = 5
    _g = (
        rq3_artists_df.groupby("genre_tag", sort=False)
        .agg(
            median_play_per_listener=("play_per_listener", "median"),
            n_artists=("play_per_listener", "count"),
            sum_play=("playcount", "sum"),
            sum_listen=("listeners", "sum"),
        )
        .reset_index()
    )
    _g["weighted_play_per_listener"] = _g["sum_play"] / _g["sum_listen"]
    return _g.loc[_g["n_artists"] >= MIN_ARTISTS_PER_TAG].sort_values(
        "median_play_per_listener", ascending=False
    )


def main() -> None:
    os.chdir(_ROOT)
    print("Fetching RQ1 geo top artists...")
    df = fetch_rq1_geo()
    rq1 = rq1_derived(df)

    print("Fetching RQ2 chart.getTopTags...")
    tags_df = fetch_rq2_tags()

    print("Fetching RQ3 chart.getTopArtists (100)...")
    chart100_df = fetch_rq3_chart()

    print("Fetching RQ3 artist.getinfo + artist.getTopTags (slow)...")
    rq3_artists_df = fetch_rq3_enriched(chart100_df)

    print("Building RQ3 genre summary...")
    rq3_summary = rq3_genre_summary(rq3_artists_df)

    snapshot = {
        "_snapshot_meta": {
            "notebook": "mp1.ipynb",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "description": "Offline snapshot for MP1 (RQ1–RQ3). No API credentials stored.",
            "format": {"tabular": "columns + records (pandas orient=records)"},
        },
        "df": _dataset_block(
            df,
            role="raw",
            source="geo.getTopArtists × US / Brazil / South Korea (notebook logic)",
            notes="RQ1 base table (same as notebook `df` after listener coercion).",
        ),
        "names_by_country": _dataset_block(
            rq1["names_by_country"],
            role="derived",
            source="pivot from df",
            notes="Top 10 ranks × country columns (RQ1 wide table).",
        ),
        "pairwise_df": _dataset_block(
            rq1["pairwise_df"],
            role="derived",
            source="pairwise overlap / Jaccard on df",
        ),
        "unique_df": _dataset_block(
            rq1["unique_df"],
            role="derived",
            source="artists only on one country's chart",
        ),
        "rq1_overlap_summary": _dataset_block(
            rq1["rq1_overlap_summary"],
            role="derived",
            source="intersection of all three country sets",
        ),
        "tags_df": _dataset_block(
            tags_df,
            role="raw",
            source="chart.getTopTags",
            notes="RQ2 global tag chart.",
        ),
        "chart100_df": _dataset_block(
            chart100_df,
            role="raw",
            source="chart.getTopArtists paginated, deduped (RQ3)",
        ),
        "rq3_artists_df": _dataset_block(
            rq3_artists_df,
            role="derived",
            source="artist.getInfo + artist.getTopTags per chart row",
            notes="RQ3 per-artist play/listeners and primary tag.",
        ),
        "rq3_genre_summary": _dataset_block(
            rq3_summary,
            role="derived",
            source="groupby genre_tag on rq3_artists_df",
            notes="MIN_ARTISTS_PER_TAG=5 as in notebook.",
        ),
    }

    OUT_PATH.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
