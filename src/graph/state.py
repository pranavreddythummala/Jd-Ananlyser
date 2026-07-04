from typing import TypedDict, List, Optional


class JDState(TypedDict, total=False):
    # --- inputs ---
    source_url: Optional[str]      # URL to a job posting, if provided
    raw_input: Optional[str]       # pasted JD text, if provided instead of a URL

    # --- jd_fetcher output ---
    raw_jd: str                    # plain text of the job description, from either source

    # --- jd_parser output ---
    cleaned_jd: str                # noise-stripped JD text
    requirements_raw: List[str]    # isolated requirements/responsibilities lines

    # --- qualification_extractor output ---
    extracted_skills: List[str]    # discrete technical items pulled from requirements

    # --- skill_ranker output ---
    must_have: List[str]           # required skills
    nice_to_have: List[str]        # preferred/bonus skills

    # --- gap_summarizer output ---
    summary: str                   # final "what you need to land an interview" writeup
