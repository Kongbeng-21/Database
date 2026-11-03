# Student Activity: Multi-Database Web Application with Redis Caching

This project demonstrates a microservices-style architecture using Flask, MySQL, MongoDB, and Redis. It is designed to teach the **Lazy Loading** pattern and how to manage multiple data sources in a single application.

## Prerequisites
- Docker and Docker Compose (to run the database services)
- Python 3.9+
- pip (Python Package Manager)

## Setup & Run

### 1. Start Support Services (Databases)
Start MySQL, MongoDB, and Redis using Docker. **Make sure you are freeing these ports (3306, 27017, 6379) before running the docker container.**
```bash
docker-compose up -d
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Implementation Tasks
The activity consists of the following tasks:
- **`db.py`**: Implement connection factory functions (Activities 1, 2, and 3).
- **`app.py`**: Implement Caching and Lazy Loading logic (Activities 4 through 8).

### 4. Run the Application
Start the Flask application locally:
```bash
python app.py
```

### 5. Access the Web Interface
Open [http://localhost:5001](http://localhost:5001) in your browser.

## Educational Focus: Redis Caching

This project helps you understand the **Lazy Loading (Cache-Aside)** pattern.

### 1. Lazy Loading (Cache-Aside) Pattern
0. Study the **Cache-Aside Pattern** from the following resources:
   - [GeeksforGeeks: Cache-Aside Pattern](https://www.geeksforgeeks.org/system-design-cache-aside-pattern/)
   - [AWS: Database Caching Strategies Using Redis](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
   - [Microsoft Azure: Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
1.  **Check Redis**: The app first checks if the data is already in Redis.
    -   **Cache Hit**: Data is found! It's returned instantly to the user.
    -   **Cache Miss**: Data is NOT found. The app must fetch it from the primary database (MySQL or MongoDB).
2.  **Populate Cache**: After a "Cache Miss", the app saves the fetched data into Redis so the next request will be a "Cache Hit".

### 2. Cache Invalidation
When you **add** a new user or product, the existing list in Redis becomes outdated. You must **Invalidate** (delete) the cached list so the next retrieval fetches fresh data.

### 3. How to Observe
Watch your terminal logs:
- `>>> [MONGO] Cache Miss`: Reaching out to the database.
- `>>> [REDIS] Cache Populated`: Saving data for next time.
- `>>> [REDIS] Cache Hit`: Loaded instantly from memory!
- `>>> [REDIS] Cache Invalidated`: Occurs right after you "Create" an item.

## Architecture & Ports
- **MySQL**: Local Port 3306 (User data)
- **MongoDB**: Local Port 27017 (Product data)
- **Redis**: Local Port 6379 (Caching)
- **Flask**: Local Port 5001 (Web App). **Note: We use port 5001 instead of default (Flask port 5000), since macOS already occupies 5000.**
