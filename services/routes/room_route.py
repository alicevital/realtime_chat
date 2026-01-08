from fastapi import APIRouter
from services.schemas.room_schema import RoomRequest, RoomResponse
from services.database import redis_client


router = APIRouter()

@router.post("/room/create")
def create_room(room: RoomRequest):
    
    return room

@router.get("/get/rooms")
def get_room(room: RoomResponse):
    return room