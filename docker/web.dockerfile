ARG APP_NAME=minigrim0

FROM rust:slim-bullseye AS build
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
cp /app/target/release/github-project-fetcher /bin/$APP_NAME
EOF

# Compile CSS
FROM alpine:latest AS css

WORKDIR /app

RUN apk add --no-cache npm \
    && npm install --global sass

WORKDIR /data

COPY ./tools/sass ./sass
RUN npx sass ./sass:./css

# Build final image
FROM python:3.11-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-luatex \
    lmodern \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock .
RUN pip install --upgrade pip \
 && pip install uv \
 && uv pip install --system --editable .

COPY . .

COPY --from=build /bin/minigrim0 /bin/
COPY --from=css /data/css ./minigrim0/assets/css

CMD ["uv", "run", "--extra", "prod", "gunicorn", "minigrim0.wsgi", "--bind", "0.0.0.0:8000", "--timeout", "300"]
