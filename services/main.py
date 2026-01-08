import asyncio
from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from services.routes.room_route import router as room_router
from services.routes.user_route import router as user_router
from services.websocket_manager import manager
import logging


app = FastAPI(tittle="Realtime Chat")

app.include_router(user_router)
app.include_router(room_router)

@app.on_event("startup")
async def startup():
    asyncio.create_task(manager.start_redis())

# endpoint criar user recebe "username, password, is_admin=True or False"
# endpoint de login (username e password) e atribue logged = True


# criar um endpoint que create-room no banco do redis
# só pode criar a sala se o user for admin = True e logged = True

@app.websocket("/ws/global")
async def chat_global(websocket: WebSocket, UserLogin):
    # aguardar o username para adicioanr uma melhor UX
    # verificar se username existe no redis
    # remover a criação do channel por força bruta
    channel = "chat:global"
    client_id = await manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            logging.warning(f"Mensagem recebida do client {client_id}: {data}")
            await manager.publish(f"Client {client_id}: {data}", channel)

            
    except WebSocketDisconnect:
        manager.disconnect(client_id, channel)
        await manager.publish(f"Client {client_id} saiu do chat.", channel)

    except Exception as e:
        logging.error(e)


@app.websocket("/ws/group/{room_name}")
# async def chat_private(websocket: WebSocket, PrivateChatDTO):
async def chat_room(websocket: WebSocket, channel, room_name):
    channel = f"chat:group:{room_name}"
    client_id = await manager.connect(websocket, channel)
    # adicionar o username e room_name no DTO
    # validar o room_name recebido do DTO, se existir no redis
    # verificar se username existe no redis

    try:
        while True:
            data = await websocket.receive_text()

            await manager.publish(f"Client {client_id}: {data}", channel)


    except WebSocketDisconnect:
        manager.disconnect(client_id, channel)


