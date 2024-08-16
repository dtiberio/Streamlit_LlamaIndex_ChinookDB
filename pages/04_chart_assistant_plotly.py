# pages/04_chart_assistant_plotly.py
import streamlit as st
import pandas as pd
import plotly.express as px

def create_chart(df, chart_type, x_column, y_column):
    if chart_type == "bar":
        fig = px.bar(df, x=x_column, y=y_column, title=f"{y_column} by {x_column}")
    elif chart_type == "line":
        fig = px.line(df, x=x_column, y=y_column, title=f"{y_column} over {x_column}")
    else:  # scatter
        fig = px.scatter(df, x=x_column, y=y_column, title=f"{y_column} vs {x_column}")
    
    fig.update_layout(xaxis_title=x_column, yaxis_title=y_column)
    return fig

def main():
    st.title("Chart Assistant with Plotly")

    # Initialize query_history if it doesn't exist
    if 'query_history' not in st.session_state:
        st.session_state.query_history = {}

    # Display query history in reverse order
    st.header("SQL Query History")
    total_queries = len(st.session_state.query_history)
    for i, (query, result) in enumerate(reversed(list(st.session_state.query_history.items())), 1):
        query_number = total_queries - i + 1  # Calculate the original query number
        with st.expander(f"Query {query_number} of {total_queries}: {query[:50]}..."):
            st.code(query, language='sql')
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
                
                # User selects chart type and columns
                chart_type = st.selectbox(f"Select chart type for Query {query_number}", ["bar", "line", "scatter"])
                columns = result.columns.tolist()
                x_column = st.selectbox(f"Select X-axis column for Query {query_number}", columns)
                numeric_columns = result.select_dtypes(include=['int64', 'float64']).columns.tolist()
                y_column = st.selectbox(f"Select Y-axis column for Query {query_number}", numeric_columns)
                
                if st.button(f"Generate Chart for Query {query_number}"):
                    fig = create_chart(result, chart_type, x_column, y_column)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Error: {result}")

if __name__ == "__main__":
    main()