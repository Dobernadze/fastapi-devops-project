from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Создаем класс для настроек
class Settings(BaseSettings):
    # !!! ОБЯЗАТЕЛЬНО: Объявляем поле с типом и значением по умолчанию !!!
    secret_key: str = "default-secret-key"

    # 2. Указываем Pydantic v2, как инициализировать настройки.
    #    Удаляем env_file='.env' - Pydantic теперь ищет SECRET_KEY только в 
    #    настоящих переменных окружения (которые передаст Docker или GitHub Actions).
    model_config = SettingsConfigDict() 

# Инициализируем настройки
settings = Settings()

app = FastAPI()

@app.get("/")
def read_root():
    # Возвращаем секретный ключ для проверки
    return {"message": "Hello World", "secret_key_used": settings.secret_key}

@app.get("/secret")
def read_secret():
    return {"app_secret_key": settings.secret_key}