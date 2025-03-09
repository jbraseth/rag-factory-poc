#!/bin/bash
# setup_weaviate.sh - Script to set up a local Weaviate instance using Docker Compose

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install Git and try again."
    exit 1
fi

# Clone the Weaviate Quickstart repository if it does not exist
if [ ! -d "weaviate-quickstart" ]; then
    echo "Cloning the Weaviate Quickstart repository..."
    git clone https://github.com/semi-technologies/weaviate-quickstart.git
fi

cd weaviate-quickstart

# Start Weaviate using Docker Compose
echo "Starting Weaviate..."
docker-compose up -d

echo "Weaviate is now running on http://localhost:8080"
