# Base image
FROM python:3.7-slim

# Set working directory and copy files
WORKDIR /app
COPY . /app


# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --requirement requirements.txt


# Tell Docker about the port `serve` will expose on
EXPOSE 8080

# Start server
ENTRYPOINT ["./scripts/start_gunicorn.sh"]
