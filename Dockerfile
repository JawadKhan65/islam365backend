# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code into the image
COPY . .

# Command to run the application
CMD ["python", "app.py"]
