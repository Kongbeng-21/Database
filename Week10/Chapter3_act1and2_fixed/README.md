# MongoDB Docker Setup

## Prerequisites
- Docker and Docker Compose installed.

## Usage

1.  **Start the container:**
    ```bash
    docker compose up -d
    ```

2.  **Stop the container:**
    ```bash
    docker compose down
    ```

## Configuration
- **Port:** 27017
- **Username:** root
- **Password:** examplepassword
- **Volume:** `mongo-data` (persists data)

## Connecting
You can connect using a connection string like:
`mongodb://root:examplepassword@localhost:27017/`
