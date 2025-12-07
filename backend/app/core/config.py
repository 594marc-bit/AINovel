from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    # 大模型相关配置
    LLM_API_KEY: str
    LLM_BASE_URL: str = "https://api.openai.com/v1"  # 支持OpenAI兼容模式的API基础URL
    LLM_MODEL_NAME: str = "gpt-4"

    # Embedding模型相关配置
    EMBEDDING_API_KEY: str
    EMBEDDING_BASE_URL: str = "https://api.openai.com/v1"
    EMBEDDING_MODEL_NAME: str = "text-embedding-3-large"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()