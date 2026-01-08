'''
Docstring for services.schemas(Schemas para futura integração com banco MongoDB)
'''
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserRequest(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class UserResponse(BaseModel):
    username: str
    id: Optional[str] = None
    date_created: datetime
