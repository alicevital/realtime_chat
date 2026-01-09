import asyncio
from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from services.routes.room_route import router as room_router
from services.routes.user_route import router as user_router
from services.websocket_manager import manager
import logging
from services.database import redis_client


app = FastAPI(tittle="Realtime Chat")

app.include_router(user_router)
app.include_router(room_router)

@app.on_event("startup")
async def startup():
    await redis_client.sadd("rooms", "global")
    asyncio.create_task(manager.start_redis())


@app.websocket("/ws/global")
async def chat_global(websocket: WebSocket, username: str):

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


