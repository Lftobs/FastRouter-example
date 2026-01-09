from fastapi import Request, Response, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.core.database import get_session
from app.models.user import User
from app.models.todo import Todo
from app.dependencies import get_current_user

def get(
    request: Request,
    id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, id)
    if not todo or todo.owner_id != user.id:
        return Response(status_code=404)
        
    templates: Jinja2Templates = request.app.state.templates
    return templates.TemplateResponse("todo_edit.html", {"request": request, "todo": todo})
