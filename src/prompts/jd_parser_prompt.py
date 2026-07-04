REQUIREMENTS_EXTRACTION_PROMPT = """
You are given the full text of a job posting. Extract only the lines that
describe required or preferred qualifications, skills, tools, experience
level, or certifications — the kind of content that would appear under a
"Requirements" or "Qualifications" heading, even if this job posting
doesn't use clear section headers.

Ignore company descriptions, responsibilities/duties, benefits, and
application instructions.

Return one qualification per line, plain text, no bullets or numbering.

Job posting text:
{cleaned_jd}
"""