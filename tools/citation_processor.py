"""Convert APA-style manuscript citations to numeric bracketed citations.

The processor treats the manuscript reference section as the authoritative source
for bibliography entries. It sorts those entries alphabetically, assigns stable
numeric identifiers, and rewrites matching author-year citations in the body to
SEINFORMS-compatible bracketed citations.

Copyright © 2026 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

YEAR_PATTERN = r"(?:19|20)\d{2}[a-z]?"
REFERENCE_HEADING_PATTERN = re.compile(r"(?m)^##\s+\d*\.?\s*References\s*$")
NEXT_HEADING_PATTERN = re.compile(r"(?m)^##\s+")
APA_YEAR_PATTERN = re.compile(rf"\(({YEAR_PATTERN})(?:,\s*[^)]*)?\)")
PARENTHETICAL_CITATION_PATTERN = re.compile(r"\(([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*)\)")
CITATION_SEGMENT_PATTERN = re.compile(
    rf"^(?P<authors>.+?),\s*(?P<year>{YEAR_PATTERN})(?P<locator>,\s*.+)?$"
)
AUTHOR_NAME_PATTERN = r"[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'\-]+"
NARRATIVE_CITATION_PATTERN = re.compile(
    rf"(?P<authors>"
    rf"{AUTHOR_NAME_PATTERN}"
    rf"(?:,\s*{AUTHOR_NAME_PATTERN})*"
    rf"(?:,?\s*(?:&|and)\s*{AUTHOR_NAME_PATTERN}|\s+et\s+al\.)?"
    rf")\s*\((?P<year>{YEAR_PATTERN})\)"
)
SUBHEADING_PATTERN = re.compile(r"^#{1,6}\s+")

ALIAS_BY_CANONICAL_AUTHOR = {
    "Council on Environmental Quality": {"CEQ"},
    "International Energy Agency": {"IEA", "IEA Global EV Outlook"},
    "North Carolina Department of Transportation": {"NCDOT"},
    "Joint Office of Energy and Transportation": {"Joint Office"},
    "U.S. Census Bureau": {"LEHD LODES"},
    "U.S. Department of Energy": {"DOE"},
}


@dataclass(frozen=True)
class ReferenceEntry:
    """Parsed reference entry with derived citation keys."""

    sort_key: str
    text: str
    year: str
    citation_names: frozenset[str]


def process_citations(text: str) -> tuple[str, list[str]]:
    """Convert author-year citations in text to numeric bracketed citations.

    Args:
        text: Markdown manuscript text containing APA-style inline citations and
            a References section.

    Returns:
        Tuple containing the citation-converted manuscript text and a sorted list
        of numbered reference strings.
    """
    body, references_section, suffix = _split_reference_section(text)
    references = _parse_references(references_section)
    references_by_number = _number_references(references)
    citation_map = _build_citation_map(references_by_number)

    updated_body = _replace_parenthetical_citations(body, citation_map)
    updated_body = _replace_narrative_citations(updated_body, citation_map)
    formatted_references = [
        f"[{number}] {entry.text}" for number, entry in references_by_number
    ]

    if references_section:
        updated_text = _join_with_numbered_references(
            updated_body,
            formatted_references,
            suffix,
        )
    else:
        updated_text = updated_body

    return updated_text, formatted_references


def _split_reference_section(text: str) -> tuple[str, str, str]:
    reference_match = REFERENCE_HEADING_PATTERN.search(text)
    if reference_match is None:
        return text, "", ""

    body = text[: reference_match.start()].rstrip()
    references_start = reference_match.start()
    after_heading_start = reference_match.end()
    next_heading_match = NEXT_HEADING_PATTERN.search(text, after_heading_start)

    if next_heading_match is None:
        return body, text[references_start:].strip(), ""

    references_section = text[references_start : next_heading_match.start()].strip()
    suffix = text[next_heading_match.start() :].lstrip()
    return body, references_section, suffix


def _parse_references(references_section: str) -> list[ReferenceEntry]:
    entries: list[ReferenceEntry] = []
    blocks = re.split(r"\n\s*\n", references_section)

    for block in blocks:
        entry_text = " ".join(line.strip() for line in block.splitlines()).strip()
        if not entry_text or SUBHEADING_PATTERN.match(entry_text):
            continue

        year_match = APA_YEAR_PATTERN.search(entry_text)
        if year_match is None:
            continue

        author_text = entry_text[: year_match.start()].strip().rstrip(".")
        if not author_text:
            continue

        year = year_match.group(1)
        citation_names = _citation_names_for_author_text(author_text)
        entries.append(
            ReferenceEntry(
                sort_key=_normalize_sort_key(entry_text),
                text=entry_text,
                year=year,
                citation_names=frozenset(citation_names),
            )
        )

    return sorted(entries, key=lambda entry: entry.sort_key)


def _number_references(
    references: list[ReferenceEntry],
) -> list[tuple[int, ReferenceEntry]]:
    return list(enumerate(references, start=1))


def _build_citation_map(
    references_by_number: list[tuple[int, ReferenceEntry]],
) -> dict[tuple[str, str], int]:
    citation_map: dict[tuple[str, str], int] = {}

    for number, entry in references_by_number:
        for citation_name in entry.citation_names:
            citation_map[_normalize_citation_name(citation_name), entry.year] = number

    return citation_map


def _citation_number_for(
    authors: str,
    year: str,
    citation_map: dict[tuple[str, str], int],
) -> int | None:
    normalized_authors = _normalize_citation_name(authors)
    direct_match = citation_map.get((normalized_authors, year))
    if direct_match is not None:
        return direct_match

    return None


def _replace_parenthetical_citations(
    text: str,
    citation_map: dict[tuple[str, str], int],
) -> str:
    def replace_match(match: re.Match[str]) -> str:
        content = match.group(1)
        segments = [segment.strip() for segment in content.split(";")]
        converted_segments = [
            _convert_citation_segment(segment, citation_map) for segment in segments
        ]

        if all(segment is not None for segment in converted_segments):
            converted = [
                segment for segment in converted_segments if segment is not None
            ]
            if all(
                segment.startswith("[") and segment.endswith("]")
                for segment in converted
            ):
                return _merge_bracket_citations(converted)
            return f"({'; '.join(converted)})"

        rebuilt_segments = [
            converted if converted is not None else original
            for original, converted in zip(segments, converted_segments, strict=True)
        ]
        return f"({'; '.join(rebuilt_segments)})"

    return PARENTHETICAL_CITATION_PATTERN.sub(replace_match, text)


def _replace_narrative_citations(
    text: str,
    citation_map: dict[tuple[str, str], int],
) -> str:
    def replace_match(match: re.Match[str]) -> str:
        authors = match.group("authors").strip()
        year = match.group("year")
        number = _citation_number_for(authors, year, citation_map)
        if number is None:
            return match.group(0)
        return f"{authors} [{number}]"

    return NARRATIVE_CITATION_PATTERN.sub(replace_match, text)


def _convert_citation_segment(
    segment: str,
    citation_map: dict[tuple[str, str], int],
) -> str | None:
    citation_match = CITATION_SEGMENT_PATTERN.match(segment)
    if citation_match is None:
        return None

    authors = citation_match.group("authors").strip()
    year = citation_match.group("year")
    locator = citation_match.group("locator") or ""
    number = _citation_number_for(authors, year, citation_map)
    if number is not None:
        if locator:
            return f"[{number}{locator}]"
        return f"[{number}]"

    for marker in (" as in ", " based on "):
        prefix, separator, citation_tail = authors.rpartition(marker)
        if not separator:
            continue
        number = _citation_number_for(citation_tail, year, citation_map)
        if number is not None:
            return f"{prefix}{separator}[{number}{locator}]"

    return None


def _merge_bracket_citations(citations: list[str]) -> str:
    if len(citations) == 1:
        return citations[0]

    merged_parts = [citation.strip("[]") for citation in citations]
    return f"[{', '.join(merged_parts)}]"


def _citation_names_for_author_text(author_text: str) -> set[str]:
    corporate_author = _corporate_author(author_text)
    if corporate_author is not None:
        names = {corporate_author}
        names.update(ALIAS_BY_CANONICAL_AUTHOR.get(corporate_author, set()))
        return names

    surnames = _personal_author_surnames(author_text)
    if not surnames:
        return {author_text}

    if len(surnames) == 1:
        return {surnames[0]}

    names = {f"{surnames[0]} et al."}
    if len(surnames) == 2:
        names.add(f"{surnames[0]} & {surnames[1]}")
        names.add(f"{surnames[0]} and {surnames[1]}")
    else:
        serial_names = ", ".join(surnames[:-1])
        names.add(f"{serial_names}, & {surnames[-1]}")
        names.add(f"{serial_names}, and {surnames[-1]}")
    return names


def _corporate_author(author_text: str) -> str | None:
    if "," not in author_text and "&" not in author_text:
        return author_text

    for corporate_author in ALIAS_BY_CANONICAL_AUTHOR:
        if author_text.startswith(corporate_author):
            return corporate_author

    return None


def _personal_author_surnames(author_text: str) -> list[str]:
    normalized = author_text.replace(", &", ",").replace(" &", ",")
    parts = [part.strip() for part in normalized.split(",") if part.strip()]
    surnames: list[str] = []

    index = 0
    while index < len(parts):
        part = parts[index]
        if _looks_like_initials(part):
            index += 1
            continue
        surnames.append(part)
        index += 1

    return surnames


def _looks_like_initials(text: str) -> bool:
    return bool(re.fullmatch(r"(?:[A-Z]\.?\s*)+(?:III|IV|Jr\.)?", text))


def _normalize_citation_name(name: str) -> str:
    normalized = name.replace("&", "and")
    normalized = re.sub(r"\bet\s+al\b", "et al", normalized, flags=re.IGNORECASE)
    normalized = normalized.replace("\u2019", "'")
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"\s*,\s*", ", ", normalized)
    return normalized.strip().rstrip(".").casefold()


def _normalize_sort_key(text: str) -> str:
    return re.sub(r"\s+", " ", text).casefold()


def _join_with_numbered_references(
    body: str,
    formatted_references: list[str],
    suffix: str,
) -> str:
    references_text = "\n\n".join(formatted_references)
    updated_text = f"{body}\n\n---\n\n## 12. References\n\n{references_text}"
    if suffix:
        updated_text = f"{updated_text}\n\n---\n\n{suffix.rstrip()}"
    return f"{updated_text}\n"


def main() -> None:
    """Run the citation processor against a manuscript file."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path, help="Markdown manuscript to process")
    parser.add_argument(
        "--preview-lines",
        type=int,
        default=80,
        help="Number of converted text lines to print before the bibliography",
    )
    args = parser.parse_args()

    updated_text, references = process_citations(args.manuscript.read_text())
    preview = "\n".join(updated_text.splitlines()[: args.preview_lines])

    print("=== Converted text preview ===")
    print(preview)
    print("\n=== Numbered references ===")
    for reference in references:
        print(reference)


if __name__ == "__main__":
    main()
