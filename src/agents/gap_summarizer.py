"""
gap_summarizer: turns the ranked skill lists into a clear, actionable
"what you need to land an interview" writeup.
"""

import logging

from src.graph.state import JDState
from src.prompts.gap_summarizer_prompt import GAP_SUMMARIZER_PROMPT
from src.tools.llm_client import call_llm

logger = logging.getLogger(__name__)


def gap_summarizer(state: JDState) -> dict:
    must_have = state["must_have"]
    nice_to_have = state["nice_to_have"]

    if not must_have and not nice_to_have:
        logger.warning("gap_summarizer: no skills to summarize, returning empty summary")
        return {"summary": "No skills could be extracted from this job description."}

    prompt = GAP_SUMMARIZER_PROMPT.format(
        must_have="\n".join(must_have) or "(none identified)",
        nice_to_have="\n".join(nice_to_have) or "(none identified)",
    )

    logger.info("gap_summarizer: generating summary from %d must-have, %d nice-to-have skills",
                len(must_have), len(nice_to_have))

    summary = call_llm(prompt, max_tokens=1024)

    logger.info("gap_summarizer: generated summary (%d chars)", len(summary))

    return {"summary": summary}