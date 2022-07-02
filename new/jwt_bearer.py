from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from new.jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request : Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, details="Invalid or Expired Token!")
            else:
                return credentials.credentials
        else:
            raise HTTPException(status_code=403, details="Invalid or Expired Token!")

    def verify_jwt(self, jwttoken: str):
        isTokenValid : bool = False
        payload = decodeJWT(jwttoken)
        if payload:
            idTokenValid = True
        return isTokenValid