FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8003

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]