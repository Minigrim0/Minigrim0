ARG RUST_VERSION=1.70.0
ARG APP_NAME=minigrim0

FROM rust:${RUST_VERSION}-slim-bullseye AS build
ARG APP_NAME
WORKDIR /app

RUN apt update && apt install libssl-dev pkg-config -y

RUN --mount=type=bind,source=tools/projects/src,target=src \
    --mount=type=bind,source=tools/projects/Cargo.toml,target=Cargo.toml \
    --mount=type=bind,source=tools/projects/Cargo.lock,target=Cargo.lock \
    --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    <<EOF
set -e
cargo build --locked --release
cp ./target/release/$APP_NAME /bin/minigrim0
EOF

# pull official base image
FROM python:3.11-slim AS final

WORKDIR /usr/src/app

RUN apt update && apt install libpq-dev gcc -y

COPY . .
RUN rm tools/ -r
RUN pip install --upgrade pip
RUN pip install poetry
COPY --from=build /bin/minigrim0 /bin/

# install project dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

CMD ["gunicorn", "minigrim0.wsgi", "--bind", "0.0.0.0:8000", "--timeout", "300"]
