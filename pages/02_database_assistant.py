# pages/02_sql_assistant.py
import streamlit as st
from sqlalchemy import text
import pandas as pd
from utils.boot_st import init_page_database, get_db
import json
import pyperclip
import logging

# Function to execute SQL query
def execute_sql_query(query, engine):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            columns = result.keys()
            data = result.fetchall()
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        return str(e)

# Function to sample top 5 rows and copy to clipboard as JSON
def sample_and_copy_to_clipboard(df):
    try:
        if len(df) > 0:
            sample = df.head(5).to_dict(orient='records')
            json_sample = json.dumps(sample, indent=2)
            pyperclip.copy(json_sample)
            return True
        return False
    except Exception as e:
        logging.error(f"Error in sample_and_copy_to_clipboard: {str(e)}")
        return False

# Streamlit app
st.title("Database Assistant")
if "boot_db" not in st.session_state.keys():
    init_page_database()

# Option to clear query history
if st.sidebar.button("Clear Query History"):
    st.session_state.query_history = {}
    st.rerun()

# Database connection
engine, metadata_db = get_db()

# Chat input for SQL query
query = st.chat_input("Enter your SQL query:")
if query:
    # Execute query and get response
    response = execute_sql_query(query, engine)
    
    # Save query and result to session state
    if isinstance(response, pd.DataFrame):
        st.session_state.query_history[query] = response
        st.success("Query executed successfully!")
        st.dataframe(response)
    else:
        st.session_state.query_history[query] = f"Error: {response}"
        st.error(f"Error executing query: {response}")

# Display query history
st.header("SQL Query History")
total_queries = len(st.session_state.query_history)
query_items = list(st.session_state.query_history.items())

for i, (past_query, result) in enumerate(reversed(query_items), 1):
    query_number = total_queries - i + 1  # Calculate the correct query number
    with st.expander(f"Query {query_number} of {total_queries}: {past_query[:50]}..."):
        st.code(past_query, language="sql")
        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
            if st.button(f"Copy Top 5 rows from Query {query_number}"):
                if sample_and_copy_to_clipboard(result):
                    st.success("Top 5 rows copied to clipboard in JSON format!")
                else:
                    st.warning("No data to copy.")
        else:
            st.error(result)
        if st.button(f"Re-execute Query {query_number}"):
            response = execute_sql_query(past_query, engine)
            if isinstance(response, pd.DataFrame):
                st.session_state.query_history[past_query] = response
                st.success("Query re-executed successfully!")
                st.dataframe(response)
            else:
                st.session_state.query_history[past_query] = f"Error: {response}"
                st.error(f"Error executing query: {response}")
