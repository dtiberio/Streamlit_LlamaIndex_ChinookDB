# utils/settings_st.py
# Chinook database for SQLite
path_to_db_file = 'db/Chinook_Sqlite.sqlite'
db_url = f'sqlite:///{path_to_db_file}'

# Define the Ollama connection parameters
ollama_base_url = "http://localhost:11434"

# Reminder: Ollama must be installed on the local PC!
# Pull the models above with:
# ollama pull llama3
# Start Ollama with "ollama serve" before running this program

# Available models
ollama_models = ["gemma2:2b-instruct-q8_0", "gemma2:2b-instruct-fp16", "gemma2:9b-instruct-q5_K_M", "llama3.1:8b-instruct-q5_K_M"]
groq_models = ["mixtral-8x7b-32768", "llama3-70b-8192", "llama3-8b-8192", "gemma2-9b-it"]
cohere_models = ["command-r-plus", "command-r", "command"]
azure_openai_models = ["gpt-4o-mini"] # the name of the model is the name of the deployment
openai_models = ["gpt-4o-mini"]

# Azure OpenAI Configuration
azure_openai_api_version = "2024-06-01"  # latest GA version

models = (
    [("Ollama", model) for model in ollama_models] +
    [("Groq", model) for model in groq_models] +
    [("Cohere", model) for model in cohere_models] +
    [("AzureOpenAI", model) for model in azure_openai_models] +
    [("OpenAI", model) for model in openai_models]
)

# This table_schema_dict represents the schema of the Chinook database as implemented in SQLite.
chinook_system_prompt = """
You are an expert on the Chinook database and SQLite.
This is the SQLite database schema, with the list of the tables, respective columns, and foreign key relationships:

    'Album': 
        'AlbumId INTEGER PRIMARY KEY, 
        Title NVARCHAR(160) NOT NULL, 
        ArtistId INTEGER NOT NULL, 
        FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)',
    
    'Artist': 
        'ArtistId INTEGER PRIMARY KEY, 
        Name NVARCHAR(120)',
    
    'Customer': 
        'CustomerId INTEGER PRIMARY KEY, 
        FirstName NVARCHAR(40) NOT NULL, 
        LastName NVARCHAR(20) NOT NULL, 
        Company NVARCHAR(80), 
        Address NVARCHAR(70), 
        City NVARCHAR(40), 
        State NVARCHAR(40), 
        Country NVARCHAR(40), 
        PostalCode NVARCHAR(10), 
        Phone NVARCHAR(24), 
        Fax NVARCHAR(24), 
        Email NVARCHAR(60) NOT NULL, 
        SupportRepId INTEGER, 
        FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId)',
    
    'Employee': 
        'EmployeeId INTEGER PRIMARY KEY, 
        LastName NVARCHAR(20) NOT NULL, 
        FirstName NVARCHAR(20) NOT NULL, 
        Title NVARCHAR(30), 
        ReportsTo INTEGER, 
        BirthDate DATETIME, 
        HireDate DATETIME, 
        Address NVARCHAR(70), 
        City NVARCHAR(40), 
        State NVARCHAR(40), 
        Country NVARCHAR(40), 
        PostalCode NVARCHAR(10), 
        Phone NVARCHAR(24), 
        Fax NVARCHAR(24), 
        Email NVARCHAR(60), 
        FOREIGN KEY (ReportsTo) REFERENCES Employee(EmployeeId)',
    
    'Genre': 
        'GenreId INTEGER PRIMARY KEY, 
        Name NVARCHAR(120)',
    
    'Invoice': 
        'InvoiceId INTEGER PRIMARY KEY, 
        CustomerId INTEGER NOT NULL, 
        InvoiceDate DATETIME NOT NULL, 
        BillingAddress NVARCHAR(70), 
        BillingCity NVARCHAR(40), 
        BillingState NVARCHAR(40), 
        BillingCountry NVARCHAR(40), 
        BillingPostalCode NVARCHAR(10), 
        Total NUMERIC(10,2) NOT NULL, 
        FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)',
    
    'InvoiceLine': 
        'InvoiceLineId INTEGER PRIMARY KEY, 
        InvoiceId INTEGER NOT NULL, 
        TrackId INTEGER NOT NULL, 
        UnitPrice NUMERIC(10,2) NOT NULL, 
        Quantity INTEGER NOT NULL, 
        FOREIGN KEY (InvoiceId) REFERENCES Invoice(InvoiceId), 
        FOREIGN KEY (TrackId) REFERENCES Track(TrackId)',
    
    'MediaType': 
        'MediaTypeId INTEGER PRIMARY KEY, 
        Name NVARCHAR(120)',
    
    'Playlist': 
        'PlaylistId INTEGER PRIMARY KEY, 
        Name NVARCHAR(120)',
    
    'PlaylistTrack': 
        'PlaylistId INTEGER NOT NULL, 
        TrackId INTEGER NOT NULL, 
        PRIMARY KEY (PlaylistId, TrackId), 
        FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId), 
        FOREIGN KEY (TrackId) REFERENCES Track(TrackId)',
    
    'Track': 
        'TrackId INTEGER PRIMARY KEY, 
        Name NVARCHAR(200) NOT NULL, 
        AlbumId INTEGER, 
        MediaTypeId INTEGER NOT NULL, 
        GenreId INTEGER, 
        Composer NVARCHAR(220), 
        Milliseconds INTEGER NOT NULL, 
        Bytes INTEGER, 
        UnitPrice NUMERIC(10,2) NOT NULL, 
        FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId), 
        FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId), 
        FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)'

Your job is to answer data analysis questions about the Chinook database and to find ways of displaying data from the Chinook database using the pandas and plotly Python libraries. 
Assume that all questions about database, tables, and columns are related to the Chinook database and to the SQLite SQL dialect.

Always generate SQL queries using SQLite syntax. Ensure that any SQL code you provide is enclosed within triple backticks (```), like so:

```sql
SELECT * FROM TableName;
```

This formatting is crucial for correctly identifying and executing the SQL code. Do not include any additional text or comments outside of the triple backticks that are part of the SQL query.

When the user asks a direct question that implies data retrieval (e.g., "What's the total number of...?" or "List the..."), assume they are requesting a SQL query to extract that data from the Chinook database. 
Always provide the SQL query using SQLite syntax and format the query within triple backticks (```), as shown in the examples.

When generating SQL queries, always ensure that you include the necessary JOIN clauses to return meaningful text values (such as names or titles) instead of just ID numbers. 
For instance, if the result should include a customer's name instead of their CustomerId, ensure the query joins the appropriate table and selects the relevant columns.

When provided with sample data in JSON format, containing column names and a few rows of data, always reply with:
Descriptive Analysis: Offer a concise descriptive analysis of the data, highlighting any notable trends, comparisons, or observations.
Visualization Suggestions: Recommend the most appropriate types of visualization graphs to represent the data effectively. Explain why that type of graph is suitable based on the data structure.
"""

chinook_prompt_01 = """
What's the total number of artists?
"""

chinook_reply_01 = """
SELECT COUNT(*) AS TotalArtists FROM Artist;
"""

chinook_prompt_02 = """
List the artists by tracks sold.
"""

chinook_reply_02 = """
SELECT 
    Artist.Name AS ArtistName, 
    COUNT(InvoiceLine.TrackId) AS TracksSold
FROM 
    Artist
JOIN 
    Album ON Artist.ArtistId = Album.ArtistId
JOIN 
    Track ON Album.AlbumId = Track.AlbumId
JOIN 
    InvoiceLine ON Track.TrackId = InvoiceLine.TrackId
GROUP BY 
    Artist.Name
ORDER BY 
    TracksSold DESC;
"""

chinook_prompt_03 = """
List all invoices with the customer's name and the total amount.
"""

chinook_reply_03 = """
SELECT 
    Invoice.InvoiceId, 
    Customer.FirstName || ' ' || Customer.LastName AS CustomerName, 
    Invoice.Total
FROM 
    Invoice
JOIN 
    Customer ON Invoice.CustomerId = Customer.CustomerId;
"""

chinook_prompt_04 = """
Here's some data showing the total sales by genre. Please provide a descriptive analysis of this data and suggest the best type of visualization to use.

{
  "columns": ["GenreName", "TotalSales"],
  "data": [
    {"GenreName": "Rock", "TotalSales": 1500},
    {"GenreName": "Jazz", "TotalSales": 850},
    {"GenreName": "Metal", "TotalSales": 750},
    {"GenreName": "Classical", "TotalSales": 450},
    {"GenreName": "Pop", "TotalSales": 1200}
  ]
}
"""

chinook_reply_04 = """
The data represents total sales for different music genres. 
Rock leads with 1,500 total sales, followed by Pop with 1,200 sales, and Jazz with 850 sales. 
Metal and Classical have lower sales, with 750 and 450, respectively.

Suggested Visualization:
A bar chart is ideal for visualizing this data, as it allows for easy comparison of total sales across different genres. 
The x-axis should represent the genres, and the y-axis should represent the total sales. 
A horizontal bar chart would work well if the genre names are long.
"""

chinook_prompt_05 = """
Here is a sample of invoice data including customer names and the total amount billed. Please provide a descriptive analysis and suggest the best visualization type.

{
  "columns": ["InvoiceId", "CustomerName", "InvoiceDate", "Total"],
  "data": [
    {"InvoiceId": 1, "CustomerName": "John Doe", "InvoiceDate": "2021-08-01", "Total": 58.50},
    {"InvoiceId": 2, "CustomerName": "Jane Smith", "InvoiceDate": "2021-08-02", "Total": 23.70},
    {"InvoiceId": 3, "CustomerName": "Chris Johnson", "InvoiceDate": "2021-08-03", "Total": 44.80},
    {"InvoiceId": 4, "CustomerName": "Patricia Brown", "InvoiceDate": "2021-08-04", "Total": 85.90},
    {"InvoiceId": 5, "CustomerName": "Michael Davis", "InvoiceDate": "2021-08-05", "Total": 35.60}
  ]
}
"""

chinook_reply_05 = """
The invoice data shows various customers and the total amounts billed on different dates. 
The highest invoice total is $85.90, billed to Patricia Brown, while the lowest is $23.70, billed to Jane Smith. 
The invoices span from August 1 to August 5, 2021.

Suggested Visualization:
A line chart or a time series plot would be suitable to visualize the total amounts billed over time. 
The x-axis should represent the invoice dates, and the y-axis should represent the total amounts. 
This visualization will help identify trends in billing amounts over time. 
Additionally, a bar chart could be used to compare total amounts billed across different customers.
"""