"""
TaskFlow Backend - FastAPI Task Management Service

A RESTful API for task management with TDD approach.

TP 1 & 2: Uses in-memory storage for simplicity
TP 3: Will introduce PostgreSQL database (see migration guide)
"""

from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("taskflow")


# =============================================================================
# ENUMS & MODELS
# =============================================================================

class TaskStatus(str, Enum):
    """Task status enum - simpler than SQLAlchemy version."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    """Task priority enum - simpler than SQLAlchemy version."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    """Model for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    assignee: Optional[str] = Field(None, max_length=100, description="Assigned user")
    due_date: Optional[datetime] = Field(None, description="Due date")


class TaskUpdate(BaseModel):
    """Model for updating a task - all fields optional for partial updates."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = None


class Task(TaskCreate):
    """Model for a task with ID and timestamps."""
    id: int  # Integer ID instead of UUID string - simpler!
    created_at: datetime
    updated_at: datetime


# =============================================================================
# IN-MEMORY STORAGE (for Atelier 1 & 2)
# =============================================================================

# Simple dictionary to store tasks
# In Atelier 3, this will be replaced with PostgreSQL database
tasks_db: Dict[int, Task] = {}
next_id = 1


def get_next_id() -> int:
    """Get next available task ID."""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id


def clear_tasks():
    """Clear all tasks - useful for testing."""
    global tasks_db, next_id
    tasks_db = {}
    next_id = 1


# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="TaskFlow API",
    description="Simple task management API for learning unit testing and CI/CD",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
def startup():
    """Simple startup - just log a message."""
    logger.info("🚀 TaskFlow backend starting up...")
    logger.info("Using in-memory storage (no database)")


@app.on_event("shutdown")
def shutdown():
    """Simple shutdown - just log a message."""
    logger.info("🛑 TaskFlow backend shutting down...")


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "Welcome to TaskFlow API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "tasks_count": len(tasks_db)
    }


@app.get("/tasks", response_model=List[Task])
async def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None
) -> List[Task]:
    """
    Get all tasks with optional filtering.

    Query parameters:
    - status: Filter by task status (todo, in_progress, done)
    - priority: Filter by priority (low, medium, high)
    - assignee: Filter by assignee email
    """
    tasks = list(tasks_db.values())

    # Apply filters
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if assignee:
        tasks = [t for t in tasks if t.assignee == assignee]

    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int) -> Task:
    """Get a single task by ID."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return tasks_db[task_id]


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate) -> Task:
    """Create a new task."""
    # Validate title is not empty
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=422, detail="Title cannot be empty")

    # Create new task with auto-generated ID
    task_id = get_next_id()
    now = datetime.utcnow()

    task = Task(
        id=task_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        assignee=task_data.assignee,
        due_date=task_data.due_date,
        created_at=now,
        updated_at=now
    )

    tasks_db[task_id] = task
    logger.info(f"Task created successfully: {task_id}")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updates: TaskUpdate) -> Task:
    # 1) Vérifier l'existence
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    # 2) Récupérer la tâche existante
    existing_task: Task = tasks_db[task_id]

    # 3) Champs fournis (partial update)
    update_data = updates.model_dump(exclude_unset=True)

    # 4) Valider le titre s'il est fourni
    if "title" in update_data and (update_data["title"] is None or str(update_data["title"]).strip() == ""):
        raise HTTPException(status_code=422, detail="Title cannot be empty")

    # 5) Construire la nouvelle tâche (en gardant created_at)
    updated_task = Task(
        id=task_id,
        title=update_data.get("title", existing_task.title),
        description=update_data.get("description", existing_task.description),
        status=update_data.get("status", existing_task.status),
        created_at=existing_task.created_at,
        updated_at=datetime.utcnow(),
    )

    # 6) Persister
    tasks_db[task_id] = updated_task

    # 7) Retourner
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """
    Delete a task by ID.

    TODO (TP 1 - Exercice 1): Implémenter cette fonction

    Étapes à suivre:
    1. Vérifier que la tâche existe dans tasks_db
       - Si elle n'existe pas, lever HTTPException(status_code=404, detail=f"Task {task_id} not found")

    2. Supprimer la tâche du dictionnaire tasks_db
       - Utiliser: del tasks_db[task_id]

    3. Retourner None (car status_code=204 n'a pas de body)

    Indice: C'est très simple, seulement 3 lignes de code !
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    del tasks_db[task_id]
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)