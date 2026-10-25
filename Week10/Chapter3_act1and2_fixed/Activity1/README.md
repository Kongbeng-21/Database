# Activity 1: Student Management System (CLI)

This is a command-line interface (CLI) application for managing students using Python and MongoDB.

## Prerequisites

1.  **MongoDB**: Ensure MongoDB is running (e.g., via Docker).
    ```bash
    docker compose up -d
    ```
    *Connection string used:* `mongodb://root:examplepassword@localhost:27017/`

2.  **Python Dependencies**:
    ```bash
    pip install pymongo
    ```

## How to Run

1.  Navigate to the directory:
    ```bash
    cd Activity1
    ```
2.  Run the application:
    ```bash
    python main.py
    ```

## Features
- Add, View, Update, Delete Students.
- **Advanced Search**: Search with AND/OR conditions.
- **Clear All Data**: Quickly reset the database.
