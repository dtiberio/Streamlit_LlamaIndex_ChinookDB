# # Chinook Database Dashboard and Analytics App

This Streamlit application provides a comprehensive dashboard and analytics tools for the Chinook database. It offers an interactive interface for data exploration, SQL querying, data visualization, and AI-powered analytics using various language models.

## Features

- Main Dashboard: Overview of the Chinook database structure and key insights
  - Database statistics (total tables, rows, columns)
  - Table information with row counts
  - Entity Relationship Diagram
  - Data visualizations including top artists by track count, genre distribution, and sales over time

- Chatbot Assistant: Interact with various Language Models (LLMs) to analyze the Chinook database
  - Support for multiple LLM providers and models (Ollama, Groq, Cohere, Azure OpenAI, OpenAI)
  - Conversational interface for asking questions and receiving insights

- Database Assistant: 
  - View and re-execute SQL query history
  - Copy query results to clipboard

- Chart Assistant: Visualize SQL query results
  - Supports bar charts, line charts, and scatter plots
  - Interactive selection of chart type and data columns

- Chat Index: Analytics on Chatbot Assistant usage
  - Overall statistics (total queries, average response time)
  - Most frequent user queries
  - Query type distribution
  - Model performance and response time analysis
  - Recent activity log

## Setup

1. Clone the repository:

```bash
git clone https://github.com/dtiberio/Streamlit_LlamaIndex_ChinookDB.git
cd Streamlit_LlamaIndex_ChinookDB
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Obtain API keys for the LLM providers you plan to use (Groq, Cohere, OpenAI, Azure OpenAI) and add them to a `.streamlit/secrets.toml` file in the project root directory, using the format provided in `secrets.txt`.

4. To use Ollama models, ensure you have Ollama installed locally and the required models downloaded. Start the Ollama server with `ollama serve` before running the Streamlit app.

5. Run the Streamlit app:

```bash
streamlit run app_st_main.py
```

6. Access the dashboard by opening the provided URL in your web browser.

## File Structure

- `app_st_main.py`: Main Streamlit app script, contains the dashboard
- `pages/01_chatbot_assistant.py`: Chatbot Assistant page
- `pages/02_database_assistant.py`: Database Assistant page
- `pages/03_chart_assistant_vega.py`: Chart Assistant page using Vega-Altair (not used)
- `pages/04_chart_assistant_plotly.py`: Chart Assistant page using Plotly
- `pages/05_chat_index.py`: Chat Index page for Chatbot Assistant analytics
- `pages/06_about.py`: About page with project information
- `utils/boot_st.py`: Initialization functions for Streamlit app
- `utils/helpers_st.py`: Helper functions for Streamlit app
- `utils/settings_st.py`: Configuration settings for Streamlit app
- `db/Chinook_Sqlite.sqlite`: SQLite database file for Chinook
- `db/chinookDB.png`: Entity Relationship Diagram image for Chinook database
- `log/metadata.csv`: Log file for Chatbot Assistant interactions
- `requirements.txt`: Python package requirements
- `secrets.txt`: Template for secret keys (copy to `.streamlit/secrets.toml`)

## Final notes

I have developed this code as part of a project for a bootcamp on Data Analysis and Data Science.  
It covers a range of differente topics, such as SQL databases, LlamaIndex and LLM models, Streamlit dashboards and data visualization, that we've learnt during the bootcamp, as such, I've really enjoyed working on it.  

I share this code in the hope that you might find it useful to learn about these topics and to develop your skills.

Have fun with it!  