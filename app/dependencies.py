from typing import Generator, Optional
from fastapi import Request, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.security import verify_token
from app.core.config import settings
from app.models.user import User

def get_current_user_optional(request: Request, session: Session = Depends(get_session)) -> Optional[User]:
    token_cookie = request.cookies.get("access_token")
    if not token_cookie:
        return None
    
    scheme, _, token = token_cookie.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    
    payload = verify_token(token)
    if not payload:
        return None
    
    email = payload.get("sub")
    if not email:
        return None
        
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

def get_current_user(user: Optional[User] = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
