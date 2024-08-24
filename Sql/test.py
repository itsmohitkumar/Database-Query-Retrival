import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph

# Load environment variables from the .env file
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

try:
    # Initialize the Neo4j driver with Aura URI
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        enhanced_schema=True,
    )

    # Test the connection
    graph.refresh_schema()
    print("Connection successful!")
    print("Graph schema:", graph.schema)

except Exception as e:
    print(f"Connection failed: {e}")
