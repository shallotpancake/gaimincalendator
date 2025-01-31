#!/bin/bash

IMAGE_NAME="gaimin-calendator"

echo "Building the container image..."
podman build -t $IMAGE_NAME -f Containerfile

# Check if the build was successful
if [ $? -ne 0 ]; then
  echo "Failed to build the container image."
  exit 1
fi

# Run the container
echo "Running the container..."
podman run \
  -v $(pwd)/.env:/.env \
  -v $(pwd)/temp/:/temp/ \
  --rm -it $IMAGE_NAME