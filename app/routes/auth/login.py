from fastapi.responses import RedirectResponse
from app.core.config import settings
import urllib.parse

def get():
    scope = "openid email profile"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": scope,
        "access_type": "offline",
        "prompt": "consent"
    }
    encoded_params = urllib.parse.urlencode(params)
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{encoded_params}"
    return RedirectResponse(auth_url)
