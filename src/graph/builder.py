from langgraph.graph import StateGraph, START, END

from src.graph.state import JDState
from src.agents.jd_fetcher import jd_fetcher
from src.agents.jd_parser import jd_parser
from src.agents.qualification_extractor import qualification_extractor
from src.agents.skill_ranker import skill_ranker
from src.agents.gap_summarizer import gap_summarizer
from langgraph.checkpoint.memory import MemorySaver


def build_graph():
    builder = StateGraph(JDState)

    builder.add_node("jd_fetcher", jd_fetcher)
    builder.add_node("jd_parser", jd_parser)
    builder.add_node("qualification_extractor", qualification_extractor)
    builder.add_node("skill_ranker", skill_ranker)
    builder.add_node("gap_summarizer", gap_summarizer)

    builder.add_edge(START, "jd_fetcher")
    builder.add_edge("jd_fetcher", "jd_parser")
    builder.add_edge("jd_parser", "qualification_extractor")
    builder.add_edge("qualification_extractor", "skill_ranker")
    builder.add_edge("skill_ranker", "gap_summarizer")
    builder.add_edge("gap_summarizer", END)

    return builder.compile(checkpointer=MemorySaver())
