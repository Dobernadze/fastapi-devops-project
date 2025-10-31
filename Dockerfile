FROM python:3.11-alpine

# 2. Переменные окружения и рабочая директория
WORKDIR /app

# 3. Установка системных зависимостей
# Добавлены:
# - bash (для более удобной отладки)
# - netcat-openbsd (nc) для проверки портов
# - curl (для проверки метрик)
# - wget (для альтернативной проверки метрик)
RUN apk add --no-cache gcc musl-dev postgresql-dev bash netcat-openbsd curl wget

# 4. Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копирование кода приложения
COPY . .

# 6. Открытие порта
EXPOSE 8000

# 7. Запуск приложения (оставлена без изменений, так как она корректна)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]