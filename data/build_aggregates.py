"""Build compact, reconciled JSON aggregates for the DArts website."""

from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


EXPECTED_ARTWORKS = 144_149
EXPECTED_ARTISTS = 11_879
YEAR_RE = re.compile(r"(17\d{2}|18\d{2}|19\d{2}|20[0-2]\d|2030)")

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "moma-collection"
OUTPUT_DIR = ROOT / "website" / "public" / "data"
REPORT_PATH = DATA_DIR / "build_report.txt"

ARTWORK_KEY_COLUMNS = [
    "Title",
    "Artist",
    "ConstituentID",
    "ArtistBio",
    "Nationality",
    "BeginDate",
    "EndDate",
    "Gender",
    "Date",
    "Medium",
    "Classification",
    "Department",
]

ARTIST_KEY_COLUMNS = ["ArtistBio", "Nationality", "Gender", "BeginDate"]

ISO3_TO_COUNTRY = {
    "AFG": "Afghanistan",
    "ALB": "Albania",
    "ARE": "United Arab Emirates",
    "ARG": "Argentina",
    "AUS": "Australia",
    "AUT": "Austria",
    "AZE": "Azerbaijan",
    "BEL": "Belgium",
    "BEN": "Benin",
    "BFA": "Burkina Faso",
    "BGD": "Bangladesh",
    "BGR": "Bulgaria",
    "BHS": "Bahamas",
    "BIH": "Bosnia and Herzegovina",
    "BOL": "Bolivia",
    "BRA": "Brazil",
    "CAF": "Central African Republic",
    "CAN": "Canada",
    "CHE": "Switzerland",
    "CHL": "Chile",
    "CHN": "China",
    "CIV": "Cote d'Ivoire",
    "CMR": "Cameroon",
    "COD": "Democratic Republic of the Congo",
    "COL": "Colombia",
    "CRI": "Costa Rica",
    "CUB": "Cuba",
    "CYP": "Cyprus",
    "CZE": "Czechia",
    "DEU": "Germany",
    "DNK": "Denmark",
    "DZA": "Algeria",
    "ECU": "Ecuador",
    "EGY": "Egypt",
    "ESP": "Spain",
    "EST": "Estonia",
    "ETH": "Ethiopia",
    "FIN": "Finland",
    "FRA": "France",
    "GBR": "United Kingdom",
    "GEO": "Georgia",
    "GHA": "Ghana",
    "GRC": "Greece",
    "GTM": "Guatemala",
    "HRV": "Croatia",
    "HTI": "Haiti",
    "HUN": "Hungary",
    "IDN": "Indonesia",
    "IND": "India",
    "IRL": "Ireland",
    "IRN": "Iran",
    "IRQ": "Iraq",
    "ISL": "Iceland",
    "ISR": "Israel",
    "ITA": "Italy",
    "JAM": "Jamaica",
    "JPN": "Japan",
    "KEN": "Kenya",
    "KGZ": "Kyrgyzstan",
    "KHM": "Cambodia",
    "KOR": "South Korea",
    "KWT": "Kuwait",
    "LBN": "Lebanon",
    "LKA": "Sri Lanka",
    "LTU": "Lithuania",
    "LUX": "Luxembourg",
    "LVA": "Latvia",
    "MAR": "Morocco",
    "MEX": "Mexico",
    "MKD": "North Macedonia",
    "MLI": "Mali",
    "MOZ": "Mozambique",
    "MYS": "Malaysia",
    "NAM": "Namibia",
    "NGA": "Nigeria",
    "NIC": "Nicaragua",
    "NLD": "Netherlands",
    "NOR": "Norway",
    "NPL": "Nepal",
    "NZL": "New Zealand",
    "PAK": "Pakistan",
    "PAN": "Panama",
    "PER": "Peru",
    "PHL": "Philippines",
    "POL": "Poland",
    "PRI": "Puerto Rico",
    "PRT": "Portugal",
    "PRY": "Paraguay",
    "PSE": "Palestine",
    "ROU": "Romania",
    "RUS": "Russia",
    "SDN": "Sudan",
    "SEN": "Senegal",
    "SGP": "Singapore",
    "SLE": "Sierra Leone",
    "SLV": "El Salvador",
    "SRB": "Serbia",
    "SVK": "Slovakia",
    "SVN": "Slovenia",
    "SWE": "Sweden",
    "SYR": "Syria",
    "THA": "Thailand",
    "TTO": "Trinidad and Tobago",
    "TUN": "Tunisia",
    "TUR": "Turkey",
    "TWN": "Taiwan",
    "TZA": "Tanzania",
    "UGA": "Uganda",
    "UKR": "Ukraine",
    "URY": "Uruguay",
    "USA": "United States",
    "UZB": "Uzbekistan",
    "VEN": "Venezuela",
    "VNM": "Vietnam",
    "ZAF": "South Africa",
    "ZWE": "Zimbabwe",
}


def ascii_fold(value: str) -> str:
    """Return a plain-ASCII key for mapping unstable nationality labels."""
    folded = unicodedata.normalize("NFKD", value)
    return folded.encode("ascii", "ignore").decode("ascii")


def clean_token(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    token = str(value).strip()
    if not token:
        return None
    token = token.strip("() ").replace("–", "-").replace("—", "-")
    token = re.sub(r"\s+", " ", token)
    if not token or token == "()":
        return None
    return token


def mapping_key(value: str | None) -> str | None:
    token = clean_token(value)
    if token is None:
        return None
    token = token.split(",", 1)[0].strip()
    token = ascii_fold(token)
    if token.lower() in {"nationality unknown", "unknown", "nan"}:
        return None
    return token


def split_parenthesized(value: Any) -> list[str]:
    token = clean_token(value)
    if token is None:
        return []
    parts = re.split(r"\)\s*\(", str(value).strip())
    cleaned = [clean_token(part) for part in parts]
    return [part for part in cleaned if part is not None]


def split_ids(value: Any) -> list[int]:
    token = clean_token(value)
    if token is None:
        return []
    ids: list[int] = []
    for part in str(token).split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(float(part)))
        except ValueError:
            continue
    return ids


def parse_year(value: Any) -> int | None:
    token = clean_token(value)
    if token is None:
        return None
    match = YEAR_RE.search(token)
    return int(match.group(1)) if match else None


def decade_from_year(year: int | None) -> int | None:
    if year is None or pd.isna(year):
        return None
    return int(math.floor(year / 10) * 10)


def normalize_gender(value: Any) -> str:
    token = clean_token(value)
    if token is None:
        return "unknown"
    lower = token.lower()
    if "non-binary" in lower or "gender non-conforming" in lower:
        return "non-binary"
    if "transgender woman" in lower or "transwoman" in lower:
        return "female"
    if "female" in lower:
        return "female"
    if re.search(r"\bmale\b", lower):
        return "male"
    return "unknown"


def canonical_medium(classification: Any, medium: Any, department: Any) -> str:
    text = " ".join(
        clean_token(value) or "" for value in [classification, medium, department]
    ).lower()
    if any(term in text for term in ["photograph", "photogravure", "gelatin silver", "chromogenic"]):
        return "Photography"
    if any(term in text for term in ["print", "illustrated book", "portfolio", "periodical", "lithograph", "etching", "woodcut"]):
        return "Prints & Books"
    if any(term in text for term in ["drawing", "pencil", "ink on paper", "work on paper", "collage"]):
        return "Drawing"
    if any(term in text for term in ["architecture", "mies van der rohe", "frank lloyd wright"]):
        return "Architecture"
    if any(term in text for term in ["design", "textile", "furniture", "poster", "graphic design"]):
        return "Design"
    if "painting" in text or "oil on canvas" in text:
        return "Painting"
    if any(term in text for term in ["video", "film", "audio", "digital", "media", "software", "website", "moving image"]):
        return "Film/Video"
    if any(term in text for term in ["sculpture", "installation", "multiple"]):
        return "Sculpture"
    if "performance" in text:
        return "Performance"
    if any(term in text for term in ["archive", "ephemera", "correspondence", "document", "publication"]):
        return "Archives & Ephemera"
    return "Other"


def iso_for_nationality(value: Any, nationality_to_iso: dict[str, str]) -> str | None:
    key = mapping_key(str(value)) if value is not None and not pd.isna(value) else None
    if key is None:
        return None
    return nationality_to_iso.get(key)


def get_region(iso3: str | None, regions: dict[str, str]) -> str:
    if iso3 is None:
        return "Unknown"
    return regions.get(iso3, "Unknown")


def json_ready(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def records_from_df(df: pd.DataFrame) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in df.to_dict(orient="records"):
        records.append({key: json_ready(value) for key, value in row.items()})
    return records


def write_json(name: str, data: Any) -> None:
    path = OUTPUT_DIR / name
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def seeded_index(seed: str, length: int) -> int:
    if length <= 1:
        return 0
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % length


def lifespan(begin: int | None, end: int | None) -> str:
    begin = json_ready(begin)
    end = json_ready(end)
    if begin and end:
        return f"{begin}-{end}"
    if begin:
        return f"born {begin}"
    return "lifespan unknown"


def artist_story(
    artist_name: str,
    country_name: str,
    n_works: int,
    top_medium: str,
    first_decade: int | None,
    last_decade: int | None,
    work_title: str | None,
    work_year: int | None,
) -> str:
    """Build a factual collection note without inventing biography."""
    country_phrase = (
        f"the {country_name}"
        if country_name in {"United States", "United Kingdom", "Netherlands"}
        else country_name
    )
    if first_decade and last_decade and first_decade != last_decade:
        span = f"from the {first_decade}s to the {last_decade}s"
    elif first_decade:
        span = f"in the {first_decade}s"
    else:
        span = "across undated or partially dated records"
    work = ""
    if work_title:
        work = f" One representative record is {work_title}"
        if work_year:
            work += f" ({work_year})"
        work += "."
    return (
        f"In this dataset, {artist_name} is the most represented artist credited to {country_phrase}, "
        f"with {n_works:,} credited works. MoMA's records place this artist mostly in {top_medium}, "
        f"with works appearing {span}.{work}"
    )


def load_lookup_files() -> tuple[dict[str, str], dict[str, str]]:
    with (DATA_DIR / "nationality_to_iso3.json").open("r", encoding="utf-8") as handle:
        raw_nationality_to_iso = json.load(handle)
    with (DATA_DIR / "regions.json").open("r", encoding="utf-8") as handle:
        regions = json.load(handle)
    nationality_to_iso = {mapping_key(key) or key: value for key, value in raw_nationality_to_iso.items()}
    missing_regions = sorted(set(nationality_to_iso.values()) - set(regions))
    if missing_regions:
        raise ValueError(f"Missing region mappings for ISO3 codes: {missing_regions}")
    return nationality_to_iso, regions


def build_credit_rows(artworks: pd.DataFrame, nationality_to_iso: dict[str, str], regions: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in artworks.itertuples(index=False):
        artwork_id = int(getattr(row, "ObjectID"))
        ids = split_ids(getattr(row, "ConstituentID"))
        nationalities = split_parenthesized(getattr(row, "Nationality"))
        genders = split_parenthesized(getattr(row, "Gender"))
        begin_dates = split_parenthesized(getattr(row, "BeginDate"))
        end_dates = split_parenthesized(getattr(row, "EndDate"))
        names = [name.strip() for name in str(getattr(row, "Artist")).split(",")]
        credit_count = max(len(ids), len(nationalities), len(genders), 1)

        for index in range(credit_count):
            artist_id = ids[index] if index < len(ids) else None
            if artist_id is None:
                continue
            nationality = nationalities[index] if index < len(nationalities) else None
            iso3 = iso_for_nationality(nationality, nationality_to_iso)
            year = getattr(row, "year")
            rows.append(
                {
                    "artwork_id": artwork_id,
                    "artist_id": artist_id,
                    "artist_name": names[index] if index < len(names) else str(getattr(row, "Artist")),
                    "title": clean_token(getattr(row, "Title")),
                    "year": int(year) if pd.notna(year) else None,
                    "decade": int(getattr(row, "decade")) if pd.notna(getattr(row, "decade")) else None,
                    "date_label": clean_token(getattr(row, "Date")),
                    "department": clean_token(getattr(row, "Department")) or "Unknown",
                    "classification": clean_token(getattr(row, "Classification")) or "Unknown",
                    "medium": clean_token(getattr(row, "Medium")) or "Unknown",
                    "medium_group": getattr(row, "medium_group"),
                    "nationality": nationality,
                    "iso3": iso3,
                    "country_name": ISO3_TO_COUNTRY.get(iso3, iso3) if iso3 else None,
                    "region": get_region(iso3, regions),
                    "gender": normalize_gender(genders[index] if index < len(genders) else None),
                    "year_birth": parse_year(begin_dates[index] if index < len(begin_dates) else None),
                    "year_death": parse_year(end_dates[index] if index < len(end_dates) else None),
                    "url": clean_token(getattr(row, "URL")),
                }
            )
    return rows


def add_count_alias(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for record in records:
        if "n" in record:
            record["count"] = record["n"]
    return records


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale_json in OUTPUT_DIR.glob("*.json"):
        stale_json.unlink()
    nationality_to_iso, regions = load_lookup_files()

    artworks_raw = pd.read_csv(RAW_DIR / "Artworks.csv", low_memory=False)
    artists_raw = pd.read_csv(RAW_DIR / "Artists.csv", low_memory=False)

    artworks = artworks_raw.dropna(subset=ARTWORK_KEY_COLUMNS).copy()
    artists = artists_raw.drop(columns=["Wiki QID", "ULAN"]).dropna(subset=ARTIST_KEY_COLUMNS).copy()

    if len(artworks) != EXPECTED_ARTWORKS:
        raise AssertionError(f"Expected {EXPECTED_ARTWORKS} cleaned artworks, got {len(artworks)}")
    if len(artists) != EXPECTED_ARTISTS:
        raise AssertionError(f"Expected {EXPECTED_ARTISTS} cleaned artists, got {len(artists)}")

    artworks["year"] = artworks["Date"].map(parse_year)
    artworks["decade"] = artworks["year"].map(decade_from_year)
    artworks["medium_group"] = artworks.apply(
        lambda row: canonical_medium(row["Classification"], row["Medium"], row["Department"]),
        axis=1,
    )

    credit_rows = build_credit_rows(artworks, nationality_to_iso, regions)
    credits = pd.DataFrame(credit_rows)
    n_total = len(artworks)
    n_credits = len(credits)

    summary = {
        "n_artworks_total": n_total,
        "n_artworks_dated": int(artworks["year"].notna().sum()),
        "n_artist_credits": n_credits,
        "n_artists_total": len(artists),
        "year_min": int(artworks["year"].min()),
        "year_max": int(artworks["year"].max()),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_artworks": n_total,
        "total_artists": len(artists),
        "unique_nationalities": int(artists["Nationality"].nunique()),
        "top_department": str(artworks["Department"].value_counts().index[0]),
    }
    write_json("summary.json", summary)

    medium_counts = artworks["Department"].value_counts().reset_index()
    medium_counts.columns = ["medium", "n"]
    top_mediums = medium_counts.head(12).copy()
    other_n = int(medium_counts["n"].iloc[12:].sum())
    if other_n:
        top_mediums = pd.concat(
            [top_mediums, pd.DataFrame([{"medium": "Other", "n": other_n}])],
            ignore_index=True,
        )
    top_mediums["pct"] = (top_mediums["n"] / n_total * 100).round(4)
    medium_total_records = records_from_df(top_mediums)
    write_json("medium_totals.json", medium_total_records)

    timeline = artworks.groupby("decade", dropna=False).size().reset_index(name="n")
    timeline_records = add_count_alias(records_from_df(timeline.sort_values("decade")))
    write_json("timeline.json", timeline_records)

    gender_by_decade = credits.groupby(["decade", "gender"], dropna=False).size().reset_index(name="n")
    write_json("gender_by_decade.json", add_count_alias(records_from_df(gender_by_decade)))

    gender_by_dept = credits.groupby(["decade", "department", "gender"], dropna=False).size().reset_index(name="n")
    write_json("gender_by_decade_department.json", records_from_df(gender_by_dept))

    gender_by_country = credits.groupby(["decade", "iso3", "gender"], dropna=False).size().reset_index(name="n")
    write_json("gender_by_decade_country.json", records_from_df(gender_by_country))

    country_credits = credits.dropna(subset=["iso3"]).copy()
    country_by_decade = (
        country_credits.groupby(["decade", "iso3", "country_name"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["decade", "n"], ascending=[True, False])
    )
    write_json("country_by_decade.json", records_from_df(country_by_decade))

    country_summary_records: list[dict[str, Any]] = []
    for iso3, group in country_credits.groupby("iso3"):
        medium_counter = Counter(group["medium_group"])
        sorted_group = group.sort_values(["artist_name", "title", "year"], na_position="last")
        sample = sorted_group.iloc[seeded_index(str(iso3), len(sorted_group))]
        featured_artist_id = int(group["artist_id"].value_counts().sort_values(ascending=False).index[0])
        featured_group = group[group["artist_id"] == featured_artist_id].sort_values(["year", "title"], na_position="last")
        featured_sample = featured_group.iloc[0]
        featured_medium = Counter(featured_group["medium_group"]).most_common(1)[0][0]
        featured_decades = [int(decade) for decade in featured_group["decade"].dropna().unique()]
        featured_first = min(featured_decades) if featured_decades else None
        featured_last = max(featured_decades) if featured_decades else None
        featured_work_year = json_ready(featured_sample["year"])
        country_name = ISO3_TO_COUNTRY.get(iso3, iso3)
        country_summary_records.append(
            {
                "iso3": iso3,
                "country_name": country_name,
                "region": regions.get(iso3, "Unknown"),
                "n": int(len(group)),
                "n_artists": int(group["artist_id"].nunique()),
                "top_medium": medium_counter.most_common(1)[0][0],
                "sample_artist": sample["artist_name"],
                "sample_lifespan": lifespan(sample["year_birth"], sample["year_death"]),
                "sample_work_title": sample["title"],
                "sample_work_year": json_ready(sample["year"]),
                "sample_work_medium": sample["medium"],
                "featured_artist_id": featured_artist_id,
                "featured_artist": featured_sample["artist_name"],
                "featured_artist_n_works": int(len(featured_group)),
                "featured_artist_lifespan": lifespan(
                    featured_sample["year_birth"],
                    featured_sample["year_death"],
                ),
                "featured_artist_gender": featured_sample["gender"],
                "featured_artist_medium": featured_medium,
                "featured_decade_first": featured_first,
                "featured_decade_last": featured_last,
                "featured_work_title": featured_sample["title"],
                "featured_work_year": featured_work_year,
                "featured_story": artist_story(
                    featured_sample["artist_name"],
                    country_name,
                    int(len(featured_group)),
                    featured_medium,
                    featured_first,
                    featured_last,
                    featured_sample["title"],
                    featured_work_year,
                ),
            }
        )
    country_summary_records.sort(key=lambda item: item["n"], reverse=True)
    write_json("country_summary.json", country_summary_records)

    top_medium_groups = credits["medium_group"].value_counts().head(9).index.tolist()
    medium_breakdown = (
        credits[credits["medium_group"].isin(top_medium_groups)]
        .groupby(["medium_group", "decade", "gender", "region", "department", "iso3"], dropna=False)
        .size()
        .reset_index(name="n")
        .rename(columns={"medium_group": "medium"})
    )
    write_json("medium_breakdown.json", records_from_df(medium_breakdown))

    artist_counts = credits.groupby("artist_id").size().to_dict()
    artist_medium_primary = (
        credits.groupby(["artist_id", "medium_group"]).size().reset_index(name="n")
        .sort_values(["artist_id", "n", "medium_group"], ascending=[True, False, True])
        .drop_duplicates("artist_id")
        .set_index("artist_id")["medium_group"]
        .to_dict()
    )
    dated_credits = credits.dropna(subset=["decade"])
    artist_decades = dated_credits.groupby("artist_id")["decade"].agg(["min", "max"]).to_dict(orient="index")
    artist_samples = (
        credits.sort_values(["artist_id", "year", "title"], na_position="last")
        .drop_duplicates("artist_id")
        .set_index("artist_id")
        .to_dict(orient="index")
    )

    artist_records: list[dict[str, Any]] = []
    for artist in artists.itertuples(index=False):
        artist_id = int(getattr(artist, "ConstituentID"))
        birth = int(getattr(artist, "BeginDate")) if int(getattr(artist, "BeginDate")) > 0 else None
        death = int(getattr(artist, "EndDate")) if int(getattr(artist, "EndDate")) > 0 else None
        birth_decade = decade_from_year(birth)
        nationality = clean_token(getattr(artist, "Nationality"))
        iso3 = iso_for_nationality(nationality, nationality_to_iso)
        decades = artist_decades.get(artist_id, {})
        first_decade = json_ready(decades.get("min")) if decades else birth_decade
        last_decade = json_ready(decades.get("max")) if decades else birth_decade
        sample = artist_samples.get(artist_id, {})
        if int(artist_counts.get(artist_id, 0)) <= 0:
            continue
        record = {
            "artist_id": artist_id,
            "name": clean_token(getattr(artist, "DisplayName")),
            "nationality": nationality,
            "iso3": iso3,
            "region": get_region(iso3, regions),
            "gender": normalize_gender(getattr(artist, "Gender")),
            "year_birth": birth,
            "year_death": death,
            "decade_active_first": first_decade,
            "decade_active_last": last_decade,
            "medium_primary": artist_medium_primary.get(artist_id, "Other"),
            "n_works": int(artist_counts.get(artist_id, 0)),
            "sample_work_title": sample.get("title"),
            "sample_work_year": json_ready(sample.get("year")),
        }
        artist_records.append(
            {
                key: value
                for key, value in record.items()
                if value is not None
                and value != ""
                and not (key == "decade_active_last" and value == record.get("decade_active_first"))
                and not (key == "region" and value == "Unknown")
            }
        )
    artist_records.sort(key=lambda record: (record["name"] or ""))
    write_json("artist_index.json", artist_records)

    top_unmapped = (
        credits[credits["iso3"].isna()]["nationality"]
        .fillna("Unknown")
        .value_counts()
        .head(12)
        .to_dict()
    )
    medium_sum = sum(int(record["n"]) for record in medium_total_records)
    report_lines = [
        "DArts aggregate build report",
        f"generated_at: {summary['generated_at']}",
        "",
        f"raw_artworks: {len(artworks_raw):,}",
        f"cleaned_artworks: {n_total:,}",
        f"expected_cleaned_artworks: {EXPECTED_ARTWORKS:,}",
        f"artworks_excluded_by_m1_key_fields: {len(artworks_raw) - n_total:,}",
        f"dated_artworks_after_permissive_parse: {summary['n_artworks_dated']:,}",
        f"undated_after_parse_within_cleaned_corpus: {n_total - summary['n_artworks_dated']:,}",
        f"raw_artists: {len(artists_raw):,}",
        f"cleaned_artists: {len(artists):,}",
        f"expected_cleaned_artists: {EXPECTED_ARTISTS:,}",
        f"artist_credits: {n_credits:,}",
        "",
        f"medium_totals_sum: {medium_sum:,}",
        f"medium_totals_reconciles: {medium_sum == n_total}",
        f"country_mapped_artist_credits: {len(country_credits):,}",
        f"country_unmapped_artist_credits: {n_credits - len(country_credits):,}",
        f"country_unmapped_share_of_credits: {(n_credits - len(country_credits)) / n_credits * 100:.2f}%",
        "",
        "top_countries_by_credit:",
    ]
    for row in country_summary_records[:8]:
        report_lines.append(f"  {row['country_name']}: {row['n']:,}")
    report_lines.extend(["", "top_unmapped_nationality_labels:"])
    for nationality, count in top_unmapped.items():
        report_lines.append(f"  {nationality}: {count:,}")
    report_lines.extend(["", "outputs:"])
    for path in sorted(OUTPUT_DIR.glob("*.json")):
        report_lines.append(f"  {path.name}: {path.stat().st_size:,} bytes")

    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print("\n".join(report_lines))


if __name__ == "__main__":
    main()
