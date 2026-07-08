"""Small text helpers for rule-based caption analysis."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable


EMOJI_PATTERN = re.compile(
    "["
    "\U0001f300-\U0001f5ff"
    "\U0001f600-\U0001f64f"
    "\U0001f680-\U0001f6ff"
    "\U0001f700-\U0001f77f"
    "\U0001f780-\U0001f7ff"
    "\U0001f800-\U0001f8ff"
    "\U0001f900-\U0001f9ff"
    "\U0001fa00-\U0001fa6f"
    "\U0001fa70-\U0001faff"
    "\u2600-\u26ff"
    "\u2700-\u27bf"
    "]+",
    flags=re.UNICODE,
)


def normalize_text(value: str | None) -> str:
    """Lowercase and normalize spacing while preserving phrase boundaries."""
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKC", value)
    normalized = normalized.replace("’", "'").replace("“", '"').replace("”", '"')
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip().lower()


def contains_phrase(text: str, phrase: str) -> bool:
    """Match a word or phrase with basic word boundaries."""
    clean_phrase = normalize_text(phrase)
    if not clean_phrase:
        return False

    escaped = re.escape(clean_phrase).replace(r"\ ", r"\s+")
    return re.search(rf"(?<!\w){escaped}(?!\w)", text) is not None


def find_matches(text: str, phrases: Iterable[str]) -> list[str]:
    """Return matching phrases in input order with duplicates removed."""
    return unique_preserve_order([phrase for phrase in phrases if contains_phrase(text, phrase)])


def count_emojis(text: str) -> int:
    """Count emoji code-point groups in a caption."""
    if not text:
        return 0
    return len(EMOJI_PATTERN.findall(text))


def has_excessive_punctuation(text: str) -> bool:
    """Flag repeated punctuation that usually makes branded copy feel pushy."""
    return bool(re.search(r"([!?])\1{2,}", text or ""))


def word_count(text: str) -> int:
    """Count words and hashtag terms."""
    return len(re.findall(r"[A-Za-z0-9#'-]+", text or ""))


def clamp(value: int | float, minimum: int = 0, maximum: int = 100) -> int:
    """Clamp a numeric score and return an int."""
    return int(max(minimum, min(maximum, round(value))))


def unique_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = normalize_text(value)
        if key and key not in seen:
            seen.add(key)
            result.append(value)
    return result


def parse_list_text(value: str | Iterable[str] | None) -> list[str]:
    """Accept lists or comma/newline separated values for custom profiles."""
    if value is None:
        return []
    if isinstance(value, str):
        parts = re.split(r"[,;\n]+", value)
        return [part.strip() for part in parts if part.strip()]
    return [str(item).strip() for item in value if str(item).strip()]

