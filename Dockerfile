FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for psycopg2 and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only pyproject.toml and poetry.lock to cache the dependency layer
COPY pyproject.toml poetry.lock /app/

# Install Python dependencies using Poetry
RUN poetry install --no-root --no-dev

# Copy the rest of the project files into the container
COPY . /app/

# Copy the wait-for-it.sh script into the container
COPY wait-for-it.sh /app/

# Make the wait-for-it.sh file executable
RUN chmod +x /app/wait-for-it.sh

# Copy the entrypoint.sh script into the container
COPY entrypoint.sh /app/

# Make the entrypoint.sh file executable
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 to access the application
EXPOSE 8000

# Use the custom entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
