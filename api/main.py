from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse

app = FastAPI()
status_message="<h1>Done</h1>"


@app.get("/", response_class=HTMLResponse)
def read_root():
    return {"Test message"}

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