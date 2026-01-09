from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fast_router import create_router
from fastapi.templating import Jinja2Templates
from app.dependencies import get_current_user_optional

# Initialize FastRouter
router = create_router("app/routes")
app = router.get_app()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

app.state.templates = templates

@app.get("/")
async def root():
    return RedirectResponse(url="/todos")

