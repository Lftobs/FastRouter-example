# FastRouter Example Project

This project demonstrates how to use `fast-router` with FastAPI for file-based routing, similar to Next.js or SvelteKit. It implements a full-featured Todo application using **HTMX**, **SQLModel**, and **Jinja2 Templates**.

## Features

*   **File-based Routing**: Using [fast-router](https://github.com/dmontagu/fast-router) to automatically generate routes from the file structure in `app/routes`.
*   **HTMX Frontend**: A dynamic, single-page-like experience without complex JavaScript frameworks.
*   **Database**: SQLite with SQLModel (SQLAlchemy + Pydantic).
*   **Authentication**: Google OAuth2 integration.

## Project Structure

The URL structure is defined by the file system in `app/routes`:

```
.
├── app
│   ├── core               # Database config, security, settings
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models             # SQLModel database models
│   │   ├── todo.py
│   │   └── user.py
│   ├── routes             # File-based routes (FastRouter)
│   │   ├── auth
│   │   │   ├── callback.py    # GET /auth/callback
│   │   │   ├── login.py       # GET /auth/login
│   │   │   └── logout.py      # GET /auth/logout
│   │   └── todos
│   │       ├── [id]           # Dynamic route /todos/{id}
│   │       │   ├── edit.py    # GET /todos/{id}/edit
│   │       │   └── index.py   # GET, PUT, DELETE /todos/{id}
│   │       └── index.py       # GET /todos, POST /todos
│   ├── templates          # Jinja2 templates for HTMX
│   │   ├── index.html
│   │   ├── layout.html
│   │   ├── todo.html
│   │   └── todo_edit.html
│   └── dependencies.py    # Shared FastAPI dependencies
├── static                 # Static files (CSS, JS)
├── main.py                # App entrypoint
└── pyproject.toml         # Project dependencies
```

## Setup & Running

This project uses `uv` for dependency management.

1.  **Install Dependencies**:
    ```bash
    uv sync
    ```

2.  **Environment Setup**:
    Copy `.env.example` to `.env` (if provided) or create one:
    ```bash
    cp .env .env.local
    ```
    *Note: You will need Google OAuth credentials for login to work properly.*

3.  **Run the Server**:
    ```bash
    uv run uvicorn main:app --reload
    ```
    Open [http://localhost:8000](http://localhost:8000) in your browser.


## Technologies

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [FastRouter](https://pypi.org/project/fast-router/)
*   [SQLModel](https://sqlmodel.tiangolo.com/)
*   [HTMX](https://htmx.org/)
*   [UV](https://github.com/astral-sh/uv)
