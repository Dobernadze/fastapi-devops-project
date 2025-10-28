# Импортируем специальный тестовый клиент для ASGI-приложений (FastAPI)
from fastapi.testclient import TestClient 
from main import app 
# ИМПОРТИРУЕМ settings ИЗ main.py, где оно было создано!
from main import settings

# Создаем тестовый клиент. 
client = TestClient(app) 

def test_read_root():
    # Отправляем GET-запрос
    response = client.get("/")

    # Проверяем, что статус ответа 200 (ОК)
    assert response.status_code == 200

    # Проверяем содержимое ответа
    assert response.json() == {
        # Новое сообщение, которое мы ожидаем
        "message": "Hello World from CI/CD v2", 
        "secret_key_used": settings.secret_key
    }