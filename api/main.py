from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from redis import Redis
from rq import Queue
import os
# import subprocess

from tasks import run_test

app = FastAPI()
status_message="<h1>Done</h1>"

redis_conn = Redis()
q = Queue(connection=redis_conn)


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

@app.get("/booking/")
def get_booking(HOTEL: str, DAY: str, DATE: str):
    job = q.enqueue(run_test, HOTEL, DAY, DATE)
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
        "job_id": job.get_id(),
        "status": job.get_status()
    }