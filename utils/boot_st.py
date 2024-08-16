# utils/boot_st.py
# each page must run its boot process to initialize all its st.session variables and objects

import streamlit as st
from utils.settings_st import *
from sqlalchemy import create_engine, MetaData
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.llms.ollama import Ollama
from llama_index.llms.groq import Groq
from llama_index.llms.cohere import Cohere
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
import pandas as pd


# 01_chatbot_assistant.py
@st.cache_resource(show_spinner=True)
def init_page_chatbot():
    # init session
    if "boot_chatbot" not in st.session_state.keys():  # Check if boot has been done
        st.session_state.boot_chatboot = True
    
    # init messages
    if "messages_chatbot" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages_chatbot = [
            ChatMessage(role=MessageRole.SYSTEM, content=chinook_system_prompt),
            ChatMessage(role=MessageRole.USER, content=chinook_prompt_01),
            ChatMessage(role=MessageRole.ASSISTANT, content=chinook_reply_01),
            ChatMessage(role=MessageRole.USER, content=chinook_prompt_02),
            ChatMessage(role=MessageRole.ASSISTANT, content=chinook_reply_02),
            ChatMessage(role=MessageRole.USER, content=chinook_prompt_03),
            ChatMessage(role=MessageRole.ASSISTANT, content=chinook_reply_03),
            ChatMessage(role=MessageRole.USER, content=chinook_prompt_04),
            ChatMessage(role=MessageRole.ASSISTANT, content=chinook_reply_04),
            ChatMessage(role=MessageRole.USER, content=chinook_prompt_05),
            ChatMessage(role=MessageRole.ASSISTANT, content=chinook_reply_05),
        ]

    # Initialize or load the metadata DataFrame
    if 'metadata_df' not in st.session_state:
        st.session_state.metadata_df = pd.DataFrame({
            'timestamp': pd.Series(dtype='datetime64[ns]'),
            'message_index': pd.Series(dtype=int),
            'provider': pd.Series(dtype=str),
            'model': pd.Series(dtype=str),
            'user_prompt': pd.Series(dtype=str),
            'elapsed_time': pd.Series(dtype=float),
            'total_messages': pd.Series(dtype=int),
            'estimated_prompt_tokens': pd.Series(dtype=int),
            'estimated_response_tokens': pd.Series(dtype=int),
            'estimated_total_tokens': pd.Series(dtype=int)
        })


    return

# 03_sql_assistant.py
@st.cache_resource(show_spinner=True)
def init_page_database():
    # init session
    if "boot_db" not in st.session_state.keys():  # Check if boot has been done
        st.session_state.boot_db = True
    
    # init messages
    if "messages_db" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages_db = []

    # Initialize the query_history in session state if not present
    if 'query_history' not in st.session_state:
        st.session_state.query_history = {}

    return

@st.cache_resource(show_spinner=True)
def get_db():
    connection_string = db_url
    engine = create_engine(connection_string)
    metadata_obj = MetaData()
    # reflect the database schema into the SQLAlchemy object
    metadata_obj.reflect(bind=engine)
    print("The db engine was created.")
    return engine, metadata_obj

# 01_chatbot_assistant.py
# Initialize all LLM models
@st.cache_resource(show_spinner=True)
def initialize_llms():
    llms = {}
    for provider, model in models:
        if provider == "Ollama":
            llms[(provider, model)] = Ollama(model=model)
        elif provider == "Groq":
            groq_api_key = st.secrets.get("GROQ_API_KEY")
            if not groq_api_key:
                st.error("Groq API key not found in secrets. Groq models will not be available.")
            else:
                llms[(provider, model)] = Groq(model=model, api_key=groq_api_key)
        elif provider == "Cohere":
            cohere_api_key = st.secrets.get("COHERE_API_KEY")
            if not cohere_api_key:
                st.error("Cohere API key not found in secrets. Cohere models will not be available.")
            else:
                llms[(provider, model)] = Cohere(model=model, api_key=cohere_api_key)
        elif provider == "AzureOpenAI":
            azure_openai_api_key = st.secrets.get("AZURE_OPENAI_API_KEY")
            azure_openai_endpoint = st.secrets.get("AZURE_OPENAI_ENDPOINT")
            if not azure_openai_api_key or not azure_openai_endpoint:
                st.error("Azure OpenAI API key or endpoint not found in secrets. Azure OpenAI models will not be available.")
            else:
                llms[(provider, model)] = AzureOpenAI(
                    engine=model,
                    model=model,
                    azure_endpoint=azure_openai_endpoint,
                    api_key=azure_openai_api_key,
                    api_version=azure_openai_api_version,
                )
        elif provider == "OpenAI":
            openai_api_key = st.secrets.get("OPENAI_API_KEY")
            if not openai_api_key:
                st.error("OpenAI API key not found in secrets. OpenAI models will not be available.")
            else:
                llms[(provider, model)] = OpenAI(model=model, api_key=openai_api_key)
    
    return llms