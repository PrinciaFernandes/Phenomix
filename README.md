# PHENOMIX: Advanced Phenotype Search System

An advanced phenotype search system integrating graph databases (Neo4j) and vector embeddings (ChromaDB) with LLM-powered RAG chatbot for efficient biomedical data retrieval.

##  Project Overview

PHENOMIX is a comprehensive biomedical data retrieval system that combines the power of graph databases and vector embeddings to create an intelligent phenotype search platform. The system leverages web scraping, data processing, and machine learning to provide researchers with three specialized interfaces for phenotype discovery and analysis.

##  Three Specialized User Interfaces

### 1.  Phenomix Explorer
**Purpose**: Provide multi-faceted views of specific phenotype data

**Functionality**:
- **Phenotype Input**: Search for any phenotype (e.g., "AIDS", "Acne", "HIV")
- **Document View**: Display comprehensive, document-style JSON information about selected phenotypes
- **Table View**: Present phenotype data in structured, easy-to-read tabular format
- **Graph View**: Visualize relationships and connections within the knowledge graph, making complex interdependencies clear

### 2.  Phenomix Assistant
**Purpose**: Intelligent question-answering system for phenotype-related queries

**Functionality**:
- **Natural Language Queries**: Ask specific questions in plain English (e.g., "What is the definition of 'COPD'?", "How many phenotypes are in the 'PHEKB' database?")
- **AI-Powered Answers**: Provide concise and relevant answers based on the underlying knowledge base
- **Cypher Query Transparency**: Uniquely displays the generated Cypher query executed to retrieve answers, offering insights into backend logic
- **Technical Insights**: Bridge between user questions and database operations

### 3.  Phenomix ChatBot
**Purpose**: Conversational interface for general phenotype-related discussions

**Functionality**:
- **Conversational AI**: Engage users in fluid dialogue about various phenotype topics (e.g.,"Give a brief on Peanut Allergy?", "What are PID of Acne")
- **General Information Retrieval**: Ideal for quick summaries, definitions, or broad inquiries without needing underlying query language
- **Natural Interaction**: Seamless dialogue experience for exploratory research

##  System Architecture

### Data Pipeline Workflow

1. **Web Scraping**: Extracts phenotype data from 5 major biomedical databases
2. **Data Processing**: Converts raw data into structured JSON format with details and concepts
3. **Master List Creation**: Generates unique IDs for each phenotype
4. **Graph Database**: Stores relationships in Neo4j using masterlist, details, and concepts
5. **Vector Embeddings**: Creates ChromaDB embeddings using Gemini's embedding-001 model
6. **RAG Chatbot**: Provides intelligent phenotype search through natural language queries

### Data Sources

- **Sentinel**: Clinical phenotype definitions
- **HDR UK**: Health data research phenotypes
- **CPRD**: Clinical Practice Research Datalink phenotypes
- **PheKB**: Phenotype KnowledgeBase
- **OHDSI**: Observational Health Data Sciences phenotypes

##  Project Structure
```
PHENOMIX/
├── data/                               # Data storage
│   ├── Chatbot_vector_db/              # ChromaDB vector database
│   ├── masterlist/                     # Master phenotype lists
│   ├── processed/                      # Processed data files
│   └── raw/                            # Raw scraped data
├── src/                                # Source code
│   ├── config.py                       # Configuration settings
│   ├── logger.py                       # Logging utilities
│   ├── utils.py                        # Utility functions
│   ├── database/                       # Database connections
│   │   ├── load_vector_data.py
│   │   └── neo4j.py
│   ├── llm_model/                      # LLM integration
│   │   └── gemini_model.py
│   ├── masterlist/                     # Master list processing
│   │   └── masterlist.py
│   ├── prompts/                        # LLM prompts
│   │   └── Prompts.py
│   ├── pipeline/                       # Data pipelines
│   │   ├── sentinel_pipe.py            # Sentinel data pipeline
│   │   ├── hdruk_pipe.py               # HDR UK data pipeline
│   │   ├── cprd_pipe.py                # CPRD data pipeline
│   │   ├── phekb_pipe.py               # PheKB data pipeline
│   │   └── ohdsi_pipe.py               # OHDSI data pipeline
│   ├── processing/                     # Data processing modules
│   │   ├── sentinel_concept_detail.py
│   │   ├── hdruk_concept_detail.py
│   │   ├── cprd_concept_detail.py
│   │   ├── phekb_concept_detail.py
│   │   └── ohdsi_concept_detail.py
│   └── scraping/                       # Web scraping modules
│       ├── sentinel_webscrapping.py
│       ├── hdruk_webscrapping.py
│       ├── cprd_webscrapping.py
│       └── phekb_webscrapping.py
├── streamlit_file/                     # Web interface
│   ├── streamlit_app.py                # Main Streamlit application
│   ├── style.py                        # UI styling
│   └── views/                          # Application views
│       ├── chatbot.py                  # RAG chatbot interface
│       ├── dynamic.py                  # Dynamic search
│       ├── graph.py                    # Graph visualization
│       ├── phenosearch.py              # Phenotype search
│       └── table.py                    # Data tables
├── logs/                               # Application logs
├── notebooks/                          # Jupyter notebooks
├── main.py                             # Main execution script
└── requirements.txt                    # Python dependencies
```
##  Getting Started

### Prerequisites

- Python 3.8+
- Neo4j Database
- ChromaDB
- Google Gemini API access

### Installation

1. Clone the repository:
```bash
git clone [Phenomix](https://github.com/PrinciaFernandes/Phenomix)
cd PHENOMIX
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

4. Run the main pipeline:
```bash
python main.py
```

5. Launch the Streamlit interface:
```bash
streamlit run streamlit_file\streamlit_app.py 
```

##  Configuration

The system uses environment variables for configuration. Key settings include:

- Database connection strings (Neo4j, ChromaDB)
- API keys for LLM services
- Data directory paths
- Logging levels

##  Features

### Core Functionality

- **Multi-source Data Integration**: Aggregates phenotype data from 5 major repositories
- **Graph Database Storage**: Maintains complex relationships between phenotypes
- **Vector Search**: Semantic search capabilities using embeddings
- **Natural Language Interface**: Chat-based phenotype discovery
- **Interactive Visualizations**: Graph and table views of phenotype data

### Advanced Search Capabilities
- **Semantic Search**: Find phenotypes by meaning, not just keywords
- **Graph Traversal**: Explore relationships between phenotypes and concepts
- **Hybrid Queries**: Combine multiple search approaches for comprehensive results
- **Source Filtering**: Target specific databases or research contexts

### Interactive Visualizations
- **Knowledge Graph Views**: Visual representation of phenotype relationships
- **Data Tables**: Structured presentation of search results
- **Metadata Display**: Comprehensive phenotype information and provenance
- **Multi-View Exploration**: Document, table, and graph perspectives

### AI-Powered Assistance
- **Conversational Interface**: Natural language queries about phenotypes
- **Contextual Responses**: AI-generated answers backed by retrieved data
- **Query Transparency**: View underlying database queries and search logic
- **Real-time Processing**: Immediate responses to user queries

### User Experience Features
- **Three Specialized Interfaces**: Explorer, Assistant, and ChatBot for different use cases
- **Cypher Query Visualization**: Unique transparency into database operations
- **Responsive Design**: Optimized for researchers and clinicians
- **Progressive Disclosure**: Information depth based on user needs

##  Usage Guide

### Phenomix Explorer Usage
1. Enter a phenotype name in the search box
2. Choose your preferred view:
   - **Document View**: Comprehensive JSON-style information
   - **Table View**: Structured data presentation
   - **Graph View**: Visual relationship mapping
3. Explore interconnections and detailed metadata

### Phenomix Assistant Usage
1. Ask natural language questions about phenotypes
2. Receive AI-powered answers with source citations
3. View the generated Cypher query for transparency
4. Learn how your question was translated to database operations

### Phenomix ChatBot Usage
1. Engage in conversational queries about phenotypes
2. Request summaries, definitions, or general information
3. Explore topics through natural dialogue
4. Get quick answers without technical details

### Running the Complete Pipeline

```python
# Execute the full data processing pipeline
python main.py
```

### Using Individual Components

```python
from src.pipeline.hdruk_pipe import HDRUKPipeline

# Run individual pipeline
pipeline = HDRUKPipeline()
pipeline.main()
```

##  Development

### Adding New Data Sources

1. Create scraping module in `src/scraping/`
2. Implement processing logic in `src/processing/`
3. Add pipeline class in `src/pipeline/`
4. Update `main.py` to include new pipeline

### Extending the Interfaces

1. **Explorer Enhancements**: Modify views in the Streamlit pages
2. **Assistant Features**: Update query processing and Cypher generation
3. **ChatBot Improvements**: Enhance conversational AI capabilities
4. **Cross-Interface Features**: Add shared functionality across all three pages

##  Logging

The system provides comprehensive logging:

- Pipeline execution logs
- Error tracking and debugging
- Performance monitoring
- Data processing statistics

Logs are stored in the `logs/` directory with configurable levels.

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

##  License

This project is licensed under the terms specified in the MIT LICENSE file.

##  Related Technologies

- **Neo4j**: Graph database for relationship storage
- **ChromaDB**: Vector database for embeddings
- **Streamlit**: Web interface framework
- **Google Gemini**: LLM and embedding services
- **Trafilatura**: Web content extraction


*PHENOMIX: Advancing biomedical research through intelligent phenotype discovery*