import asyncio
import json
from typing import List
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("conexão bem sucedida!")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("client desconectado")

    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str): 
        for actives in self.active_connections:
            await actives.send_text(message)

manager = WebSocketManager()