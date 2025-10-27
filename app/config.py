from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_dsn: str = "postgresql://postgres:postgres@aiti_guru-postgres/postgres"
    migrations_path: str = "app/migrations"
    backend_port: int = 8080
    auto_reload: bool = True
    log_level: str = "info"
    enable_docs: bool = True


settings = Settings()
