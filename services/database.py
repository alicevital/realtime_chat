'''
Docstring for services.database
'''
import os
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

async def test_connect():
    try:
        pong = await redis_client.ping()
        print("Conectado: ", pong)
    except Exception as e:
        print("Falha ao conectar com Redis: ", e)
        raise