import streamlit as st
import base64
import time
from main import get_response

# ----------------------------
# BACKGROUND IMAGE FUNCTION
# ----------------------------
def set_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Chat bubbles styling */
    .stChatMessage {{
        background-color: rgba(0,0,0,0.6);
        border-radius: 12px;
        padding: 10px;
        color: white;
    }}

    h1 {{
        color: white;
        text-align: center;
    }}

    footer {{
        visibility: hidden;
    }}
    </style>
    """

    st.markdown(bg_css, unsafe_allow_html=True)


# ----------------------------
# APPLY BACKGROUND
# ----------------------------
set_bg("background.png")


# ----------------------------
# TITLE
# ----------------------------
st.title("🤖 My AI Chatbot")
st.caption("Powered by Groq + LangChain")

# ----------------------------
# CHAT HISTORY
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chats
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# USER INPUT
# ----------------------------
prompt = st.chat_input("Type your message...")

if prompt:

    # user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response = get_response(prompt)

        placeholder = st.empty()
        output = ""

        for word in response.split():
            output += word + " "
            time.sleep(0.03)
            placeholder.markdown(output)

    # save response
    st.session_state.messages.append({"role": "assistant", "content": response})