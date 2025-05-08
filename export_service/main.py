from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid

app = FastAPI()
STORE = Path("/app/files")
STORE.mkdir(exist_ok=True)

@app.post("/export")
async def export(file: UploadFile = File(...)):
    dest = STORE / f"{uuid.uuid4()}-{file.filename}"
    with dest.open("wb") as out:
        out.write(await file.read())
    return JSONResponse({"url": f"/files/{dest.name}"})

@app.get("/files/{fname}")
async def get_file(fname: str):
    path = STORE / fname
    return FileResponse(path)
