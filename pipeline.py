import os
from dotenv import load_dotenv
from tavily import TavilyClient
from agents import search_agent, reader_agent, writer_agent, critic_agent

# Load environment variables
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")

# Initialize Tavily client
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def fetch_tavily_snippets(query, max_results=5):
    """
    Fetches clean content or snippets from Tavily search results.
    """
    results = tavily.search(query=query, max_results=max_results)
    snippets = []
    for res in results.get("results", []):
        # Prefer 'content', fallback to 'snippet'
        snippet = res.get("content") or res.get("snippet")
        if snippet:
            snippets.append(f"- Source: {res.get('url', '')}\n{snippet}")
    return "\n\n".join(snippets)

def main():
    print("=== Multi-Agent AI Research System ===")
    user_input = input("Enter your research topic or question: ").strip()
    if not user_input:
        print("No input provided. Exiting.")
        return

    # 1. Search Agent: Generate search query
    search_query = search_agent(user_input)
    print(f"\n[Search Agent] Query: {search_query}")

    # 2. Tavily API: Fetch top results
    snippets = fetch_tavily_snippets(search_query)
    if not snippets:
        print("No relevant results found from Tavily.")
        return
    print(f"\n[Tavily] Retrieved {snippets.count('- Source:')} snippets.")

    # 3. Reader Agent: Extract deep insights
    insights = reader_agent(snippets)
    print("\n[Reader Agent] Extracted Insights:\n", insights)

    # 4. Writer Agent: Generate analytical report
    report = writer_agent(insights)
    print("\n[Writer Agent] Analytical Report:\n", report)

    # 5. Critic Agent: Evaluate the report
    critique = critic_agent(report)
    print("\n[Critic Agent] Evaluation:\n", critique)

    # 6. Save final report
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write("=== Analytical Research Report ===\n\n")
        f.write(report)
        f.write("\n\n=== Critic Evaluation ===\n\n")
        f.write(critique)
    print('\nFinal report saved to "final_report.txt".')

if __name__ == "__main__":
    main()