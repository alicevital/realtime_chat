from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from services.websocket_manager import WebSocketManager, manager

app = FastAPI()


@app.websocket("/ws/global")
async def websocket_endepoint(websocket: WebSocket):
    client_id = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send(f"Message: {data}", websocket)
            await manager.broadcast(f"Client {client_id} says: {data}")

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client {client_id} has left the chat")


