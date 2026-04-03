from datetime import datetime, timedelta
from google import genai
import time
import threading
from dotenv import load_dotenv
import os


load_dotenv() 
# 1. Setup your API Key (Use your freshly generated one later) -> GEMINI AI 

# RAM Memory
tasks = []

def ask_ai(task_name):
    """Sends the task context to the cloud AI."""
    prompt = f"I have a task: '{task_name}' coming up very soon. Act as a proactive, supportive assistant. Ask me a quick question to ensure I am ready or have what I need. Keep it under 2 sentences."
    
    try:
        print("[SYSTEM: Reaching out to Cloud AI...]")
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt,
        )
        return response.text
        
    except Exception as e:
        return f"Whoops, the AI hit a snag: {e}"

def add_task(task_name, minutes_until_due):
    """Creates a task and calculates exactly when to check in."""
    now = datetime.now()
    due_time = now + timedelta(minutes=minutes_until_due)
    check_in_time = due_time - timedelta(minutes=1) 

    task = {
        "name": task_name,
        "due_time": due_time,
        "check_in_time": check_in_time,
        "has_checked_in": False
    }
    tasks.append(task)
    print(f"✅ Added: '{task_name}'. Due at {due_time.strftime('%H:%M:%S')}.")
    print(f"⏳ The AI will check in at exactly {check_in_time.strftime('%H:%M:%S')}.\n")

def run_scheduler():
    """The 'Alarm Clock' loop that constantly checks the time."""
    print("Background scheduler running. Watching the clock...\n")
    
    while True:
        now = datetime.now()
        
        for task in tasks:
            if now >= task["check_in_time"] and not task["has_checked_in"]:
                print(f"[SYSTEM: Time to check on '{task['name']}']...")

                ai_message = ask_ai(task['name'])
                print(f"\n🤖 Assistant: {ai_message}\n")
                
                task["has_checked_in"] = True 
                
        time.sleep(10) 

# --- EXECUTION ---
if __name__ == "__main__":
    add_task("Test the AI assistant", 5)
    run_scheduler()