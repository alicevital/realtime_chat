'''
Docstring for services.schemas(Schemas para futura integração com banco MongoDB)
'''
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    username: str
    name: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
