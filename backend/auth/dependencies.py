from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def get_current_user(request: Request) -> dict:
    """
    Extract the current user from the access_token cookie.
    Raises HTTPException if invalid or missing.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    token = token.replace("Bearer ", "")

    try:
        SECRET_KEY = os.getenv("SECRET_KEY")
        if not SECRET_KEY:
            raise RuntimeError("SECRET_KEY environment variable is not set")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": user_email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
