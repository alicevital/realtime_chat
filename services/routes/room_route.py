from fastapi import APIRouter, HTTPException
from services.schemas.room_schema import RoomRequest, RoomResponse
from services.utils.database import redis_client


router = APIRouter()

@router.post("/room/create")
async def create_room(room_name: str, username: str):

    user_key = f"user:{username}"

    if not await redis_client.exists(user_key):
        raise HTTPException(404, "Usuário não existe")
    
    user_data = await redis_client.hgetall(user_key)

    if user_data["is_admin"] != "true":
        raise HTTPException(403, "Apenas admins podem criar salas")
    
    if not await redis_client.sismember("logged_users", username):
        raise HTTPException(403, "Usuário não está logado")
    
    if await redis_client.sismember("rooms", room_name):
        raise HTTPException(400, "Sala já existe")
    
    await redis_client.sadd("rooms", room_name)

    return {"message": f"Sala '{room_name}' criada!"}

@router.get("/get/rooms")
def get_room(room: RoomResponse):
    pass