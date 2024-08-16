# utils/helpers_st.py
import streamlit as st
import pandas as pd
import time
import os
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from utils.boot_st import initialize_llms

# Display chat messages
def display_chat_history():
    for idx, message in enumerate(st.session_state.messages_chatbot[11:], start=1):  # Skip the system message and training prompts
        with st.chat_message(message.role.value):
            st.write(message.content)
        if message.role == MessageRole.ASSISTANT:
            metadata = st.session_state.metadata_df[st.session_state.metadata_df['message_index'] == idx]
            if not metadata.empty:
                st.caption(f"Answered by: {metadata['provider'].values[0]} - {metadata['model'].values[0]}")

def estimate_tokens(text: str) -> int:
    """Rough estimation of tokens based on word count."""
    return len(text.split())

def get_user_input():
    llms = initialize_llms()

    user_input = st.chat_input("Ask a question:")

    if user_input:
        # Add user message to chat history
        user_message = ChatMessage(role=MessageRole.USER, content=user_input)
        st.session_state.messages_chatbot.append(user_message)
        with st.chat_message("user"):
            st.write(user_input)
        
        # Estimate tokens for user input
        user_tokens = estimate_tokens(user_input)

        # Generate LLM response
        with st.chat_message("assistant"):
            with st.spinner(f"Generating response using {st.session_state.selected_model}..."):
                llm = llms[(st.session_state.selected_provider, st.session_state.selected_model)]
                
                start_time = time.time()
                response = llm.chat(st.session_state.messages_chatbot)
                end_time = time.time()
                
                elapsed_time = end_time - start_time
                
                st.write(response.message.content)
        
        # Estimate tokens for response
        response_tokens = estimate_tokens(response.message.content)

        # Add assistant message to chat history
        assistant_message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response.message.content,
        )
        st.session_state.messages_chatbot.append(assistant_message)

        # Update metadata DataFrame
        new_metadata = pd.DataFrame({
            'timestamp': [pd.Timestamp.now()],
            'message_index': [len(st.session_state.messages_chatbot) - 1],
            'provider': [st.session_state.selected_provider],
            'model': [st.session_state.selected_model],
            'user_prompt': [user_input],
            'elapsed_time': [elapsed_time],
            'total_messages': [len(st.session_state.messages_chatbot)],
            'estimated_prompt_tokens': [user_tokens],
            'estimated_response_tokens': [response_tokens],
            'estimated_total_tokens': [user_tokens + response_tokens]
        })
        st.session_state.metadata_df = pd.concat([st.session_state.metadata_df, new_metadata], ignore_index=True)

        # Append new metadata to CSV file, excluding 'message_index'
        csv_path = "log/metadata.csv"
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)  # Ensure the directory exists
        new_metadata_for_csv = new_metadata.drop(columns=['message_index'])
        new_metadata_for_csv.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)

        # Display model info for the current response
        st.caption(f"Answered by: {st.session_state.selected_provider} - {st.session_state.selected_model} in {elapsed_time:.2f} seconds. Session total messages: {len(st.session_state.messages_chatbot)}")
        st.caption(f"Estimated tokens - Prompt: {user_tokens}, Response: {response_tokens}, Total: {user_tokens + response_tokens}")
