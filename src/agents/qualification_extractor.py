"""
qualification_extractor: pulls discrete technical items out of the
requirements section (languages, tools, years of experience, certs).
"""

import logging

from src.graph.state import JDState
from src.prompts.qualification_extractor_prompt import QUALIFICATION_EXTRACTOR_PROMPT
from src.tools.llm_client import call_llm_for_lines

logger = logging.getLogger(__name__)


def qualification_extractor(state: JDState) -> dict:
    requirements_raw = state["requirements_raw"]

    if not requirements_raw:
        logger.warning("qualification_extractor: requirements_raw is empty, skipping LLM call")
        return {"extracted_skills": []}

    requirements_text = "\n".join(requirements_raw)
    prompt = QUALIFICATION_EXTRACTOR_PROMPT.format(requirements_raw=requirements_text)

    extracted_skills = call_llm_for_lines(prompt)
    logger.info("qualification_extractor: extracted %d discrete skills", len(extracted_skills))

    return {"extracted_skills": extracted_skills}