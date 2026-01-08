from services.schemas.user_schema import UserLogin, UserRequest
from services.database import redis_client
from fastapi import APIRouter


router = APIRouter()

@router.post("/user/register")
def create_user(user: UserRequest):
    '''
        Função da rota de criar user, recebe o dto como parametro, 
        cria uma chave que armazena o username da classse UserRequest,
        verifica se o user é admin, 
        insere o usuário e seus dados no redis
    '''
    user_key = f"user:{user.username}"

    if not redis_client.exists.user:
        raise Exception("Esse nome de username já existe!")

    if "admin@secret" not in user.username:
        is_admin = False

    if "admin@secret" in user.username:
        is_admin = True

    verify_admin = is_admin

    redis_client.hset(user_key, mapping={
            "username": user.username,
            "name": user.name,
            "password": user.password,
            "is_admin": verify_admin
        }
    )

    return user

@router.get("/user/list")
async def get_user_by_name(name: str):
    # user_key = f"user:{name}" <- testar sem usar key

    if not redis_client.exists(f"user:{name}"):
        raise Exception("Não existe esse usuário")
    else:
        return name


@router.post("/user/login")
def login(user: UserLogin):

    users_loggeds = user
    
    if redis_client.exists(f"user:{user.name}"):
        return users_loggeds
    else:
        return {"message": "Usuário não existe, faça o cadastro"}