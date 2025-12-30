APP_NAME="mini-RAG"
APP_VERSION="0.1"
OPENAI_API_KEY=""

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000 # 512KB

# ========================= DAtabase Config =========================
POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = ""
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_MAIN_DATABASE = "minirag"

# ========================= LLM Config =========================
GENERATION_BACKEND = "OPENAI"
EMBEDDING_BACKEND = "COHERE"

OPENAI_API_KEY=""
OPENAI_API_URL="http://localhost:11434/v1"
COHERE_API_KEY=""

GENERATION_MODEL_ID_LITERAL = ["gpt-oss:120b-cloud","gpt-oss:20b-cloud"]
GENERATION_MODEL_ID="gpt-oss:120b-cloud"
EMBEDDING_MODEL_ID="embed-multilingual-v3.0"
EMBEDDING_MODEL_SIZE=1024

INPUT_DAFAULT_MAX_CHARACTERS=1024
GENERATION_DAFAULT_MAX_TOKENS=200
GENERATION_DAFAULT_TEMPERATURE=0.1

# ========================= VectorDB Config ========================
VECTOR_DB_BACKEND_LITERAL = ["QUDRANT","PGVECTOR"]
VECTOR_DB_BACKEND = "QUDRANT"
VECTOR_DB_PATH = "qudrant_db"
VECTOR_DB_DISTANCE_METHOD = "cosine"
VECTOR_DB_PGVEC_INDEX_THRESHOLD = 300

# ========================= Template Config ========================
PRIMARY_LANG = "en"
DEFAULT_LANG = "en"