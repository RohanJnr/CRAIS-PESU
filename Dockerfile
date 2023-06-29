# Stage 1: Build environment
FROM python:3.11-slim-buster AS build

# Install dependencies to system without creaeting venv.
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Install poetry.
RUN pip install poetry

# Install dependencies to system /usr/local/lib/python3.11/site-packages
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

# Install Node.js and NPM
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

COPY static/css/input.css ./

# Install Tailwind CSS and compile the styles
RUN npm install tailwindcss && \
    npx tailwindcss-cli@latest build -i input.css -o output.css

RUN python manage.py collectstatic

CMD ["bash"]

# Stage 2: Production environment
FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app
# /usr/local/lib/python3.11/site-packages
# Copy the compiled Tailwind CSS and Django project code from the build stage
COPY --from=build /app/static/src/output.css /app/static/src/output.css
COPY --from=build /app /app

# Install minimal dependencies for production
RUN pip install --no-cache-dir gunicorn

# Expose the necessary port
EXPOSE 8000

# Define the command to run the Django application
CMD ["gunicorn", "yourproject.wsgi:application", "--bind", "0.0.0.0:8000"]
