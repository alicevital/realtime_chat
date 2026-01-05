import asyncio
import uuid
from typing import List
from fastapi import WebSocket
import redis.asyncio as redis

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, dict[str, WebSocket]] = {}
        self.redis = redis.from_url("redis://redis:6379", decode_responses=True)
        self.channel = "chat:global"
    

    async def connect(self, websocket: WebSocket, channel: str) -> str:
        await websocket.accept()
        client_id = str(uuid.uuid4())

        if channel not in self.active_connections:
            self.active_connections[channel] = {}

        self.active_connections[channel][client_id] = websocket
        print(f" {client_id} se conectou no cannal {channel}")

        return client_id
    
    def disconnect(self, client_id: str, channel: str):
        self.active_connections.get(channel, {}).pop(client_id, None)
        print(f"client {client_id} desconectado")

    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str, channel: str): 
        for actives in self.active_connections.get(channel, {}).values():
            await actives.send_text(message)
    
    async def start_redis(self):
        pubsub = self.redis.pubsub()
        await pubsub.psubscribe("chat: ")

        async for message in pubsub.listen():
            if message["type"] == "pmessage":
                channel = message["channel"]
                data = message["data"]
                await self.broadcast(channel, data)

    async def publish(self, message: str, channel: str):
        await self.redis.publish(channel, message)

manager = WebSocketManager()