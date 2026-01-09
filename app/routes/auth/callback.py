from fastapi import Request, Response, HTTPException, Depends
from sqlmodel import Session
from fastapi.responses import RedirectResponse
import httpx
from sqlmodel import select
from app.core.config import settings
from app.core.database import get_session
from app.models.user import User
from app.core.security import create_access_token

async def get(request: Request, session: Session = Depends(get_session)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")

    # Exchange code for token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data["access_token"]
        
        # Get user info
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info_response.raise_for_status()
        user_info = user_info_response.json()

    try:
        statement = select(User).where(User.email == user_info["email"])
        result = session.exec(statement)
        user = result.first()
        
        if not user:
            user = User(
                email=user_info["email"],
                name=user_info.get("given_name", "User"),
                picture=user_info.get("picture"),
                provider="google"
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        
        # Create JWT
        access_token = create_access_token(data={"sub": user.email, "id": user.id})
        
        response = RedirectResponse(url="/")
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True, # Should be True in production
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        return response
    finally:
        session.close()
