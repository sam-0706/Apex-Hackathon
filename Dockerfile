# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install OS-level dependencies
RUN apt-get update && apt-get install -y git

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the desired port
EXPOSE 2781

# Start the FastAPI app on port 2781
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2781"]
