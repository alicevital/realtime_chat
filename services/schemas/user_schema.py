'''
Docstring for services.schemas(Schemas para futura integração com banco MongoDB)
'''
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserRequest(BaseModel):
    username: str
    name: str
    password: str
    is_admin: bool

class UserResponse(BaseModel):
    name: str
    username: str
    is_admin: bool
    id: Optional[str] = None
    date_created: datetime

class UserLogin(BaseModel):
    name: str
    password: str
