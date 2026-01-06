import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from services.websocket_manager import manager
import logging


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
            logging.warning(f"Mensagem recebida do client {client_id}: {data}")
            await manager.publish(f"Client {client_id}: {data}", channel)

            
    except WebSocketDisconnect:
        manager.disconnect(client_id, channel)
        await manager.publish(f"Client {client_id} saiu do chat")

    except Exception as e:
        logging.error(e)

@app.websocket("/ws/group")
async def chat_group(websocket: WebSocket):
    group_id = websocket.query_params.get("group_id")
    channel = f"chat:group:{group_id}"
    client_id = await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(f"Client {client_id}: {data}", channel)

    except WebSocketDisconnect:
        manager.disconnect(client_id, channel)


@app.websocket("/ws/private/{client_id}")
async def chat_private(websocket: WebSocket, client_id: str):
    channel = f"chat:private:{client_id}"
    client_id = await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(f"Client {client_id}: {data}", channel)


    except WebSocketDisconnect:
        manager.disconnect(client_id, channel)


