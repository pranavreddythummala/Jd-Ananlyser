SKILL_RANKER_PROMPT = """
You are given a list of extracted skills and the full cleaned job description.
Classify each skill as "must_have" or "nice_to_have" based on:
- explicit language ("required" vs "preferred"/"bonus"/"a plus")
- how central the skill is to the core responsibilities

Return two lists in JSON: {{"must_have": [...], "nice_to_have": [...]}}

Extracted skills:
{extracted_skills}

Full job description:
{cleaned_jd}
"""
