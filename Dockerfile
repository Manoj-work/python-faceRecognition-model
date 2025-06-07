# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only app folder and requirements
COPY ./app /app/app
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
