from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional 
import os 
from dotenv import load_dotenv 
from google import genai
from google.genai import types  
from Class.models import * 
import json
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)

# Consts 
MESSAGE = "message" # lmao the irony
#Make title 
app = FastAPI(title="Proactive AI To Do List")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

Ram = []
#--Routes (in this case no, not all routes gonna take u to rome)

# Create route or url for endpoint
@app.get("/")
async def root():
    return {MESSAGE : "Backend is alive"}

@app.post("/tasks/")
async def creating_task(task: Task):
    Ram.append(task)
    return {MESSAGE : "Task Created: ", "task": task}

@app.get("/tasks/")
async def get_all_tasks():
    return {"total task" : len(Ram), "task" : Ram} 

@app.get("/ai-test/")
async def test_ai():
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Say 'Hello Simran, my AI brain is online!' in a robotic way."
    )
    return {"ai_response": response.text}

# --- THE AI DECOMPOSER ROUTE ---
@app.post("/decompose/")
async def decompose_task(vague_task: str):
    # 1. The Prompt
    prompt = f"""
    You are an expert productivity assistant. 
    Take the following task and break it down into 3 to 5 highly actionable, 
    bite-sized sub-tasks. 
    Task: {vague_task}
    """
    
    # 2. The AI Call (with Structured Output)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", 
            response_schema=TaskBreakdown,         
            temperature=0.2 # Keep the AI logical, not creative
        ),
    )
    
    # 3. Convert the AI's string response back into a Python dictionary
    structured_data = json.loads(response.text)

    main_task = Task(
        id=len(Ram) + 1,
        title=structured_data["main_task"],
        description="Main Goal",
        completed=False
    )
    Ram.append(main_task)

    for data in structured_data["sub_tasks"]: # Cuz gonna have multiple sbutask for each task 
        # We combine the AI's description and the time estimate into one string
        
        sub_task = Task(
            id=len(Ram) + 1,
            title=f"↳ {data['title']}",  # Added a little arrow so it looks like a sub-task
            description=data['description'],
            completed=False,
            est_time=data['est_time']
        )
        Ram.append(sub_task)
        
    return {"message": "Task successfully broken down!", "data": structured_data}
