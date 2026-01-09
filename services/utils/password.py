from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    '''
    Função que adiciona hash a senha armazenada
    '''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
        Função que verifica se senha é correspondente ao senha com hash
    '''
    return pwd_context.verify(plain_password, hashed_password)