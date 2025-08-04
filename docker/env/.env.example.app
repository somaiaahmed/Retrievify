APP_NAME="mini_RAG"
APP_VERSION="0.1.0"
OPENAI_API_KEY=""

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10

FILE_DEFAULT_CHUNK_SIZE=512000 # 512 KB

POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_HOST="pgvector"
POSTGRES_PORT=5432
POSTGRES_MAIN_DATABASE="minirag"

#================================================= LLM Config=================================================
GENERATION_BACKEND="COHERE"  # Options: "openai", "cohere", "ollama"
EMBEDDING_BACKEND="COHERE"  # Options: "openai", "cohere", "ollama"

OPENAI_API_KEY=
OPENAI_API_URL=
COHERE_API_KEY=

GENERATION_MODEL_ID_LITERAL=["command-r-plus", "gpt-3.5-turbo-0125"]
GENERATION_MODEL_ID="command-r-plus" # command-r-plus, gpt-3.5-turbo-0125
EMBEDDING_MODEL_ID="embed-multilingual-v3.0"
EMBEDDING_MODEL_SIZE=1024

INPUT_DEFAULT_MAX_CHARACTERS=1024
GENERATION_DEFAULT_MAX_TOKENS=200
GENERATION_DEFAULT_TEMPERATURE=0.1

#================================================= VectorDB Config =================================================
VECTOR_DB_BACKEND_LITERAL=["QDRANT", "PGVECTOR"]  
VECTOR_DB_BACKEND="PGVECTOR"  
VECTOR_DB_PATH="qdrant_db"
VECTOR_DB_DISTANCE_METHOD="Cosine"  # Options: "cosine", "dot", "euclidean
VECTOR_DB_PGVEV_INDEX_THRESHOLD = 300

#================================================= Templates Config =================================================
PRIMARY_LANG="ar"
DEFAULT_LANG="en" 
