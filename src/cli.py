from .graph_agent import ask


def main() -> None:
    print("Agentic RAG Knowledge Base Assistant")
    print("输入问题开始，输入 exit 退出。\n")
    while True:
        q = input("你: ").strip()
        if q.lower() in {"exit", "quit", "q"}:
            break
        if not q:
            continue
        result = ask(q)
        print("\nAgent:")
        print(result["answer"])
        print()


if __name__ == "__main__":
    main()
