FROM python:3.11-slim

COPY . .
RUN pip install poetry
RUN poetry install --with=prod

CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:8000", "--timeout", "300"]
