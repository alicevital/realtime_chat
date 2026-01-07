import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from services.schemas.room_schema import RoomRequest, RoomResponse
from services.schemas.user_schema import UserLogin, UserRequest, UserResponse
from services.websocket_manager import manager
from services.database import redis_client
import logging
from uuid import uuid4
from datetime import datetime


app = FastAPI()

@app.post("/user/register",response_model=UserResponse)
def create_user(user: UserRequest):
    user_key = f"user:{user.username}"

    is_admin = False
    if "admin@secret" in user.username:
        is_admin = True

    user_id = str(uuid4())
    date_created = datetime.utcnow()   

    redis_client.hset(user_key, mapping={
            "username": user.username,
            "name": user.name,
            "password": user.password,
            "is_admin": str(is_admin),
            "date_created": date_created.isoformat()
        }
    )
    
    return UserResponse(
        id=user_id,
        name=user.name,
        username=user.username,
        is_admin=is_admin,
        date_created=date_created
    )

@app.get("/user/list")
def get_user(user: UserResponse):
    # HGETALL usuario:1
    pass

@app.post("/user/login")
def login(self, user: UserLogin):
    pass

@app.post("/room/create")
def create_room(self, room: RoomRequest):
    pass

@app.get("/get/rooms")
def get_room(self, room: RoomResponse):
    pass

@app.on_event("startup")
async def startup():
    asyncio.create_task(manager.start_redis())

# endpoint criar user recebe "username, password, is_admin=True or False"
# endpoint de login (username e password) e atribue logged = True


# criar um endpoint que create-room no banco do redis
# só pode criar a sala se o user for admin = True e logged = True

@app.websocket("/ws/global")
async def chat_global(websocket: WebSocket, UserDTO):
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


