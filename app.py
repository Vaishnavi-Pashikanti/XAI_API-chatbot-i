import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Page config
st.set_page_config(page_title="Grok AI Chatbot", page_icon="🤖", layout="wide")

# Initialize OpenAI client with X.AI configuration
XAI_API_KEY = os.getenv("XAI_API_KEY")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Grok, a chatbot that helps user to assist in a best way."}
    ]

def get_grok_response(messages):
    """Get response from Grok API"""
    try:
        completion = client.chat.completions.create(
            model="grok-beta",
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response from Grok: {str(e)}")
        return None

def main():
    st.title("🤖 Grok AI Chatbot")

    for message in st.session_state.messages:
        if message["role"] != "system":  # Don't display system messages
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are Grok, a chatbot that helps user to assist in a best way."}
        ]

    prompt = st.chat_input("What would you like to ask Grok?")
    if prompt :
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_grok_response(st.session_state.messages)
            
            if response:
                st.write(response)
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

if __name__ == "__main__":
    main()