from services.schemas.user_schema import UserLogin, UserRequest
from services.utils.database import redis_client
from fastapi import APIRouter, HTTPException
from services.utils.password import hash_password


router = APIRouter()

@router.post("/user/register")
async def create_user(user: UserRequest):
    '''
        Função da rota de criar user, recebe o schema como parametro; 
        cria uma chave que armazena o username da classse UserRequest;
        verifica se usuário já existe;
        verifica se o user é admin;
        insere o usuário e seus dados no redis.
    '''
    user_key = f"user:{user.username}"

    if await redis_client.exists(user_key):
        raise HTTPException(status_code=400, detail="Esse nome de username já existe!")

    is_admin = "true" if "admin@secret" in user.username else "false"

    await redis_client.hset(user_key, mapping={
            "username": user.username,
            "name": user.name,
            "password": user.password,
            "is_admin": is_admin
        }
    )

    return {"message": "Usupario criado com sucesso",
            "name": user.name,
            "is_admin": is_admin}


@router.get("/user/consult")
async def get_user_by_name(username: str):
    '''
        Função que busca usuário por nome;
        chave recebe username como parametro;
        Verifica se usuário existe com function exists do redis;
        user_data recebe os dados do user a partir do comando hgetall do redis;
        retorna dados do usuário.
    '''
    user_key = f"user:{username}"

    if not await redis_client.exists(user_key):
        raise HTTPException(status_code=404, detail="Não existe esse usuário")

    user_data = await redis_client.hgetall(user_key)

    return {
        "name": user_data.get("name"),
        "is_admin": user_data.get("is_admin")
    }


@router.post("/user/login")
async def login(user: UserLogin):
    '''
        Função de login de usuário;
        Verifica se user existe no redis;
        user_data recebe dados do user buscado no redis;
        Verifica se password é correspondente ao usuário;
        Adiciona usuário a coleção de usuários logados;
        retorna mensagem de usuário logado.
    '''

    user_key = f"user:{user.username}"
    
    if not await redis_client.exists(user_key):
        raise HTTPException(status_code=404, detail="Usuário não existe, crie.")
    
    user_data = await redis_client.hgetall(user_key)

    if user.password != user_data["password"]:
        raise HTTPException(
            status_code=401, detail="Senha incorreta"
        )
    
    await redis_client.sadd("logged_users", user.username)

    return {
        "message": "Login realizado com sucesso!",
        "name": user_data["name"],
        "is_admin": user_data["is_admin"]
    }