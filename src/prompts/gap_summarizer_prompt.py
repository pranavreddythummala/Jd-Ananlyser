GAP_SUMMARIZER_PROMPT = """
You are given must-have and nice-to-have skills extracted from a job posting.
Write a short, clear summary titled "What you need to land an interview"
that:
- Lists the must-have skills plainly, grouped logically if it helps
- Notes the nice-to-have skills as a secondary, shorter list
- Is direct and practical, no fluff

Must-have skills:
{must_have}

Nice-to-have skills:
{nice_to_have}
"""
