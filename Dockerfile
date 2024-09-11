# Use Ubuntu 22.04 as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local files to the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the application will listen on (not necessary for background tasks)
EXPOSE 8080

# Run the Python script
CMD ["python", "app.py"]
