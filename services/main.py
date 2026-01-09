import asyncio
from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from services.routes.room_route import router as room_router
from services.routes.user_route import router as user_router
from services.utils.websocket_manager import manager
from services.utils.database import redis_client


app = FastAPI(tittle="Realtime Chat")
'''
    Instancia rotas com include_router
'''
app.include_router(user_router)
app.include_router(room_router)

@app.on_event("startup")
async def startup():
    '''
        Inicializa as ativadades do websocket e redis;
        Cria canal global quando iniciado.
    '''
    await redis_client.sadd("rooms", "global")
    asyncio.create_task(manager.start_redis())


@app.websocket("/ws/global")
async def chat_global(websocket: WebSocket, username: str):
    '''
        Endpoint de chat global, usuário é conectado via websocket e seu username;
        chave e valor são chat:global;
        websocket recebe mensagens e envia para users logados;
        mostra username de quem envia mensagem;
        usuário sai e é desconectado do canal.
    '''
    if not await redis_client.sismember("rooms", "global"):
        await websocket.close(code=1011)
        return
    
    channel = "chat:global"

    client_id = await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(f"{username}: {data}", channel)
    except WebSocketDisconnect:
        manager.disconnect(client_id, channel)


@app.websocket("/ws/group/{room_name}")
async def chat_room(websocket: WebSocket, room_name: str, username: str):
    '''
        Função de salas de chat, recebe nome de usuário e nome da sala;
        Verifica se nome da sala existe para user entrar;
        Nome da chave e valor são chat:group;
        websocket recebe mensagem e envia para usuários conectados na romm;
        user sai do canal e é desconectado.
    '''

    if not await redis_client.sismember("rooms", room_name):
        await websocket.close(code=1008)
        return
    
    channel = f"chat: group:{room_name}"
    client_id = await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(f"{username}: {data}", channel)
    except WebSocketDisconnect:
        manager.disconnect(client_id, channel)


