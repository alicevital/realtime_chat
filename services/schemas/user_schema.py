'''
Docstring for services.schemas(Schemas para futura integração com banco MongoDB)
'''
from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    name: str
    password: str
    is_admin: bool

class UserLogin(BaseModel):
    name: str
    password: str
