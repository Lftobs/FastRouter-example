from fastapi import Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import Optional

from app.core.database import get_session
from app.models.user import User
from app.models.todo import Todo
from app.dependencies import get_current_user, get_current_user_optional

def get(request: Request, user: Optional[User] = Depends(get_current_user_optional), session: Session = Depends(get_session)):
    templates: Jinja2Templates = request.app.state.templates
    
    todos = []
    if user:
        statement = select(Todo).where(Todo.owner_id == user.id).order_by(Todo.id.desc())
        todos = session.exec(statement).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "todos": todos,
        "user": user
    })

def post(
    request: Request, 
    title: str = Form(...), 
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    templates: Jinja2Templates = request.app.state.templates
    
    todo = Todo(title=title, owner_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    
    return templates.TemplateResponse("todo.html", {"request": request, "todo": todo})
