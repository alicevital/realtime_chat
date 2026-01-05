import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from services.websocket_manager import manager

app = FastAPI()

@app.on_event("startup")
async def startup():
    asyncio.create_task(manager.start_redis())


@app.websocket("/ws/global")
async def chat_global(websocket: WebSocket):
    channel = "chat:global"
    client_id = await manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(channel, f"Client {client_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(channel, client_id)
        await manager.publish(f"Client {client_id} saiu do chat")


@app.websocket("/ws/group/{gropu_id}")
async def chat_group(websocket: WebSocket, group_id: str):
    channel = f"chat:group:{group_id}"
    client_id = await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(channel, f"{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(channel, client_id)


@app.websocket("/ws/private/{user_id}")
async def chat_private(websocket: WebSocket, user_id: str):
    channel = f"chat:private:{user_id}"
    client_id = await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(channel, f"{client_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(channel, client_id)


