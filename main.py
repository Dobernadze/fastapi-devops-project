from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict # Важный импорт!

# 1. Создаем класс для настроек, наследуясь от BaseSettings
class Settings(BaseSettings):
    # 2. Имя переменной окружения: SECRET_KEY
    # 3. Значение по умолчанию: 'default-secret-key' (для локального dev)
    secret_key: str = "default-secret-key"

    # 4. Указываем Pydantic, что нужно искать переменные окружения
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

# Инициализируем настройки
settings = Settings()

app = FastAPI()

@app.get("/")
def read_root():
    # Возвращаем секретный ключ, чтобы увидеть, что он прочитан правильно
    return {"message": "Hello World", "secret_key_used": settings.secret_key}

# Добавляем новую конечную точку, которая должна быть защищена (почти)
@app.get("/secret")
def read_secret():
    return {"app_secret_key": settings.secret_key}