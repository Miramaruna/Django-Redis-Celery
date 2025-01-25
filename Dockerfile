# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . /app/

# Открываем порт для Django
EXPOSE 8000

# Команда для запуска Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]