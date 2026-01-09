# import asyncio
import logging
import uuid
from fastapi import WebSocket
# import redis.asyncio as redis
from services.utils.database import redis_client

class WebSocketManager:
    '''
        Classe padrão de conexão websocket
    '''
    def __init__(self):
        self.active_connections: dict[str, dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str) -> str:
        '''
            Método de conexão, client_id é gerado com uuid;
            Adiciona canal em lista de conexões ativas;
            Mostra mensagem de sucesso.
        '''
        await websocket.accept()
        client_id = str(uuid.uuid4())

        if channel not in self.active_connections:
            self.active_connections[channel] = {}
            
        self.active_connections[channel][client_id] = websocket
        logging.info(f" {client_id} se conectou no cannal {channel}")

        return client_id
    

    def disconnect(self, client_id: str, channel: str):
        '''
            Método de desconexão, retira canal da fila com pop;
            retorna mensagem de sucesso.
        '''
        self.active_connections.get(channel, {}).pop(client_id, None)
        print(f"client {client_id} desconectado")


    async def send(self, message: str, websocket: WebSocket):
        '''
            Função de enviar mensagem;
            Envia mensagem via websocket.
        '''
        await websocket.send_text(message)


    async def broadcast(self, message: str, channel: str):
        '''
            Função de broadcast;
            Para cada ativo na lista de conexões ativos, ele envia a mensagem.
        ''' 
        for active in self.active_connections.get(channel, {}).values():
            await active.send_text(message)
    

    async def start_pub_sub(self):
        '''
            Inscreve client ao chat;
            Para cada mensagem enviada ao pubsub, clientes conectados escutam;
            data recebe dados da mensagem;
            broadcast envia para todos conectados.
        '''
        pubsub = redis_client.pubsub()
        await pubsub.psubscribe("chat:")

        async for message in pubsub.listen():
            if message["type"] == "pmessage":
                channel = message["channel"].decode()
                data = message["data"].decode()
                await self.broadcast(data, channel)


    async def save_message(self, channel: str, message: str):
        '''
            Função de salvar mensagens no redis;
            chave recebe nome do canal;
            rpush adiciona o elemento ao final da lista da chave;
        '''
        key = f"chat:messages:{channel}"
        await redis_client.rpush(key, message)


    async def publish(self, message: str, channel: str):
        '''
            Função de publicar mensagens;
            publica o salvamento com função save_message;
            publica o broadcast com a função broadcast;
            redis recebe tudo que foi publicado.
        '''
        await self.save_message(message, channel)
        await self.broadcast(message, channel)
        await redis_client.publish(message, channel)

manager = WebSocketManager()