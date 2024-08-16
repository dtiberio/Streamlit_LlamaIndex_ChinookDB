# app_st_main.py

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import func
from utils.boot_st import get_db
from PIL import Image

st.set_page_config(page_title="Chinook Database Dashboard", page_icon="🎵", layout="wide", initial_sidebar_state="auto", menu_items=None)

def get_table_row_count(engine, table):
    with engine.connect() as connection:
        result = connection.execute(func.count().select().select_from(table))
        return result.scalar()

def main():
    st.title("Chinook Database Dashboard 🎵💽")

    st.info("This dashboard provides an overview of the Chinook database structure and some key insights from the data.", icon="ℹ️")

    # Get database connection and metadata
    engine, metadata = get_db()

    # Database Statistics
    st.header("Database Overview")
    col1, col2, col3 = st.columns(3)
    
    total_tables = len(metadata.tables)
    col1.metric("Total Tables", total_tables)
    
    total_rows = sum(get_table_row_count(engine, table) for table in metadata.tables.values())
    col2.metric("Total Rows", total_rows)
    
    total_columns = sum(len(table.columns) for table in metadata.tables.values())
    col3.metric("Total Columns", total_columns)

    # Table Information
    st.header("Table Information")
    table_info = []
    for table_name, table in metadata.tables.items():
        row_count = get_table_row_count(engine, table)
        table_info.append({
            "Table Name": table_name,
            "Columns": len(table.columns),
            "Rows": row_count
        })
    
    df_table_info = pd.DataFrame(table_info)
    
    # Bar chart for table sizes
    fig_table_sizes = px.bar(df_table_info, x="Table Name", y="Rows", 
                             title="Number of Rows per Table", 
                             labels={"Rows": "Number of Rows"},
                             color="Table Name")
    st.plotly_chart(fig_table_sizes, use_container_width=True)

    # Table with detailed information
    st.dataframe(df_table_info.set_index("Table Name"), use_container_width=True)

    # ER Diagram
    st.header("Entity Relationship Diagram")
    er_image = Image.open("db/chinookDB.png")
    st.image(er_image, caption="Chinook Database ER Diagram", use_column_width=True)

    # Additional Visualizations
    st.header("Data Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Top 10 Artists by Track Count
        query_top_artists = """
        SELECT Artist.Name, COUNT(Track.TrackId) as TrackCount
        FROM Artist
        JOIN Album ON Artist.ArtistId = Album.ArtistId
        JOIN Track ON Album.AlbumId = Track.AlbumId
        GROUP BY Artist.ArtistId
        ORDER BY TrackCount DESC
        LIMIT 10
        """
        df_top_artists = pd.read_sql(query_top_artists, engine)
        fig_top_artists = px.bar(df_top_artists, x="Name", y="TrackCount", 
                                 title="Top 10 Artists by Track Count",
                                 labels={"Name": "Artist", "TrackCount": "Number of Tracks"},
                                 color="TrackCount")
        st.plotly_chart(fig_top_artists, use_container_width=True)

    with col2:
        # Tracks by Genre
        query_genre_distribution = """
        SELECT Genre.Name, COUNT(Track.TrackId) as TrackCount
        FROM Genre
        JOIN Track ON Genre.GenreId = Track.GenreId
        GROUP BY Genre.GenreId
        ORDER BY TrackCount DESC
        LIMIT 10
        """
        df_genre_distribution = pd.read_sql(query_genre_distribution, engine)
        fig_genre_distribution = px.pie(df_genre_distribution, values="TrackCount", names="Name", 
                                        title="Distribution of Tracks by Top 10 Genre")
        st.plotly_chart(fig_genre_distribution, use_container_width=True)

    # Sales Over Time
    query_sales_over_time = """
    SELECT strftime('%Y-%m', InvoiceDate) as Month, SUM(Total) as TotalSales
    FROM Invoice
    GROUP BY Month
    ORDER BY Month
    """
    df_sales_over_time = pd.read_sql(query_sales_over_time, engine)
    fig_sales_over_time = px.line(df_sales_over_time, x="Month", y="TotalSales", 
                                  title="Sales Over Time",
                                  labels={"Month": "Month", "TotalSales": "Total Sales ($)"},
                                  markers=True)
    st.plotly_chart(fig_sales_over_time, use_container_width=True)

    

if __name__ == "__main__":
    main()