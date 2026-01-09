# FastRouter Example Project

This request demonstrates how to use `fast-router` with FastAPI for file-based routing, similar to Next.js or SvelteKit. It implements a full-featured Todo application using **HTMX**, **SQLModel**, and **Jinja2 Templates**.

## Features

*   **File-based Routing**: Using [fast-router](https://github.com/dmontagu/fast-router) to automatically generate routes from the file structure in `app/routes`.
*   **HTMX Frontend**: A dynamic, single-page-like experience without complex JavaScript frameworks.
*   **Database**: SQLite with SQLModel (SQLAlchemy + Pydantic).
*   **Authentication**: Google OAuth2 integration.
*   **Benchmarks**: Comparisons between `fast-router` and standard FastAPI routing.

## Project Structure

The URL structure is defined by the file system in `app/routes`:

```
app/routes/
├── todos/
│   ├── index.py           # GET /todos, POST /todos
│   └── [id]/              # Nested dynamic route
│       ├── index.py       # GET, PUT, DELETE /todos/{id}
│       └── edit.py        # GET /todos/{id}/edit (Edit form)
└── auth/
    ├── login.py
    └── ...
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

## Benchmarks

This project includes benchmarking scripts to compare `fast-router` against standard `fastapi.include_router` scaling.

*   **Results**: See [BENCHMARK.md](./BENCHMARK.md).
*   **Summary**: `fast-router` improves startup time by **~2.3x** for 500 routes and **~1.13x** for 200 complex resource modules vs standard routing.

**Run Benchmarks:**
```bash
# Synthetic benchmark (500 simple routes)
uv run python -m benchmarks.run_benchmark

# Real-world benchmark (200 complex resources)
uv run python -m benchmarks.run_real_benchmark
```

## Technologies

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [FastRouter](https://pypi.org/project/fast-router/)
*   [SQLModel](https://sqlmodel.tiangolo.com/)
*   [HTMX](https://htmx.org/)
*   [UV](https://github.com/astral-sh/uv)
