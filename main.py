import sys
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

from src.graph.builder import build_graph


def _is_url(text: str) -> bool:
    parsed = urlparse(text.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def build_initial_state(user_input: str) -> dict:
    user_input = user_input.strip()
    if _is_url(user_input):
        return {"source_url": user_input}
    else:
        return {"raw_input": user_input}


def _read_multiline_input() -> str:
    print("Paste a job posting URL or the full JD text.")
    print("When done pasting, press Ctrl+D (Mac/Linux) then Enter:\n")
    return sys.stdin.read()


def main():
    graph = build_graph()

    user_input = _read_multiline_input()
    initial_state = build_initial_state(user_input)

    logging.info("main: detected input type = %s, length = %d chars",
                 "source_url" if "source_url" in initial_state else "raw_input",
                 len(user_input))

    result = graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": "test-1"}},
    )
    print("\n--- SUMMARY ---\n")
    print(result["summary"])


if __name__ == "__main__":
    main()