import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def set_cache(key, value):
    redis_client.set(key, value)


def get_cache(key):
    return redis_client.get(key)
