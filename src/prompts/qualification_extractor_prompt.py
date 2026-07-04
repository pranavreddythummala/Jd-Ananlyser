QUALIFICATION_EXTRACTOR_PROMPT = """
You are given the requirements/responsibilities section of a job description.
Extract a flat list of discrete technical qualifications: languages, tools,
frameworks, years of experience, certifications, degrees.

Return one item per line, no commentary.

Requirements text:
{requirements_raw}
"""
