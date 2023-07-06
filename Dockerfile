# Stage 1: Build environment
FROM node:20 AS build

WORKDIR /app

COPY ./templates ./templates
COPY ./tailwind ./tailwind

# Install Tailwind CSS and compile the styles
RUN cd tailwind && \
    npm i && \
    npm run build:docker:css

# Stage 2: Production environment
FROM ghcr.io/owl-corp/python-poetry-base:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false

# Set working directory
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev


COPY . .
COPY --from=build /app/tailwind/output.css /app/static/css/output.css

RUN chmod +x entrypoint.sh
