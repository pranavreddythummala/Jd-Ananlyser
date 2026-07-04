# JD Skill Gap Analyzer

A LangGraph pipeline that takes a job description (URL or pasted text) and
outputs the core technical skills you need to land an interview.

## Graph

```
START -> jd_fetcher -> jd_parser -> qualification_extractor -> skill_ranker -> gap_summarizer -> END
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your API key
python main.py
```

## Structure

- `src/graph/state.py` — shared state schema (JDState)
- `src/graph/builder.py` — wires nodes + edges into the compiled graph
- `src/agents/` — one file per node, each with a single responsibility
- `src/prompts/` — prompt templates used by the LLM-driven nodes
- `src/tools/` — reserved for future MCP / external tool integrations
- `tests/` — unit tests per node

## Status

All nodes are scaffolded with `TODO`s. Fill in `jd_fetcher` first
(URL fetching + HTML stripping), test it standalone, then move down
the pipeline one node at a time.
