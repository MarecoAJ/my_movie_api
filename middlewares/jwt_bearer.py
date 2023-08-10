
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token
from fastapi import  HTTPException, Request

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@mail.com":
            raise HTTPException(status_code=403, detail="credenciales no validas")
  