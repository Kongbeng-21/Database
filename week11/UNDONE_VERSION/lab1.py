import redis

# 1.8.1 Core Setup, Strings, Hashes, Sets

# 1. Connect (decode_responses=True returns str instead of bytes)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
print("Connected:", r.ping())  # True

# 2. Strings: Key-Value Storage & Atomic Counters
r.set("page:views", "100")
r.incr("page:views")  # Atomic increment -> 101
print(f"Page views: {r.get('page:views')}")

# 3. Hashes: Structured Object Fields (No JSON serialize overhead)
r.delete("user:101")
r.hset("user:101", mapping={"name": "Alice", "role": "admin"})
r.hincrby("user:101", "login_count", 1)  # Atomic field increment -> 1
print(f"User Object: {r.hgetall('user:101')}")

# 4. Sets: Unique Collections & Fast Intersections
r.sadd("user:101:skills", "Python", "SQL", "Redis")
r.sadd("user:102:skills", "Go", "Docker", "Redis")
print("Shared:", r.sinter("user:101:skills", "user:102:skills"))  # {'Redis'}
print("Has Python?", bool(r.sismember("user:101:skills", "Python")))  # True

# 1.8.2 Queues, Leaderboards, TTL

# 5. Lists: FIFO Producer-Consumer Task Queue
r.delete("task_queue")
r.lpush("task_queue", "send_welcome_email")
r.lpush("task_queue", "generate_pdf_report")
task = r.rpop("task_queue")  # Consumer pops the oldest task (FIFO)
print(f"Processed Task: {task}")  # 'send_welcome_email'

# 6. Sorted Sets (ZSet): Real-Time Gaming Leaderboard
r.delete("game:highscores")
r.zadd("game:highscores", {"Alice": 1450, "Bob": 2200, "Charlie": 1850})
r.zincrby("game:highscores", 500, "Alice")  # 1450 -> 1950

top_players = r.zrevrange("game:highscores", 0, 2, withscores=True)
print("Top Players:", [(p, int(s)) for p, s in top_players])

# 7. Automatic Expiration (TTL)
r.set("session:token_99", "user_auth_token", ex=30)  # Expires in 30 seconds
print(f"Remaining TTL: {r.ttl('session:token_99')} seconds")