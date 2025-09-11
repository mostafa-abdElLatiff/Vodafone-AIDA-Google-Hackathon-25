FROM python:3.10-slim

WORKDIR /app

COPY configs/__init__.py /app/configs/__init__.py
COPY backend/__init__.py /app/backend/__init__.py
COPY frontend/__init__.py /app/frontend/__init__.py

COPY pyproject.toml /app/

RUN pip install poetry==2.1.4

RUN poetry lock

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN poetry install --no-root --without dev

COPY . .

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
