from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger # <-- НОВЫЙ ИМПОРТ

# Настройка логгера для записи в файл
# Лог-файл будет создан в папке, из которой запускается Uvicorn (внутри контейнера)
logger.add("logs/app.log", rotation="10 MB", compression="zip") 

class Settings(BaseSettings):
    secret_key: str = "default-secret-key"
    model_config = SettingsConfigDict() 

settings = Settings()
app = FastAPI()

@app.get("/")
def read_root():
    # Добавляем запись в лог при каждом запросе
    logger.info("Handling root request: /") # <-- НОВАЯ СТРОКА
    return {"message": "Hello World", "secret_key_used": settings.secret_key}

@app.get("/secret")
def read_secret():
    logger.warning("Accessing protected endpoint: /secret") # <-- НОВАЯ СТРОКА
    return {"app_secret_key": settings.secret_key}