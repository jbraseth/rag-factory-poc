# Weaviate Local Setup Guide

This guide provides instructions to set up a locally hosted Weaviate instance using Docker Compose, following the official deployment patterns as described in the [Weaviate Local Quickstart Guide](https://weaviate.io/developers/weaviate/quickstart/local).

## Prerequisites

- **Docker**: Install from [Docker's official site](https://docs.docker.com/get-docker/).
- **Docker Compose**: Ensure Docker Compose is installed ([Installation Guide](https://docs.docker.com/compose/install/)).

## Setup Steps

### 1. Clone the Quickstart Repository

Clone the repository containing the Docker Compose configuration:

```
git clone https://github.com/semi-technologies/weaviate-quickstart.git
cd weaviate-quickstart
```

### 2. Start Weaviate with Docker Compose

Start the Weaviate instance locally:

```
docker-compose up -d
```

This command pulls the necessary images and runs Weaviate on port **8080**.

### 3. Verify the Deployment

Once the containers are running, you can verify your Weaviate instance by accessing:
- **Meta Endpoint**: [http://localhost:8080/v1/meta](http://localhost:8080/v1/meta)
- **GraphQL Playground**: [http://localhost:8080](http://localhost:8080)

### 4. Stop the Instance

When finished, shut down Weaviate with:

```
docker-compose down
```

## Additional Configuration

You can customize the `docker-compose.yml` file for additional environment variables, persistent data storage, or module configurations as needed.
