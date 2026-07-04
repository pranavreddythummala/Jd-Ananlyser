import logging
logging.basicConfig(level=logging.INFO)

from src.graph.builder import build_graph


def main():
    graph = build_graph()

    initial_state = {
        "raw_input": """
        Senior Backend Engineer

        Requirements:
        - 5+ years of experience with Python
        - Strong knowledge of AWS and PostgreSQL
        - Bachelor's degree in Computer Science or equivalent

        Nice to have:
        - Experience with Kubernetes
        - Familiarity with Kafka
        """,
    }

    result = graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": "test-1"}},
    )
    print(result["summary"])


if __name__ == "__main__":
    main()