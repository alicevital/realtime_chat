import asyncio
import uuid
from typing import List
from fastapi import WebSocket
import redis.asyncio as redis

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.redis = redis.from_url("redis://redis:6379", decode_responses=True)
        self.channel = "chat:global"
    

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        client_id = str(uuid.uuid4())
        self.active_connections[client_id] = websocket
        print(f"conexão bem sucedida!{client_id}")

        return client_id
    
    def disconnect(self, client_id: str):
        self.active_connections.remove(client_id, None)
        print(f"client {client_id} desconectado")

    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str): 
        for actives in self.active_connections.values():
            await actives.send_text(message)
    
    async def start_redis(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.channel)

        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"]
                await self.broadcast(data)

    async def publish(self, message: str):
        await self.redis.publish(self.channel, message)

manager = WebSocketManager()