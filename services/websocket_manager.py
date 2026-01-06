# import asyncio
import logging
import uuid
from fastapi import WebSocket
# import redis.asyncio as redis
from services.database import redis_client

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str) -> str:
        await websocket.accept()
        client_id = str(uuid.uuid4())

        if channel not in self.active_connections:
            self.active_connections[channel] = {}
            
        self.active_connections[channel][client_id] = websocket
        logging.error(f" {client_id} se conectou no cannal {channel}")

        return client_id
    

    def disconnect(self, client_id: str, channel: str):
        self.active_connections.get(channel, {}).pop(client_id, None)
        print(f"client {client_id} desconectado")


    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


    async def broadcast(self, message: str, channel: str): 
        for active in self.active_connections.get(channel, {}).values():
            await active.send_text(message)
    

    async def start_redis(self):
        pubsub = redis_client.pubsub()
        await pubsub.psubscribe("chat:")

        async for message in pubsub.listen():
            if message["type"] == "pmessage":
                channel = message["channel"].decode()
                data = message["data"].decode()
                await self.broadcast(data, channel)


    async def save_message(self, channel: str, message: str):
        key = f"chat:messages:{channel}"
        await redis_client.rpush(key, message)


    async def publish(self, message: str, channel: str):
        await self.save_message(message, channel)
        await self.broadcast(message, channel)
        await redis_client.publish(message, channel)

manager = WebSocketManager()