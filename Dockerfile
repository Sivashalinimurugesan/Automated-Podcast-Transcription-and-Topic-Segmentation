# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files to disc
# and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# ffmpeg is required for audio processing (librosa, pydub)
# git is often required for installing python packages from git repositories
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make sure the data directories exist
RUN mkdir -p data/final_output data/temp_processing logs

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define environment variables for the app to use
# These override the hardcoded Windows paths in the code
ENV BASE_DIR=/app
ENV DATA_DIR=/app/data/final_output
ENV TEMP_DIR=/app/data/temp_processing
# You should mount a volume for AUDIO_DIR at runtime, e.g., -v /host/audio:/app/audio
ENV AUDIO_DIR=/app/audio

# Run the application using gunicorn
# Adjust the worker count and timeout based on your needs
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "src.web_app.app:app"]
