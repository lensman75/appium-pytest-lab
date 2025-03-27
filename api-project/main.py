from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/")
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
