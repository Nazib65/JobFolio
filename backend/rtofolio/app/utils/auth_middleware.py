import jwt
from fastapi import Request, HTTPException, status
from app.config import settings

JWT_SECRET = settings.SUPABASE_JWT_SECRET
ALGORITHM = "HS256" 

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    token = token.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms = [ALGORITHM],
            audience = "authenticated"
        )
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )