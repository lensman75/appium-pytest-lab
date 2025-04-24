from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse, FileResponse
from api.tasks import run_test
import os
from celery.result import AsyncResult
from api.celery_app import app as celery_app


app = FastAPI()
status_message="<h1>Done</h1>"

@app.get("/", response_class=JSONResponse)
def read_root():
    return {"message":"Test message"}

@app.get("/one", response_class=PlainTextResponse)
def read_file():
    file_path = "../json/card.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.get("/executing", response_class=HTMLResponse)
def sometest():
    return "<h1>Executing</h1>"

@app.get("/status", response_class=HTMLResponse)
def stat():
    global status_message
    return f"{status_message}"

@app.get("/booking/") #Change name, AddTask for example
def get_booking(HOTEL: str, DAY: str, DATE: str):
    # job = q.enqueue(run_test, HOTEL, DAY, DATE)
    task = run_test.delay(HOTEL, DAY, DATE)
    print("task: ", task)


    return {
        "message": "Test started",
        "job_id": task.id,
        "status": task.status
    }

@app.get("/get_task_status/{task_id}", response_class=JSONResponse)
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }

@app.get("/get_screenshot/{task_id}", response_class=FileResponse)
def get_screenshot(task_id: str):
    screenshot_path = os.path.join("screenshots", f"screenshot_{task_id}.png")
    
    # TODO: Add error catching
    
    return FileResponse(screenshot_path, media_type="image/png", filename=f"screenshot_{task_id}.png")