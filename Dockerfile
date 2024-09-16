# Use the official Ubuntu as a base image
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.9.0
# Set the working directory in the container
WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip

RUN  rm /usr/lib/python3.12/EXTERNALLY-MANAGED

# # RUN apt-get install -y libgdal-dev

# # RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal

# # RUN export C_INCLUDE_PATH=/usr/include/gdal

# RUN pip install GDAL==3.4.1

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/planetcoveragefinder-main/

RUN pip install .

WORKDIR /app


RUN echo "{\"key\": \"${PL_API_KEY}\"}" > ~/.planet.json \
    && chmod 600 ~/.planet.json

RUN pip install click==8.0.4

# Expose the port that the application will listen on (not necessary for background tasks)
EXPOSE 8080

# Run the Python script
CMD ["python3", "main.py"]
