#!/bin/bash

# Configuration
IMAGE_NAME="devotion-tts-spark-gptsovits"
DOCKERFILE="docker/Dockerfile.spark.gptsovits"
CONTAINER_NAME="devotion_tts_spark_gptsovits"

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME..."
docker build -t $IMAGE_NAME -f $DOCKERFILE .

if [ $? -ne 0 ]; then
    echo "Error: Docker build failed."
    exit 1
fi

echo "Docker image built successfully."

# Run the container
# We mount the current directory to /workspace/github/devotion_tts
echo "Running container: $CONTAINER_NAME..."
docker run --gpus all -it --rm \
    --name $CONTAINER_NAME \
    --shm-size=8g \
    -v $(pwd):/workspace/github/devotion_tts \
    -w /workspace/github/devotion_tts \
    $IMAGE_NAME
