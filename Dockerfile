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

EXPOSE 8000

CMD cd /app/backend/

CMD poetry run env GOOGLE_GENAI_USE_VERTEXAI=1 GOOGLE_CLOUD_PROJECT=vodaf-aida25lcpm-205 GOOGLE_CLOUD_LOCATION=europe-west1 adk web
