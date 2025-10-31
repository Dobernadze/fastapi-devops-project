from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger
from sqlmodel import create_engine
# НОВЫЙ ИМПОРТ: Инструмент для Prometheus
from prometheus_fastapi_instrumentator import Instrumentator # 1. Импорт

# Настройка логгера для записи в файл
logger.add("logs/app.log", rotation="10 MB", compression="zip") 

class Settings(BaseSettings):
    secret_key: str = "default-secret-key"
    model_config = SettingsConfigDict() 
    db_url: str = "postgresql://devuser:devpassword@db/appdb"

settings = Settings()
app = FastAPI()

# 2. КРИТИЧЕСКИЙ ФИКС: Инициализация Instrumentator ДО @app.on_event("startup")
# Instrumentator добавляет Middleware, и это должно произойти до старта приложения.
Instrumentator().instrument(app).expose(app) 

@app.on_event("startup")
def on_startup():
    # 3. В on_startup оставляем только логику, не связанную с Middleware
    try:
        # Host: 'db' (имя сервиса в compose)
        engine = create_engine(settings.db_url) 
        with engine.connect(): # Пытаемся подключиться
             logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")

@app.get("/")
def read_root():
    # Добавляем запись в лог при каждом запросе
    logger.info("Handling root request: /") 
    return {"message": "Hello World from CI/CD v2", "secret_key_used": settings.secret_key}

@app.get("/secret")
def read_secret():
    logger.warning("Accessing protected endpoint: /secret")
    return {"app_secret_key": settings.secret_key}
