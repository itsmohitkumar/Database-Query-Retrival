# Graph-Database-Query-Retrieval: Neo4j

## Overview

`Database-Query-Retrieval` is a Python package designed for advanced database query generation and retrieval using AI and open-source models. It integrates with Neo4j graph databases and utilizes cutting-edge AI models to convert natural language queries into executable database queries.

## Features

- **AI-Powered Query Generation**: Automatically generates Cypher queries for graph databases using advanced AI models.
- **Neo4j Integration**: Connects seamlessly with Neo4j graph databases.
- **Natural Language Querying**: Translates natural language queries into executable Cypher queries.
- **Simple Setup**: Easy configuration and integration with your project.

## Installation

To install `Database-Query-Retrieval`, use pip:

```bash
pip install Database-Query-Retrieval
```

## Usage

Here’s a basic example of how to use the package:

1. **Set Up Environment Variables**

   Create a `.env` file in your project directory with the following content:

   ```env
   NEO4J_URI=your_neo4j_uri
   NEO4J_USERNAME=your_neo4j_username
   NEO4J_PASSWORD=your_neo4j_password
   GROQ_API_KEY=your_groq_api_key
   ```

2. **Query the Database**

   Use the `QueryHandler` class to perform queries:

   ```python
   from database_query_retrieval import QueryHandler

   # Initialize the QueryHandler
   handler = QueryHandler()

   # Perform a query
   response = handler.query("Who played in Top Gun?")
   print(response)
   ```

## Configuration

The package uses environment variables for configuration. Ensure you have a `.env` file with the following variables:

- `NEO4J_URI`: The URI of your Neo4j database.
- `NEO4J_USERNAME`: The username for your Neo4j database.
- `NEO4J_PASSWORD`: The password for your Neo4j database.
- `GROQ_API_KEY`: Your API key for the Groq model.

## Development

To contribute to the development of `Database-Query-Retrieval`:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/itsmohitkumar/Database-Query-Retrieval.git
   cd Database-Query-Retrieval
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Tests**

   Run the test suite with pytest:

   ```bash
   pytest
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or issues, contact [Mohit Kumar](mailto:mohitpanghal12345@gmail.com).

## Acknowledgments

- [LangChain](https://github.com/langchain/langchain) for providing foundational AI models.
- [Neo4j](https://neo4j.com/) for the graph database.
- [Groq](https://www.groq.com/) for the advanced language model.
