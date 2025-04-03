from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from backend.core.config import SECRET_KEY, JWT_ALGORITHM


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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": user_email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
