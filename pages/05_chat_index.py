# pages/05_chat_index.py
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import datetime

# Load and preprocess data
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def load_data():
    df = pd.read_csv("log/metadata.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def preprocess_prompts(df):
    def categorize_prompt(prompt):
        if isinstance(prompt, str):
            if prompt.strip().startswith('SELECT'):
                return 'SQL QUERY'
            elif prompt.strip().startswith('['):
                return 'JSON OBJECT'
        return prompt

    new_df = df.copy()
    new_df['processed_prompt'] = new_df['user_prompt'].apply(categorize_prompt)
    return new_df

def main():
    st.title("Chat History Dashboard")
    
    # Click the refresh button to check for updates in the .csv file
    if st.sidebar.button('Refresh Data'):
        # This will clear all cached data
        st.cache_data.clear()
    
    # load the .csv file
    df = load_data()

    # Sidebar for time range selection
    st.sidebar.header("Time Range Selection")
    
    # Get min and max dates from the dataframe
    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()
    
    # Create a date range slider
    start_date = st.sidebar.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End date", max_date, min_value=min_date, max_value=max_date)
    
    if start_date > end_date:
        st.error("Error: End date must be after start date.")
        return
    
    # Filter dataframe based on selected date range
    mask = (df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)
    filtered_df = df.loc[mask]

    # Overall Statistics
    st.header("Selected range")
    # Display selected date range
    st.write(f"Analyzing data from {start_date} to {end_date}")
    st.metric("Data Points included in Range: ", len(filtered_df))
    
    st.header("Overall Statistics")
    total_queries = len(filtered_df)
    avg_response_time = filtered_df['elapsed_time'].mean()

    col1, col2 = st.columns(2)
    col1.metric("Total Queries", total_queries)
    col2.metric("Avg Response Time", f"{avg_response_time:.2f} seconds")

    processed_df = preprocess_prompts(filtered_df)

    # Most Frequent User Queries
    st.header("Most Frequent User Queries")
    # Filter out 'SQL QUERY' and 'JSON OBJECT' from word count, and ignore words with 3 letters or less
    word_counts = Counter(
    word.lower()
    for prompt in processed_df[processed_df['processed_prompt'].isin(['SQL QUERY', 'JSON OBJECT']) == False]['processed_prompt']
    for word in prompt.split()
    if len(word) > 3
    )
    top_queries = word_counts.most_common(10)
    top_queries_df = pd.DataFrame(top_queries, columns=['Word', 'Frequency'])
    fig_top_queries = px.bar(top_queries_df, x='Word', y='Frequency', title='Top 10 Words in User Queries (>3 letters)')
    st.plotly_chart(fig_top_queries)

    # Query Type Distribution
    st.header("Query Type Distribution")
    query_type_dist = processed_df['processed_prompt'].apply(lambda x: 'SQL QUERY' if x == 'SQL QUERY' else ('JSON OBJECT' if x == 'JSON OBJECT' else 'Other')).value_counts()
    fig_query_type_dist = px.pie(values=query_type_dist.values, names=query_type_dist.index, 
                                 title='Distribution of Query Types')
    st.plotly_chart(fig_query_type_dist)

    # Query Distribution by Provider
    st.header("Query Distribution by Provider")
    provider_dist = filtered_df['provider'].value_counts()
    fig_provider_dist = px.pie(values=provider_dist.values, names=provider_dist.index, 
                               title='Query Distribution by Provider')
    st.plotly_chart(fig_provider_dist)

    # Model Performance
    st.header("Model Performance")
    model_performance = filtered_df.groupby('model')['elapsed_time'].mean().sort_values(ascending=False)
    fig_model_perf = px.bar(model_performance, x=model_performance.index, y='elapsed_time', 
                            title='Average Response Time by Model')
    st.plotly_chart(fig_model_perf)
    
    # Response Time Distribution
    st.header("Response Time Distribution")
    fig_resp_time_dist = px.histogram(filtered_df, x='elapsed_time', nbins=20, 
                                      title='Distribution of Response Times')
    st.plotly_chart(fig_resp_time_dist)

    # Recent Activity
    st.header("10 Recent Queries")
    st.dataframe(processed_df[['timestamp', 'provider', 'model', 'processed_prompt', 'elapsed_time']].tail(10).sort_values('timestamp', ascending=False))

if __name__ == "__main__":
    main()