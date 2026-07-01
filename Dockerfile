FROM python:3.12-slim

WORKDIR /code

# Install dependencies first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Directories for the SQLite db and downloaded images.
# Mounted as a volume in docker-compose so data survives container restarts.
RUN mkdir -p /code/app/data /code/app/images

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
