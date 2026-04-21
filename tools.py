from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# @tool
# def web_search(query: str) -> str:
#     """Search the web for recent and reliable information on a topic. Return Titles, URLs and snippets."""
#     results=tavily.search(query=query, max_results=5)

#     out =[]
#     for r in results['results']:
#         out.append(
#                 f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
#         )
#     return "\n----\n".join(out)

from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic."""

    results = tavily.search(query=query, max_results=5)

    out = []

    for r in results.get("results", []):
        title = r.get("title", "No title")
        url = r.get("url", "No URL")
        content = r.get("content", "")

        snippet = content[:300] if content else "No content available"

        out.append(
            f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n"
        )

    if not out:
        return "No relevant results found."

    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp=requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soap=BeautifulSoup(resp.text, 'html.parser')
        # Remove scripts and styles
        for tag in soap(['script', 'style', 'nav','footer']):
            tag.decompose()
        return soap.get_text(separator='\n', strip=True)[:3000]  # Return first 3000 chars
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

