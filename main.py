import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not found. Check your .env file.")

# -----------------------------
# GROQ LLM
# -----------------------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0
)

# -----------------------------
# TOOLS
# -----------------------------

def calculator(query: str) -> str:
    try:
        return str(eval(query))
    except Exception as e:
        return f"Error: {e}"


def wikipedia_tool(query: str) -> str:
    import requests

    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

        r = requests.get(url)

        if r.status_code != 200:
            return "No result found."

        data = r.json()

        return data.get(
            "extract",
            "No summary available."
        )

    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# TOOL LIST
# -----------------------------

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Use this tool for mathematical calculations such as 2+2, 10*5, 100/4."
    ),

    Tool(
        name="Wikipedia",
        func=wikipedia_tool,
        description="Use this tool for general knowledge questions about people, places, history and other factual topics."
    )
]

# -----------------------------
# REACT PROMPT
# -----------------------------

prompt = PromptTemplate.from_template("""
You are a helpful AI assistant.

You have access to the following tools:

{tools}

Tool names:

{tool_names}

IMPORTANT RULES:

- Only use a tool when the question clearly requires it.
- If a tool is not required, answer directly.
- Never write "Action: None".
- Never pretend that you used a tool when you did not.
- Keep answers simple, clear and useful.

When using a tool, follow this format:

Question: {input}

Thought: decide whether a tool is required
Action: tool name
Action Input: input
Observation: result
Thought: prepare the final answer
Final Answer: response

If no tool is required:

Question: {input}

Thought: I can answer directly
Final Answer: response

Begin.

Question: {input}

{agent_scratchpad}
""")

# -----------------------------
# CREATE AGENT
# -----------------------------

agent = create_react_agent(
    llm,
    tools,
    prompt
)

# -----------------------------
# AGENT EXECUTOR
# -----------------------------

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    max_iterations=2,
    handle_parsing_errors=True
)

# -----------------------------
# FUNCTION FOR STREAMLIT
# -----------------------------

def get_response(query):

    try:
        result = agent_executor.invoke(
            {"input": query}
        )

        return result["output"]

    except Exception as e:

        return f"Error: {e}"
