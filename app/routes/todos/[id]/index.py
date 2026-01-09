from fastapi import Request, Response, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from typing import Optional

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
    return templates.TemplateResponse("todo.html", {"request": request, "todo": todo})

def put(
    request: Request,
    id: int,
    title: Optional[str] = Form(None),
    completed: Optional[bool] = Form(None),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, id)
    if not todo or todo.owner_id != user.id:
        return Response(status_code=404)

    if title is not None:
        todo.title = title
    if completed is not None:
        todo.completed = completed
        
    session.add(todo)
    session.commit()
    session.refresh(todo)
    
    templates: Jinja2Templates = request.app.state.templates
    return templates.TemplateResponse("todo.html", {"request": request, "todo": todo})

def delete(
    request: Request, 
    id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, id)
    if not todo or todo.owner_id != user.id:
        return Response(status_code=404)
        
    session.delete(todo)
    session.commit()
    return Response(status_code=200)
