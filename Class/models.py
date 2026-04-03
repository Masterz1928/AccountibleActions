from pydantic import BaseModel
from typing import Optional

# --- STANDARD MODELS ---
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# --- AI DECOMPOSER MODELS ---
class SubTask(BaseModel):
    title: str
    description: str
    difficulty: str 
    est_time: Optional[int] = None 

class TaskBreakdown(BaseModel):
    main_task: str
    difficulty: str 
    sub_tasks: list[SubTask]

    