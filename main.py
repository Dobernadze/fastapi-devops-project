from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger # <-- НОВЫЙ ИМПОРТ
from sqlmodel import create_engine

# Настройка логгера для записи в файл
# Лог-файл будет создан в папке, из которой запускается Uvicorn (внутри контейнера)
logger.add("logs/app.log", rotation="10 MB", compression="zip") 

class Settings(BaseSettings):
    secret_key: str = "default-secret-key"
    model_config = SettingsConfigDict() 
    db_url: str = "postgresql://devuser:devpassword@db/appdb"

settings = Settings()
app = FastAPI()

@app.on_event("startup")
def on_startup():
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
    logger.info("Handling root request: /") # <-- НОВАЯ СТРОКА
    return {"message": "Hello World", "secret_key_used": settings.secret_key}

@app.get("/secret")
def read_secret():
    logger.warning("Accessing protected endpoint: /secret") # <-- НОВАЯ СТРОКА
    return {"app_secret_key": settings.secret_key}