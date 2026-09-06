from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    ENV: str = "development"
    DB_PATH: str = "./data/edupulse.db"
    LOG_LEVEL: str = "INFO"

    # LLM model configuration
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    OPENROUTER_MODEL: str = "nvidia/nemotron-3.5-lightning:free"

    # RAG configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    FAISS_INDEX_DIR: str = "./data/faiss_index"

    # Cache configuration
    LRU_CACHE_CAPACITY: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
