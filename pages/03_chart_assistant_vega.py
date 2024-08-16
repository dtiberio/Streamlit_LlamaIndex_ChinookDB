# pages/03_chart_assistant_vega.py
import streamlit as st
import pandas as pd
import altair as alt

def create_chart(df, chart_type, x_column, y_column):
    if chart_type == "bar":
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(x_column, title=x_column),
            y=alt.Y(y_column, title=y_column)
        ).interactive()
    elif chart_type == "line":
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X(x_column, title=x_column),
            y=alt.Y(y_column, title=y_column)
        ).interactive()
    else:  # circle (scatter plot)
        chart = alt.Chart(df).mark_circle().encode(
            x=alt.X(x_column, title=x_column),
            y=alt.Y(y_column, title=y_column)
        ).interactive()

    return chart

def main():
    st.title("Chart Assistant Vega-Altair")

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
                chart_type = st.selectbox(f"Select chart type for Query {query_number}", ["bar", "line", "circle"])
                columns = result.columns.tolist()
                x_column = st.selectbox(f"Select X-axis column for Query {query_number}", columns)
                numeric_columns = result.select_dtypes(include=['int64', 'float64']).columns.tolist()
                y_column = st.selectbox(f"Select Y-axis column for Query {query_number}", numeric_columns)
                
                if st.button(f"Generate Chart for Query {query_number}"):
                    chart = create_chart(result, chart_type, x_column, y_column)
                    st.altair_chart(chart, use_container_width=True)
            else:
                st.error(f"Error: {result}")

if __name__ == "__main__":
    main()