import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from src_database_search import search_src_database


# =========================================================
# CONFIG
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing from your .env file.")
    st.stop()

st.set_page_config(
    page_title="SRC AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-120b"


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main dark background */
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    /* Main content */
    .main .block-container {
        max-width: 1100px;
        padding-top: 30px;
        padding-bottom: 100px;
    }

    /* Header */
    .src-title {
        text-align: center;
        color: white;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .src-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Welcome card */
    .welcome-card {
        background-color: #1e293b;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #334155;
        margin-bottom: 25px;
    }

    .welcome-title {
        color: white;
        font-size: 22px;
        font-weight: 700;
    }

    .welcome-text {
        color: #e2e8f0;
        font-size: 15px;
        margin-top: 8px;
        line-height: 1.6;
    }

    /* Normal Streamlit text */
    .stMarkdown,
    .stText,
    p,
    li {
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1e293b;
        color: white;
        border: 1px solid #475569;
        border-radius: 10px;
    }

    .stButton > button:hover {
        background-color: #334155;
        color: white;
        border-color: #64748b;
    }

    /* Chat input */
    .stChatInput {
        background-color: #1e293b;
    }

    .stChatInput textarea {
        color: white !important;
        background-color: #1e293b !important;
    }

    .stChatInput textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #111827;
        border-radius: 12px;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        color: white !important;
        background-color: #1e293b;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 40px;
        padding: 20px;
    }

    /* Divider */
    hr {
        border-color: #334155;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 SRC AI Assistant")

    st.caption(
        "Srinivasa Ramanujan Centre\n"
        "SASTRA Deemed University"
    )

    st.divider()

    st.subheader("💡 What can I ask?")

    st.markdown(
        """
        - 📚 Courses & Programmes
        - 👨‍🏫 Faculty Details
        - 👔 Dean & Administration
        - 🏫 Departments
        - 💰 Fees
        - 🎓 Admissions
        - 📅 Academic Information
        - 💼 Training & Placement
        - 🏛️ Campus Facilities
        - 🏆 Student Activities
        - 📞 Contact Information
        """
    )

    st.divider()

    st.subheader("🔗 Official Website")

    st.markdown(
        "[Visit SRC Website](https://src.sastra.edu/)"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.quick_question = None
        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<h1 class="src-title">🎓 SRC AI Assistant</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="src-subtitle">'
    'Your intelligent assistant for Srinivasa Ramanujan Centre'
    '</p>',
    unsafe_allow_html=True
)


# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.title("👋 Hello! How can I help you?")

    st.write(
        "Ask me about SRC programmes, faculty, "
        "administration, admissions, facilities, "
        "placements, academic information and more."
    )

    st.subheader("✨ Quick Questions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "👔 Who is the Dean of SRC?",
            use_container_width=True
        ):
            st.session_state.quick_question = (
                "Who is the Dean of SRC?"
            )
            st.rerun()

    with col2:
        if st.button(
            "📚 What courses are offered?",
            use_container_width=True
        ):
            st.session_state.quick_question = (
                "What courses are offered at SRC?"
            )
            st.rerun()

    with col3:
        if st.button(
            "👨‍🏫 Show faculty details",
            use_container_width=True
        ):
            st.session_state.quick_question = (
                "Show me the faculty details of SRC."
            )
            st.rerun()
# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander("🔗 Sources"):

                for source in message["sources"]:

                    st.markdown(
                        f"- {source}"
                    )


# =========================================================
# GET QUESTION
# =========================================================

question = None

if st.session_state.quick_question:

    question = st.session_state.quick_question

    st.session_state.quick_question = None

else:

    question = st.chat_input(
        "Ask anything about SRC..."
    )


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------
    # USER MESSAGE
    # -----------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    # -----------------------------------------
    # ASSISTANT
    # -----------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🔎 Searching SRC information..."):

            try:

                documents = search_src_database(
                    question,
                    k=5
                )

            except Exception as e:

                st.error(
                    f"Database search error: {e}"
                )

                st.stop()


        # -----------------------------------------
        # NO RESULTS
        # -----------------------------------------

        if not documents:

            answer = (
                "I couldn't find this information in "
                "the available official SRC information."
            )

            sources = []

        else:

            context_parts = []
            sources = []

            for document in documents:

                content = document.page_content

                source = document.metadata.get(
                    "source",
                    "https://src.sastra.edu/"
                )

                context_parts.append(
                    f"""
SOURCE:
{source}

CONTENT:
{content}
"""
                )

                if source not in sources:
                    sources.append(source)


            context = "\n\n".join(context_parts)


            # -----------------------------------------
            # PROMPT
            # -----------------------------------------

            prompt = f"""
You are SRC AI Assistant for
Srinivasa Ramanujan Centre,
SASTRA Deemed University.

Answer the user's question using ONLY
the information provided in the context.

Rules:

1. Do not invent information.
2. Do not guess.
3. If the answer is not available,
   clearly say that you could not find it.
4. Give simple and clear answers.
5. Use bullet points when useful.
6. If the user asks in Tamil,
   answer in Tamil.
7. If the user asks in Tanglish,
   answer in Tanglish.
8. If the user asks in English,
   answer in English.
9. Keep the answer relevant to SRC.

CONTEXT:

{context}

QUESTION:

{question}
"""


            # -----------------------------------------
            # GROQ
            # -----------------------------------------

            try:

                response = client.chat.completions.create(
                    model=MODEL_NAME,

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful SRC "
                                "college assistant."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.2,
                    max_tokens=1000
                )

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

            except Exception as e:

                answer = (
                    "Sorry, I couldn't generate "
                    "a response right now.\n\n"
                    f"Error: {e}"
                )


        # -----------------------------------------
        # DISPLAY ANSWER
        # -----------------------------------------

        st.markdown(answer)


        # -----------------------------------------
        # SOURCES
        # -----------------------------------------

        if sources:

            with st.expander("🔗 Sources"):

                for source in sources:

                    st.markdown(
                        f"- {source}"
                    )


    # =================================================
    # SAVE ASSISTANT MESSAGE
    # =================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'SRC AI Assistant • Powered by Groq • '
    'SRC Information Assistant'
    '</div>',
    unsafe_allow_html=True
)