from passlib.hash import sha256_crypt

def hash(password: str):
    return sha256_crypt.hash(password)


def verify(plain_password, hashed_password):
    return( sha256_crypt.verify(plain_password,hashed_password))



# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash(password: str):
#     return pwd_context.hash(password)

# def verify(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
    
# Source: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
