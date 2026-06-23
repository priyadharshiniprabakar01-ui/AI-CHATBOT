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

# -----------------------------
# LLM (LATEST STABLE MODEL)
# -----------------------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
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
        return data.get("extract", "No summary available.")
    except Exception as e:
        return f"Error: {e}"

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Use for math calculations like 2+2 or 10*5"
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia_tool,
        description="Use for general knowledge questions (people, places, history)"
    )
]

# -----------------------------
# PROMPT (REACT FORMAT)
# -----------------------------
prompt = PromptTemplate.from_template("""
You are a helpful AI assistant.

You have tools:
{tools}

Tool names:
{tool_names}

VERY IMPORTANT RULES:
- Only use tools when the question clearly needs them.
- If tools are not needed, directly give Final Answer.
- NEVER write "Action: None"
- NEVER hallucinate tool usage.
- Keep response simple and direct.

Format:

Question: {input}

If tool is needed:
Thought: decide to use tool
Action: tool name
Action Input: input
Observation: result
Thought: final reasoning
Final Answer: response

If NO tool is needed:
Thought: I can answer directly
Final Answer: response

Begin.

Question: {input}
{agent_scratchpad}
""")
# -----------------------------
# AGENT
# -----------------------------
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    max_iterations=2,
    handle_parsing_errors=True
)
# -----------------------------
# MAIN LOOP
# -----------------------------
def get_response(query):
    try:
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        return f"Error: {e}"