# EVOLVED RAG

A production-ready, scalable, and modular Retrieval-Augmented Generation (RAG) system built with FastAPI. This project provides a robust foundation for building question-answering applications with support for multiple LLM providers, efficient vector search, and comprehensive system monitoring.
This project is the extended Version of EVOLVED RAG Project, whit Extra Features.

> [!NOTE]
> **Acknowledgements**: This project is based on the **EVOLVED RAG tutorial on YouTube**. A special thanks to **Eng. Abo Bakr Soliman** for the comprehensive guide and architectural insights.

## 🚀 Features

- **Multi-LLM Support**: Seamlessly switch between **Google Gemini**, **OpenAI**, and **Cohere** for both text generation and embedding models.
- **Document Processing**: Robust support for parsing and chunking **PDF** and **Text** files.
- **Vector Database**: Integrated with **Qdrant** for high-performance vector similarity search (with support for **Pgvector**).
- **Production-Ready Monitoring**: Full observability stack included:
  - **Prometheus**: Metric collection for system performance and application Latency.
  - **Grafana**: Pre-configured dashboards for visualizing system health, request rates, and LLM performance.
  - **Node/Postgres Exporters**: Detailed hardware and database metrics.
- **Containerized**: Fully Dockerized application for consistent deployment environments.
- **RESTful API**: Clean and documented API endpoints built with FastAPI.

## 📂 Project Structure

The project follows a clean, modular architecture:

```text
EVOLVED RAG/
├── docker/             # Docker configuration and environment variables
├── src/
│   ├── controllers/    # Business logic and request handlers
│   ├── models/         # Pydantic models and Database schemas
│   ├── routes/         # API endpoint definitions
│   ├── stores/         # Data access layer (Vector DB, Document interactions)
│   ├── utils/          # Utility functions and helpers
│   └── main.py         # Application entry point
├── tests/              # Test suite
├── .env.example        # Example environment variables
├── pyproject.toml      # Python dependencies and project config
└── README.md           # Project documentation
```

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, LangChain
- **Vector Database**: Qdrant, Pgvector
- **NoSQL Database**: MongoDB (via Motor)
- **Relational Database**: PostgreSQL
- **LLM Integration**:
  - Google Generative AI (Gemini)
  - OpenAI
  - Cohere
- **Infrastructure**: Docker, Docker Compose
- **Monitoring**: Prometheus, Grafana, Node Exporter

## 📋 Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.10+ (for local development)

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/bakrianoo/EVOLVED RAG.git
cd EVOLVED RAG
```

### 2. Configure Environment Variables
Copy the example environment file and configure your API keys.

```bash
cd docker
cp env/.env.app.example env/.env.app
# also configure other env files if needed (postgres, grafana)
```

Edit `env/.env.app` to set your preferences. **Crucially**, add your API keys:

```ini
# Choose your backend (GEMINI, OPENAI, COHERE)
GENERATION_BACKEND="GEMINI"
EMBEDDING_BACKEND="COHERE"

# API Keys
GEMINI_API_KEY="your_gemini_key_here"
OPENAI_API_KEY="your_openai_key_here"
COHERE_API_KEY="your_cohere_key_here"

# Model Selection
GENERATION_MODEL_ID="gemini-1.5-flash"
EMBEDDING_MODEL_ID="embed-multilingual-v3.0"
```

### 3. Run with Docker Compose
Start the entire stack (App, DBs, Monitoring) with a single command:

```bash
sudo docker compose up -d --build
```

The services will be available at:
- **API (FastAPI)**: `http://localhost:8000` (Docs at `/docs`)
- **Grafana**: `http://localhost:3000`
- **Prometheus**: `http://localhost:9090`
- **Qdrant UI**: `http://localhost:6333/dashboard`

## 🔌 API Usage

You can explore the interactive API documentation at `http://localhost:8000/docs`.

### Common Workflows

1.  **Upload Documents**:
    ```http
    POST /data/upload/{project_id}
    Content-Type: multipart/form-data
    file=@/path/to/your/document.pdf
    ```

2.  **Process Documents (Chunking & Embedding)**:
    ```http
    POST /data/process/{project_id}
    ```

3.  **Ask a Question**:
    ```http
    POST /nlp/answer/{project_id}
    Content-Type: application/json

    {
      "question": "What does the document say about feature X?"
    }
    ```

## 📊 Monitoring

The system comes with a pre-configured monitoring stack.
- Access **Grafana** at `http://localhost:3000`.
- Login with default credentials (check `docker/env/.env.grafana` or default `admin`/`admin`).
- View dashboards for API latency, Request counts, and System resource usage.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
