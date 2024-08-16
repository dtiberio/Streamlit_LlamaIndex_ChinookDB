# pages/01_chatbot_assistant.py
import streamlit as st
import pandas as pd
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from utils.boot_st import init_page_chatbot, initialize_llms
from utils.settings_st import models
from utils.helpers_st import get_user_input, display_chat_history

# Streamlit App
st.title("Chatbot assistant")
if "boot_chatbot" not in st.session_state.keys():
    init_page_chatbot()

llms = initialize_llms()

# Dropdown for model selection in the sidebar
with st.sidebar:
    st.header("Model Selection")
    available_models = [(provider, model) for provider, model in models if (provider, model) in llms]
    
    # Initialize default values in session state if not present
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = available_models[0][0]
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = available_models[0][1]
    
    selected_provider, selected_model = st.selectbox(
        "Choose an LLM model for the next question:",
        available_models,
        format_func=lambda x: f"{x[0]} - {x[1]}",
        index=available_models.index((st.session_state.selected_provider, st.session_state.selected_model))
    )
    
    # Update session state
    st.session_state.selected_provider = selected_provider
    st.session_state.selected_model = selected_model

    # Print selected model information
    st.write(f"Current Provider: {st.session_state.selected_provider}")
    st.write(f"Current Model: {st.session_state.selected_model}")

# Print current length of messages list
st.sidebar.write(f"Current number of messages: {len(st.session_state.messages_chatbot)-11}")

display_chat_history()

get_user_input()

# Add a button to clear the chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages_chatbot = st.session_state.messages_chatbot[0:11]  # Keep the first 11 messages
    st.rerun()
