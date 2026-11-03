import redis, json, time

# 1.8.3 Practical Cache-Aside Caching

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Simulated primary database query (e.g., MySQL / MongoDB)
def query_primary_db(user_id):
    time.sleep(0.2)  # Simulated disk I/O latency
    return {"user_id": user_id, "name": "Piya", "role": "Instructor"}

# 1. READ: Cache-Aside (Lazy Loading)
def get_user_profile(user_id):
    cache_key = f"cache:user:{user_id}"
    cached = r.get(cache_key)
    if cached:
        print(f"[CACHE HIT] Retrieved '{cache_key}' from Redis (<1ms)")
        return json.loads(cached)
    print(f"[CACHE MISS] '{cache_key}' absent. Fetching from DB...")
    data = query_primary_db(user_id)
    r.setex(cache_key, 60, json.dumps(data))  # Store in Redis with 60s TTL
    return data

# 2. WRITE: Cache Invalidation (Delete-on-Write)
def update_user_profile(user_id, updated_fields):
    # primary_db.update(user_id, updated_fields)  # 1. Update primary DB
    r.delete(f"cache:user:{user_id}")              # 2. Evict stale cache key
    print(f"[CACHE INVALIDATED] Deleted cache:user:{user_id}")


# Demo: Miss -> Hit -> Invalidate -> Miss -> Hit
def timed_get(user_id):
    start = time.perf_counter()
    data = get_user_profile(user_id)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"    -> {data}  ({elapsed:.2f} ms)")

if __name__ == "__main__":
    r.delete("cache:user:1")  # start with an empty cache

    print("== Request 1 =="); timed_get(1)
    print("== Request 2 =="); timed_get(1)
    print(f"TTL of cache:user:1 = {r.ttl('cache:user:1')} s")

    print("== Update profile =="); update_user_profile(1, {"role": "Professor"})

    print("== Request 3 =="); timed_get(1)
    print("== Request 4 =="); timed_get(1)