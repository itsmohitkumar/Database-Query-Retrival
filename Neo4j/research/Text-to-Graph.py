# Step 1: Install Required Packages
# Uncomment the lines below if you're running this code outside a notebook environment
# !pip install langchain langchain-community langchain-openai neo4j llama_index python-dotenv
# !pip install -qU langchain-groq

import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Access environment variables
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 2: Connect to Neo4j and Create a Graph Instance
# Create a Neo4jGraph instance
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    enhanced_schema=True,
)

# Step 3: Seed the Database with Initial Data
# Define and execute the Cypher query to populate the database
seed_query = """
MERGE (m:Movie {name:"Top Gun", runtime: 120})
WITH m
UNWIND ["Tom Cruise", "Val Kilmer", "Anthony Edwards", "Meg Ryan"] AS actor
MERGE (a:Actor {name:actor})
MERGE (a)-[:ACTED_IN]->(m)
"""

graph.query(seed_query)

# Refresh and print the graph schema
graph.refresh_schema()
print("Graph Schema:")
print(graph.schema)

# Step 4: Initialize the LLM and Graph Q&A Chain
# Define a custom prompt template
CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Examples: Here are a few examples of generated Cypher statements for particular questions:
# How many people played in Top Gun?
MATCH (m:Movie {{name:"Top Gun"}})<-[:ACTED_IN]-()
RETURN count(*) AS numberOfActors

The question is:
{question}"""

# Initialize the prompt template
CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

# Initialize the ChatGroq LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# Initialize the GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    cypher_prompt=CYPHER_GENERATION_PROMPT
)

# Step 5: Perform a Query Using the Chain
# Define and execute a natural language query
query = {"query": "Who played in Top Gun?"}
response = chain.invoke(query)

print(f"Query: {query['query']}")
print(f"Result: {response}")
