# 1. Базовый образ: Переходим на Alpine, он меньше и лучше для продакшена.
FROM python:3.11-alpine

# 2. Переменные окружения и рабочая директория
WORKDIR /app

# 3. Установка системных зависимостей для PostgreSQL.
# Используем 'apk add' вместо 'apt-get install'. 
# 'postgresql-dev' содержит необходимые файлы для компиляции psycopg2.
RUN apk add --no-cache gcc musl-dev postgresql-dev

# 4. Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копирование кода приложения
COPY . .

# 6. Открытие порта
EXPOSE 8000

# 7. Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
