"""
jd_parser: cleans raw JD text and isolates requirements/responsibilities.

Strategy: try a cheap heuristic (section-header matching) first. Only
fall back to an LLM call if the heuristic finds nothing usable.
"""

import logging
import re

from src.graph.state import JDState
from src.prompts.jd_parser_prompt import REQUIREMENTS_EXTRACTION_PROMPT
from src.tools.llm_client import call_llm_for_lines

logger = logging.getLogger(__name__)

# Boilerplate lines that show up on job posting pages but aren't JD content
_NOISE_PATTERNS = [
    r"^apply now$",
    r"^share this job$",
    r"^similar jobs$",
    r"^back to (search|jobs|listings)$",
    r"^sign in$",
    r"^equal opportunity employer.*",
    r"^©.*",
]

# Headers that signal the start of a requirements/qualifications section
_REQUIREMENTS_HEADERS = [
    r"requirements",
    r"qualifications",
    r"what you.?ll need",
    r"what we.?re looking for",
    r"minimum qualifications",
    r"preferred qualifications",
    r"skills? (and|&) experience",
    r"who you are",
]

# Headers that signal ANY new section (used to know when to stop collecting)
_ANY_SECTION_HEADER = [
    r"about (us|the role|the team|the company)",
    r"responsibilities",
    r"what you.?ll do",
    r"benefits",
    r"perks",
    r"compensation",
    r"how to apply",
    r"equal opportunity",
] + _REQUIREMENTS_HEADERS

_MAX_HEADER_LINE_LENGTH = 60  # headers are short; long lines can't be headers


def jd_parser(state: JDState) -> dict:
    raw_jd = state["raw_jd"]
    logger.info("jd_parser: starting, raw_jd length=%d chars", len(raw_jd))

    cleaned_jd = _clean_text(raw_jd)
    logger.info("jd_parser: cleaned_jd length=%d chars (%d lines)",
                len(cleaned_jd), len(cleaned_jd.splitlines()))

    requirements_raw = _extract_requirements_heuristic(cleaned_jd)

    if requirements_raw:
        logger.info("jd_parser: heuristic found %d requirement lines",
                    len(requirements_raw))
    else:
        logger.warning("jd_parser: heuristic found nothing — falling back to LLM")
        prompt = REQUIREMENTS_EXTRACTION_PROMPT.format(cleaned_jd=cleaned_jd)
        requirements_raw = call_llm_for_lines(prompt)
        logger.info("jd_parser: LLM fallback extracted %d requirement lines",
                    len(requirements_raw))

    return {
        "cleaned_jd": cleaned_jd,
        "requirements_raw": requirements_raw,
    }


def _clean_text(text: str) -> str:
    lines = text.strip().splitlines()
    kept = []
    removed_count = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(re.match(p, stripped, re.IGNORECASE) for p in _NOISE_PATTERNS):
            removed_count += 1
            continue
        kept.append(stripped)

    if removed_count:
        logger.debug("jd_parser: removed %d boilerplate lines", removed_count)

    return "\n".join(kept)


def _is_header(line: str, patterns: list[str]) -> bool:
    if len(line) > _MAX_HEADER_LINE_LENGTH:
        return False
    line_norm = line.strip().rstrip(":").lower()
    return any(re.search(p, line_norm) for p in patterns)


def _extract_requirements_heuristic(cleaned_jd: str) -> list[str]:
    lines = cleaned_jd.splitlines()
    collected: list[str] = []
    collecting = False

    for line in lines:
        if _is_header(line, _REQUIREMENTS_HEADERS):
            logger.debug("jd_parser: heuristic matched requirements header: %r", line)
            collecting = True
            continue  # don't include the header itself
        if collecting and _is_header(line, _ANY_SECTION_HEADER):
            logger.debug("jd_parser: heuristic hit next section header, stopping: %r", line)
            break
        if collecting:
            collected.append(line)

    return collected