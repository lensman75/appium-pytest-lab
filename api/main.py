from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from api.tasks import run_test
# from redis import Redis
# from rq import Queue
import os
# import subprocess
from celery.result import AsyncResult
from api.celery_app import app as celery_app


app = FastAPI()
status_message="<h1>Done</h1>"

# redis_conn = Redis()
# q = Queue(connection=redis_conn)


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

    # env = os.environ.copy()
    # env["HOTEL"] = HOTEL
    # env["DAY"] = DAY
    # env["DATE"] = DATE

    # print(f'env["HOTEL"] = "{HOTEL}"')
    # print(f'env["DAY"] = "{DAY}"')
    # print(f'env["DATE"] = "{DATE}"')

    # result = subprocess.run(
        # ["pytest", "-v", "-s", "test.py"],
        # shell=True,
        # env=env,
        # capture_output=True,
        # text=True
    # )
    # return {
    #     "HOTEL": HOTEL,
    #     "DAY": DAY,
    #     "DATE": DATE
    # }
    # return{
    #     "stdout": result.stdout,
    #     "stderr": result.stderr,
    #     "returncode": result.returncode
    # }

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