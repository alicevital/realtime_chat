from typing import Optional
from pydantic import BaseModel, ValidationError
from datetime import datetime

class RoomRequest(BaseModel):
    name_room: str
    username_creator: str

    def validation_admin(self):
        if "admin@secret" not in self.username_creator:
            raise ValidationError("Você não pode criar salas, apenas admins podem")

class RoomResponse(BaseModel):
    name_room: str
    date_created: datetime
    id: Optional[str] = None 
