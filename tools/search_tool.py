from langchain.tools import tool
from ddgs import DDGS


@tool
def search_tool(query: str):
    """
    Useful for real-time web search.
    """

    results = []

    with DDGS() as ddgs:

        search_results = list(
            ddgs.text(
                query,
                max_results=5
            )
        )

        for r in search_results:

            results.append(
                f"""
Title: {r.get('title', '')}

Body: {r.get('body', '')}

Link: {r.get('href', '')}
"""
            )

    return "\n".join(results)