# Text-to-SQL Guide Using Olympic Medal Data from CSV

# Step 1: Install Required Libraries
# Uncomment the line below if you're running this code outside a notebook environment
# !pip install llama-index llama-index-llms-groq groq llama-index-embeddings-huggingface sqlalchemy pandas python-dotenv

import os
import pandas as pd
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    text
)

from dotenv import load_dotenv
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

import warnings
warnings.filterwarnings('ignore')

# Step 2: Load Data from CSV
csv_file_path = "/Users/taurangela/Desktop/Github/Database-Query-Retrival/data/olympics2024.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file_path)
print("DataFrame loaded successfully.")
print(df.head())

# Step 3: Create Database Schema
engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

table_name = "olympic_medals"
olympic_medals_table = Table(
    table_name,
    metadata_obj,
    Column("Rank", Integer),
    Column("Country", String(16)),
    Column("Country Code", String(3)),
    Column("Gold", Integer),
    Column("Silver", Integer),
    Column("Bronze", Integer),
    Column("Total", Integer),
)

# Drop the table if it exists
with engine.connect() as connection:
    connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))

# Create the table in the database
metadata_obj.create_all(engine)
print("Database schema created successfully.")

# Step 4: Insert Data into the Table
df.to_sql(table_name, con=engine, if_exists='append', index=False)
print("Data inserted into the table.")

# Step 5: Verify the Insertion
query = text(f"SELECT * FROM {table_name}")
with engine.connect() as connection:
    results = connection.execute(query).fetchall()
    print(f"Executed Query: {query}")
    for result in results:
        print(result)

# Step 6: Query the Table Using LLM
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("LLM and embedding model initialized.")

# Step 7: Perform a Natural Language Query
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name OLYMPIC_MEDALS and has the following columns - Rank, Country, Country Code, Gold, Silver, Bronze, Total

    For example,
    Example 1 - Which country won the most gold medals? 
    The SQL command will be something like this: 
    SELECT Country FROM OLYMPIC_MEDALS ORDER BY Gold DESC LIMIT 1;
    The result will be: United States
    
    Example 2 - Show the top 5 countries by total medals.
    The SQL command will be something like this: 
    SELECT Country FROM OLYMPIC_MEDALS ORDER BY Total DESC LIMIT 5;
    The result will be: United States, China, Russia, etc.
    
    Provide the SQL query and the result. The SQL code should not have ``` in the beginning or end, and the word SQL should not be included in the output.
    """
]

query_engine = NLSQLTableQueryEngine(
    sql_database=SQLDatabase(engine, include_tables=["olympic_medals"]), 
    tables=["olympic_medals"], 
    llm=llm, 
    embed_model=embed_model,
    prompt=prompt
)

query_str = "Which country won the most gold medals?"
response = query_engine.query(query_str)

# Step 8: Extract and Display Results
metadata = response.source_nodes[0].metadata
sql_query = metadata.get('sql_query', 'No SQL query found')
result = metadata.get('result', 'No result found')

print(f"Original Response: {response.response}")
print(f"SQL Query: {sql_query}")
print(f"Result: {result}")
