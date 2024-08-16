# pages/06_about.py
import streamlit as st
from utils.settings_st import models

def main():
    st.title("About This Streamlit App")

    st.write("This application is designed to work with the Chinook database, providing various tools for data analysis and visualization.")

    # Introduction
    with st.expander("Introduction to Chinook Database and SQLite"):
        st.write("""
        The Chinook database is a sample database available for SQL Server, Oracle, MySQL, etc. 
        It represents a digital media store, including tables for artists, albums, media tracks, invoices, and customers.

        SQLite is a C library that provides a lightweight disk-based database that doesn't require a separate server process. 
        It allows accessing the database using a nonstandard variant of the SQL query language.
        """)
        st.markdown("[Learn more about Chinook Database](https://github.com/lerocha/chinook-database)")
        st.markdown("[SQLite Official Website](https://www.sqlite.org/)")

    # Main Dashboard
    with st.expander("Main Dashboard"):
        st.write("""
        The main dashboard provides an overview of the Chinook database structure and key insights:
        - Database statistics (total tables, rows, columns)
        - Table information with row counts
        - Entity Relationship Diagram
        - Data visualizations including top artists by track count, genre distribution, and sales over time
        """)

# Chatbot Assistant
    with st.expander("Chatbot Assistant"):
        st.write("""
        The Chatbot Assistant allows users to interact with various Language Models (LLMs) to analyze the Chinook database. 
        It supports multiple LLM providers and models:
        """)
        
        providers = set(provider for provider, _ in models)
        for provider in providers:
            st.subheader(provider)
            if provider == "Ollama":
                st.write("Ollama is an open-source project that allows running large language models locally.")
                st.markdown("[Ollama Official Website](https://ollama.ai/)")
            elif provider == "Groq":
                st.write("Groq is a cloud AI platform known for its high-speed inference.")
                st.markdown("[Groq Official Website](https://groq.com/)")
            elif provider == "Cohere":
                st.write("Cohere provides access to large language models through its cloud platform.")
                st.markdown("[Cohere Official Website](https://cohere.ai/)")
            elif provider == "AzureOpenAI":
                st.write("Azure OpenAI Service provides REST API access to OpenAI's powerful language models.")
                st.markdown("[Azure OpenAI Service Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)")
            
            st.write("Available models:")
            for mod_provider, model in models:
                if mod_provider == provider:
                    if provider == "Ollama":
                        if "gemma" in model:
                            st.write(f"- {model}: A lightweight and efficient language model developed by Google.")
                        elif "llama" in model:
                            st.write(f"- {model}: An open-source large language model developed by Meta AI.")
                    elif provider == "Groq":
                        if "mixtral" in model:
                            st.write(f"- {model}: A powerful mixture-of-experts model known for its versatility.")
                        elif "llama" in model:
                            st.write(f"- {model}: Fine-tuned version of Meta's LLaMA model, optimized for Groq's platform.")
                        elif "gemma" in model:
                            st.write(f"- {model}: Google's Gemma model, adapted for Groq's high-speed inference.")
                    elif provider == "Cohere":
                        st.write(f"- {model}: A proprietary model developed by Cohere, optimized for various NLP tasks.")
                    elif provider == "AzureOpenAI":
                        st.write(f"- {model}: A deployment of OpenAI's models on Microsoft Azure, offering enterprise-grade capabilities.")

    # Database Assistant
    with st.expander("Database Assistant"):
        st.write("""
        The Database Assistant page allows users to:
        - View the history of executed SQL queries
        - Re-execute previous queries
        - Copy query results to the clipboard
        This tool is useful for database administrators and analysts who need to track and reuse their SQL queries.
        """)

    # Chart Assistant
    with st.expander("Chart Assistant"):
        st.write("""
        The Chart Assistant provides visualization capabilities for SQL query results:
        - Displays the history of executed queries
        - Allows users to select different chart types (bar, line, scatter) for each query result
        - Users can choose which columns to use for X and Y axes
        - Generates interactive charts based on user selections
        """)
        st.subheader("Plotly vs Vega-Altair")
        st.write("""
        This application uses Plotly for chart generation, but it's worth comparing it to Vega-Altair:
        
        Plotly:
        - Highly interactive and customizable
        - Extensive chart types and 3D visualizations
        - Larger library size, which can affect load times
        
        Vega-Altair:
        - Declarative API based on Vega and Vega-Lite
        - Simpler syntax for basic charts
        - Lighter weight, faster initial render times
        
        Both libraries are excellent choices for data visualization, with Plotly offering more out-of-the-box interactivity and Vega-Altair providing a more concise API for common chart types.
        """)
        st.markdown("[Learn more about Plotly](https://plotly.com/python/)")
        st.markdown("[Learn more about Vega-Altair](https://altair-viz.github.io/)")

    # Chat Index
    with st.expander("Chat Index"):
        st.write("""
        The Chat Index page provides analytics on the usage of the Chatbot Assistant:
        - Displays overall statistics like total queries and average response time
        - Shows most frequent user queries
        - Presents query type distribution
        - Offers insights into model performance and response time distribution
        - Lists recent activity
        This page is useful for understanding how the chatbot is being used and which models are performing best.
        """)

    # Additional Resources
    with st.expander("Additional Resources"):
        st.write("Here are some additional resources for learning more about the technologies used in this app:")
        st.markdown("- [Streamlit Documentation](https://docs.streamlit.io/)")
        st.markdown("- [Pandas Documentation](https://pandas.pydata.org/docs/)")
        st.markdown("- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)")

if __name__ == "__main__":
    main()