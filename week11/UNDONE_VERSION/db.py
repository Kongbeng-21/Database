import os
import mysql.connector
from pymongo import MongoClient
import redis

def get_mysql_connection():
    # Activity 1 - Setup MySQL Connection (users data, ACID)
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'rootpassword'),
            database=os.getenv('MYSQL_DATABASE', 'user_db'),
            port=int(os.getenv('MYSQL_PORT', 3306))
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def get_mongo_collection():
    # Activity 2 - Setup MongoDB Connection (product catalog, flexible documents)
    try:
        uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/product_db')
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        # get_database() uses the DB name in the URI -> product_db
        return client.get_database()['products']
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_redis_client():
    # Activity 3 - Setup Redis Client (in-memory cache)
    # decode_responses=True -> values come back as str, not bytes
    try:
        return redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None