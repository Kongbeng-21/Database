from flask import Flask, jsonify, request, render_template
from db import get_mysql_connection, get_mongo_collection, get_redis_client
import mysql.connector
import json
import time

app = Flask(__name__)

# Cache entries expire automatically after this many seconds (TTL)
CACHE_TTL = 300

# --- Frontend Route ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Health Check ---
@app.route('/health', methods=['GET'])
def health_check():
    status = {'mysql': 'down', 'mongo': 'down', 'redis': 'down'}

    try:
        conn = get_mysql_connection()
        if conn and conn.is_connected():
            status['mysql'] = 'up'
            conn.close()
    except Exception:
        pass

    try:
        products_col = get_mongo_collection()
        if products_col is not None:
            products_col.database.command('ping')
            status['mongo'] = 'up'
    except Exception:
        pass

    try:
        r = get_redis_client()
        if r.ping():
            status['redis'] = 'up'
    except Exception:
        pass

    return jsonify(status)


# ================= Product API (MongoDB + Redis) =================

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    if not data.get('_id') or not data.get('name'):
        return jsonify({"error": "Product _id and name are required"}), 400

    products_col = get_mongo_collection()
    if products_col is None:
        return jsonify({"error": "MongoDB connection failed"}), 500

    try:
        products_col.insert_one(data)

        # Activity 5 - Cache Invalidation (Delete-on-Write)
        # The cached 'product_list' no longer contains the new product -> delete it
        # so the next GET /products is a Cache Miss and reloads fresh data.
        r = get_redis_client()
        if r:
            r.delete('product_list')
            print(">>> [REDIS] Cache Invalidated: product_list deleted due to new product")

        return jsonify({"message": "Product created", "id": data['_id']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['GET'])
def list_products():
    # Activity 4 - Lazy Loading (Cache-Aside) for the product list
    r = get_redis_client()

    # 1. CHECK CACHE
    try:
        cached = r.get('product_list') if r else None
    except Exception as e:
        print(f">>> [REDIS] Unavailable, skipping cache: {e}")
        r, cached = None, None

    # 2. CACHE HIT -> return immediately
    if cached:
        print(">>> [REDIS] Cache Hit: product_list")
        return jsonify(json.loads(cached))

    # 3. CACHE MISS -> fetch from source of truth (MongoDB)
    print(">>> [MONGO] Cache Miss: Fetching product_list from MongoDB...")
    products_col = get_mongo_collection()
    if products_col is None:
        return jsonify({"error": "MongoDB connection failed"}), 500

    products = list(products_col.find())

    # 4. POPULATE CACHE (JSON string + TTL)
    if r:
        r.setex('product_list', CACHE_TTL, json.dumps(products, default=str))
        print(">>> [REDIS] Cache Populated: product_list")

    return jsonify(products)

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    # Activity 6 - Individual entity caching, key format: product:<id>
    redis_key = f"product:{product_id}"
    r = get_redis_client()

    try:
        cached = r.get(redis_key) if r else None
    except Exception:
        r, cached = None, None

    if cached:
        print(f">>> [REDIS] Cache Hit: {redis_key}")
        return jsonify(json.loads(cached))

    print(f">>> [MONGO] Cache Miss: Fetching {redis_key} from MongoDB...")
    products_col = get_mongo_collection()
    if products_col is None:
        return jsonify({"error": "MongoDB connection failed"}), 500

    product = products_col.find_one({"_id": product_id})
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if r:
        r.setex(redis_key, CACHE_TTL, json.dumps(product, default=str))
        print(f">>> [REDIS] Cache Populated: {redis_key}")

    return jsonify(product)


# ================= Cache Management =================

@app.route('/cache/remove', methods=['POST'])
def remove_cache():
    # Activity 7 - Bulk Cache Invalidation ("Nuke" button)
    # Deletes list caches + every individual entity cache so the next
    # requests become Cache Misses (useful for testing).
    r = get_redis_client()
    if not r:
        return jsonify({"error": "Redis connection failed"}), 500

    try:
        deleted = r.delete('product_list', 'user_list')   # list caches

        # scan_iter is non-blocking (unlike KEYS) -> safe on large datasets
        for pattern in ("product:*", "user:*"):
            for key in r.scan_iter(pattern):
                deleted += r.delete(key)

        print(f">>> [REDIS] Bulk Cache Invalidation: {deleted} keys deleted")
        return jsonify({"message": f"Cache cleared ({deleted} keys deleted)",
                        "deleted": deleted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cache/all', methods=['GET'])
def get_all_cache():
    r = get_redis_client()
    if not r:
        return jsonify({"error": "Redis connection failed"}), 500

    try:
        keys = r.keys("*")
        cache_data = {}
        for key in keys:
            if key == 'cache_last_refresh':
                continue
            val = r.get(key)
            try:
                cache_data[key] = json.loads(val)
            except:
                cache_data[key] = val
        return jsonify(cache_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cache/status', methods=['GET'])
def cache_status():
    r = get_redis_client()
    if not r:
        return jsonify({"error": "Redis connection failed"}), 500

    # Activity 8 - Count of keys currently stored in Redis
    try:
        total_keys = r.dbsize()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"total_cached_keys": total_keys})


# ================= Database Initialization =================

def init_mysql_db():
    conn = get_mysql_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                role ENUM('admin', 'user') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("MySQL 'users' table initialized.")


# ================= User API (MySQL + Redis) =================

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    role = data.get('role', 'user')

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    conn = get_mysql_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, role) VALUES (%s, %s, %s)",
            (username, email, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()

        # Activity 5 (Again) - Invalidate the stale 'user_list' cache
        r = get_redis_client()
        if r:
            r.delete('user_list')
            print(">>> [REDIS] Cache Invalidated: user_list deleted due to new user")

        return jsonify({"id": user_id, "message": "User created"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Activity 6 (Again) - Individual user caching, key format: user:<id>
    redis_key = f"user:{user_id}"
    r = get_redis_client()

    try:
        cached = r.get(redis_key) if r else None
    except Exception:
        r, cached = None, None

    if cached:
        print(f">>> [REDIS] Cache Hit: {redis_key}")
        return jsonify(json.loads(cached))

    print(f">>> [MYSQL] Cache Miss: Fetching {redis_key} from MySQL...")
    conn = get_mysql_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if r:
        # default=str converts the created_at datetime into a string
        r.setex(redis_key, CACHE_TTL, json.dumps(user, default=str))
        print(f">>> [REDIS] Cache Populated: {redis_key}")

    return jsonify(user)

@app.route('/users', methods=['GET'])
def list_users():
    # Activity 4 (Again) - Lazy Loading: Check Redis -> Miss -> MySQL -> Save to Redis
    r = get_redis_client()

    try:
        cached = r.get('user_list') if r else None
    except Exception:
        r, cached = None, None

    if cached:
        print(">>> [REDIS] Cache Hit: user_list")
        return jsonify(json.loads(cached))

    print(">>> [MYSQL] Cache Miss: Fetching user_list from MySQL...")
    conn = get_mysql_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    if r:
        # default=str is required: created_at is a datetime (not JSON serializable)
        r.setex('user_list', CACHE_TTL, json.dumps(users, default=str))
        print(">>> [REDIS] Cache Populated: user_list")

    return jsonify(users)


if __name__ == '__main__':
    try:
        init_mysql_db()
    except Exception as e:
        print(f"Warning: DB init failed: {e}")

    app.run(host='0.0.0.0', port=5001, debug=True)