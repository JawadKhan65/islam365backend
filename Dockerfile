# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential gcc

# Copy the requirements file into the image
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the image
COPY . .

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
