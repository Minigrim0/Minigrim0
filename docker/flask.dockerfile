FROM python:3.11-slim

COPY . .
RUN pip install poetry
RUN poetry install --with=prod
RUN mv static/ /static

CMD ["poetry", "run", "gunicorn", "app:create_app()", "--bind", "0.0.0.0:5000", "--timeout", "300"]
