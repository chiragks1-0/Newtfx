# Use a Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/pipeline

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install TFX and additional Python dependencies
RUN pip install --no-cache-dir \
    tensorflow==2.12.0 \
    apache-beam[gcp]==2.48.0 \
    tfx==1.15.1 \
    pandas \
    matplotlib \
    scikit-learn

# Set the working directory
WORKDIR $WORKDIR

# Copy pipeline code and data into the container
COPY . $WORKDIR

# Default command to run
CMD ["python", "run_pipeline.py"]
