import os
import redis.asyncio as redis


'''
    Host, Porta e nome do database redis
'''
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

'''
    redis_client recebe a classe do Redis e as variáveis de ambiente anteriores
'''
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

async def test_connect():
    '''
        Teste de conexão do redis;
        Entre no terminal com redis-cli;
        Escreva ping;
        Se estiver conectado, retornará "PONG"
        Se não, retornará a mensagem de erro.
    '''
    try:
        pong = await redis_client.ping()
        print("Conectado: ", pong)
    except Exception as e:
        print("Falha ao conectar com Redis: ", e)
        raise