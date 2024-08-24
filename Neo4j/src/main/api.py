from fastapi import APIRouter, HTTPException
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
from config.config import Config
from config.logger import setup_logger

router = APIRouter()
logger = setup_logger()

# Initialize Neo4jGraph
graph = Neo4jGraph(
    url=Config.NEO4J_URI,
    username=Config.NEO4J_USERNAME,
    password=Config.NEO4J_PASSWORD,
    enhanced_schema=True,
)

# Seed the Database with Initial Data
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
logger.info("Graph Schema:")
logger.info(graph.schema)

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

@router.get("/query")
async def query_graph(query: str):
    try:
        response = chain.invoke({"query": query})
        return {"query": query, "result": response}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")
