from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    database_url: str = ""
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:8501"
    model_path: str = "./ml/model.pkl"
    integrity_model_path: str = "./ml/integrity_model.pkl"

    class Config:
        env_file = ".env"


settings = Settings()
