import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from services.websocket_manager import manager

app = FastAPI()

@app.on_event("startup")
async def startup():
    asyncio.create_task(manager.start_redis())


@app.websocket("/ws/global")
async def websocket_endepoint(websocket: WebSocket):
    client_id = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(f"Client {client_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.publish(f"Client {client_id} saiu do chat")


