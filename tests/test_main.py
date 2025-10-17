# Импортируем специальный тестовый клиент для ASGI-приложений (FastAPI)
from fastapi.testclient import TestClient 
from main import app 

# Создаем тестовый клиент. 
# TestClient, в отличие от httpx.Client, ПРИНИМАЕТ аргумент app=app.
client = TestClient(app) 

def test_read_root():
    # Отправляем GET-запрос
    response = client.get("/")

    # Проверяем, что статус ответа 200 (ОК)
    assert response.status_code == 200

    # Проверяем содержимое ответа
    assert response.json() == {"message": "Hello World"}