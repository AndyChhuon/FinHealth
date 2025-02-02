# modules/chatbot.py
import streamlit as st
from openai import OpenAI

def chatbot(system_prompt, conversation_messages):
    """
    Takes:
      - system_prompt (str): the system instructions
      - conversation_messages (list[dict]): each dict has "role" and "content"
    
    Returns:
      - final_text (str): The entire assistant response from streaming, 
        so the caller can display it wherever desired.
    """
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
