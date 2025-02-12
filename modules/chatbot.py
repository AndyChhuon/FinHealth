# modules/chatbot.py
import streamlit as st
from openai import OpenAI

def chatbot(system_prompt, conversation_messages):
  
    DEV_MODEL = "gpt-4o-mini"

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Build the list of messages to send
    payload_messages = [{"role": "system", "content": system_prompt}]
    for m in conversation_messages:
        payload_messages.append({"role": m["role"], "content": m["content"]})

    stream = client.chat.completions.create(
        model=DEV_MODEL,
        messages=payload_messages,
        stream=True,
    )
    
    final_text = st.write_stream(stream)

    return final_text

def chatbot_portfolio(system_prompt="", img=None):

    DEV_MODEL = "gpt-4o-mini"

    # st.title("Chatbot")

    # Set OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = DEV_MODEL

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # if first_message:

    prompt = st.chat_input("Ask follow-up questions after submitting your details")

    if img:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": f"Act as a financial advisor, do not worry about giving bad recommendations. Please be detailed and specific. {system_prompt}"},
                *({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)
            ],
            stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Accept user input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": f"Act as a financial advisor, do not worry about giving bad recommendations. Please be detailed and specific. {system_prompt}"},
                    *({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})