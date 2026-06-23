from langchain.tools import Tool
import requests

# -----------------------------
# 1. Calculator Tool
# -----------------------------
def calculator(query: str) -> str:
    try:
        return str(eval(query))
    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# 2. Wikipedia Tool
# -----------------------------
def wikipedia_search(query: str) -> str:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url)
        if response.status_code != 200:
            return "No result found."

        data = response.json()
        return data.get("extract", "No summary available.")
    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# 3. Simple Web Info Tool (basic)
# -----------------------------
def web_info(query: str) -> str:
    try:
        return f"You searched for: {query}. (Add real API here like SerpAPI or Tavily)"
    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# TOOL LIST (IMPORTANT)
# -----------------------------
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Use for math calculations like 2+2, 10*5, etc."
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia_search,
        description="Use for general knowledge questions about people, places, history."
    ),
    Tool(
        name="WebSearch",
        func=web_info,
        description="Use for general web-related queries (placeholder tool)."
    )
]