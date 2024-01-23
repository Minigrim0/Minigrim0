ARG RUST_VERSION=1.70.0
ARG APP_NAME=minigrim0

FROM rust:${RUST_VERSION}-slim-bullseye AS build
ARG APP_NAME
WORKDIR /app

RUN apt update && apt install libssl-dev pkg-config -y

# Build the application.
# Leverage a cache mount to /usr/local/cargo/registry/
# for downloaded dependencies and a cache mount to /app/target/ for 
# compiled dependencies which will speed up subsequent builds.
# Leverage a bind mount to the src directory to avoid having to copy the
# source code into the container. Once built, copy the executable to an
# output directory before the cache mounted /app/target is unmounted.
RUN --mount=type=bind,source=tools/src,target=src \
    --mount=type=bind,source=tools/Cargo.toml,target=Cargo.toml \
    --mount=type=bind,source=tools/Cargo.lock,target=Cargo.lock \
    --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    <<EOF
set -e
cargo build --locked --release
cp ./target/release/$APP_NAME /bin/minigrim0
EOF

# pull official base image
FROM python:3.11-slim as final

WORKDIR /usr/src/app

RUN apt update && apt install libpq-dev gcc -y

COPY . .
RUN rm tools/ -r
RUN pip install --upgrade pip
RUN pip install poetry
COPY --from=build /bin/minigrim0 /bin/

# install project dependencies
# RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi