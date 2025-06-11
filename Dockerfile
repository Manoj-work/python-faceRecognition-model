# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including build tools and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY ./app /app/app
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create model directory and download the model
RUN mkdir -p /root/.insightface/models/buffalo_l && \
    wget https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip -O /tmp/buffalo_l.zip && \
    unzip /tmp/buffalo_l.zip -d /root/.insightface/models/buffalo_l && \
    rm /tmp/buffalo_l.zip

# Create images directory
RUN mkdir -p /app/images

# Expose port
EXPOSE 8090

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8090"]
