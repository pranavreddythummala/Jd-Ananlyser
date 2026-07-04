"""
skill_ranker: classifies each extracted skill as must-have vs nice-to-have,
based on language cues in the JD ("required" vs "preferred"/"bonus") and
centrality to the core responsibilities.
"""

import logging

from src.graph.state import JDState
from src.prompts.skill_ranker_prompt import SKILL_RANKER_PROMPT
from src.tools.llm_client import call_llm_for_json

logger = logging.getLogger(__name__)


def skill_ranker(state: JDState) -> dict:
    extracted_skills = state["extracted_skills"]
    cleaned_jd = state["cleaned_jd"]

    if not extracted_skills:
        logger.warning("skill_ranker: extracted_skills is empty, skipping LLM call")
        return {"must_have": [], "nice_to_have": []}

    skills_text = "\n".join(extracted_skills)
    prompt = SKILL_RANKER_PROMPT.format(
        extracted_skills=skills_text,
        cleaned_jd=cleaned_jd,
    )

    logger.info("skill_ranker: ranking %d extracted skills", len(extracted_skills))

    try:
        result = call_llm_for_json(prompt)
    except Exception:
        logger.error("skill_ranker: LLM call/parse failed, falling back to all-nice-to-have")
        return {"must_have": [], "nice_to_have": extracted_skills}

    must_have = result.get("must_have", [])
    nice_to_have = result.get("nice_to_have", [])

    logger.info("skill_ranker: %d must-have, %d nice-to-have",
                len(must_have), len(nice_to_have))

    return {
        "must_have": must_have,
        "nice_to_have": nice_to_have,
    }