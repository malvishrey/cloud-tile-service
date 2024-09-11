# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install Python and other required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Set the working directory in the container
WORKDIR /app

# Copy the local files to the container
COPY . /app

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Set environment variables (optional)
ENV PORT 8080

# Expose the port that the application will listen on (not necessary for background tasks)
EXPOSE 8080

# Run the Python script
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
